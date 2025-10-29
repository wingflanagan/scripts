#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

// ─────────────────────────────────────────────────────────────
// Helpers to remove comments from JSON (// and /* */)
function removeComments(jsonStr) {
  // Remove single-line comments:
  jsonStr = jsonStr.replace(/\/\/.*$/gm, "");
  // Remove multi-line comments:
  jsonStr = jsonStr.replace(/\/\*[\s\S]*?\*\//gm, "");
  return jsonStr;
}

// ─────────────────────────────────────────────────────────────
// Note conversion helpers
const NOTE_NAMES = { C: 0, "C#": 1, D: 2, "D#": 3, E: 4, F: 5, "F#": 6, G: 7, "G#": 8, A: 9, "A#": 10, B: 11 };

function noteToMidi(note) {
  // Assumes note format like "C3" or "D#4" (octave is integer)
  // MIDI number = (octave + 1)*12 + noteIndex.
  const match = note.match(/^([A-G]#?)(-?\d+)$/);
  if (!match) {
    throw new Error("Invalid note format: " + note);
  }
  const [, noteName, octaveStr] = match;
  const octave = parseInt(octaveStr, 10);
  if (!(noteName in NOTE_NAMES)) {
    throw new Error("Unknown note name: " + noteName);
  }
  return (octave + 1) * 12 + NOTE_NAMES[noteName];
}

function midiToNote(midi) {
  // Reverse conversion (choose sharps)
  const octave = Math.floor(midi / 12) - 1;
  const noteIndex = midi % 12;
  const noteName = Object.keys(NOTE_NAMES).find(k => NOTE_NAMES[k] === noteIndex);
  return noteName + octave;
}

function transposeNote(note, semitones) {
  const m = noteToMidi(note);
  return midiToNote(m + semitones);
}

// ─────────────────────────────────────────────────────────────
// Generate an array of note names from lowNote to highNote (inclusive)
function getNoteRange(lowNote, highNote) {
  const lowMidi = noteToMidi(lowNote);
  const highMidi = noteToMidi(highNote);
  const notes = [];
  for (let m = lowMidi; m <= highMidi; m++) {
    notes.push(midiToNote(m));
  }
  return notes;
}

// ─────────────────────────────────────────────────────────────
// Extract notes from a file name. Supports either "_A2.wav" or "_A1-A2.wav"
function extractNotesFromFilename(fileName) {
  // Matches either _A2.wav or _A1-A2.wav
  const m = fileName.match(/_([A-G][#]?\d)(?:-([A-G][#]?\d))?\.wav$/i);
  if (m) {
    // If there's a dash, m[2] will be the "to" note and m[1] the "from" note.
    return m[2] ? { from: m[1], to: m[2] } : { to: m[1] };
  }
  return null;
}

// ─────────────────────────────────────────────────────────────
// Given a regex string (from JSON) compile a RegExp.
function buildRegex(regexStr) {
  return new RegExp(regexStr);
}

// ─────────────────────────────────────────────────────────────
// Given a list of files (names) and a RegExp, return an array of objects for
// each file that matches and for which we can extract a note.
function getMatchingSamples(files, regex) {
  const result = [];
  files.forEach(file => {
    // ignore hidden files
    if (file[0] === ".") return;
    if (regex.test(file)) {
      const notes = extractNotesFromFilename(file);
      if (notes && notes.to) {
        result.push({
          fileName: file,
          note: notes.to,           // Use the "to" note as the key center.
          midi: noteToMidi(notes.to),
          from: notes.from || null  // Save the "from" note if available.
        });
      }
    }
  });
  // sort by MIDI note
  result.sort((a, b) => a.midi - b.midi);
  return result;
}

// ─────────────────────────────────────────────────────────────
// Given an instrument key (a note string) and an array of available sample objects,
// choose a sample file using the following rules:
// - If the key is below the lowest sample’s pitch, use the first sample.
// - Otherwise, choose the first sample whose midi is >= key midi;
// - If none is found (i.e. key is above highest sample), use the last sample.
function chooseSampleForKey(key, samples) {
  const keyMidi = noteToMidi(key);
  if (samples.length === 0) return null;
  if (keyMidi <= samples[0].midi) {
    return samples[0];
  }
  for (let i = 0; i < samples.length; i++) {
    if (samples[i].midi >= keyMidi) {
      return samples[i];
    }
  }
  return samples[samples.length - 1];
}

// ─────────────────────────────────────────────────────────────
// Build a string of key=value pairs from an object.
// When breakIntoLines is false the properties are output in columns with fixed widths.
// (Here we assume that region lines will usually have these keys.)
function buildPropertiesLine(props, breakIntoLines = true) {
  // Preferred order – note that keys not in this list will be appended afterwards.
  const order = [
    "trigger",
    "group",
    "note_polyphony",
    "off_by",
    "off_mode",
    "offset",
    "loop_mode",
    "seq_length",
    "lovel",
    "hivel",
    "volume",
    "xfin_lovel",
    "xfin_hivel",
    "xfout_lovel",
    "xfout_hivel",
    "ampeg_attack",
    "ampeg_decay",
    "ampeg_hold",
    "ampeg_sustain",
    "ampeg_release",
    "ampeg_decay_shape",
    "ampeg_attack_shape",
    // These are the extra keys that you see in region lines:
    "sample",
    "pitch_keycenter",
    "lokey",
    "hikey",
    "sw_previous",
    "seq_position"
  ];
  
  // First, collect items in the desired order.
  const items = [];
  for (let key of order) {
    if (props.hasOwnProperty(key)) {
      items.push({ key, value: props[key] });
    }
  }
  // Then add any other properties that were not in the order array.
  for (let key in props) {
    if (!order.includes(key)) {
      items.push({ key, value: props[key] });
    }
  }
  
  if (breakIntoLines) {
    // When breaking into lines simply join with newlines.
    return items.map(item => `${item.key}=${item.value}`).join("\n\t");
  } else {
    // For inline formatting we want to line up the columns.
    // For keys that we expect in region lines, we set fixed column widths.
    // (Adjust these numbers as needed for your typical data.)
    const fixedWidths = {
      sample: 40,           // e.g., "sample=samples/BP_02leg_mf_3-do_D#1.wav" padded to 40 characters
      pitch_keycenter: 24,  // e.g., "pitch_keycenter=D#1" padded to 24 characters
      lokey: 10,            // e.g., "lokey=D#1" padded to 10 characters
      hikey: 10             // e.g., "hikey=F4" padded to 10 characters
      // sw_previous and seq_position are left as-is
    };
    
    const formatted = items.map(item => {
      const str = `${item.key}=${item.value}`;
      if (fixedWidths.hasOwnProperty(item.key) && fixedWidths[item.key] > 0) {
        return str.padEnd(fixedWidths[item.key], " ");
      } else {
        return str;
      }
    });
    // Join the formatted items with a single space between columns.
    return formatted.join(" ");
  }
}

// ─────────────────────────────────────────────────────────────
// Build a comment header for a section.
function buildSectionComment(instrumentName, type, groupName) {
  const title = groupName ? `${instrumentName} ${type} samples - ${groupName}` : `${instrumentName} ${type} samples`;
  const borderStart = "/****************************************************************************************************";
  const borderEnd = "****************************************************************************************************/";
  return `${borderStart}\n * ${title}\n${borderEnd}\n`;
}

// ─────────────────────────────────────────────────────────────
// Process a single group and return an object:
// { comment, headerProps, regions, crossfadeOverlap }
function processGroup(params) {
  // params: { group, instrumentRange, files, instrumentName, extra (optional: roundRobin) }
  const group = params.group;
  const instrumentRange = params.instrumentRange;
  const files = params.files;
  const instrumentName = params.instrumentName;
  const roundRobin = params.extra && params.extra.roundRobin ? params.extra.roundRobin : null;

  // Determine which regex to use.
  let regexStr;
  if (roundRobin) {
    regexStr = roundRobin.rrRegex;
  } else {
    regexStr = group.fileRegex;
  }
  const sampleRegex = buildRegex(regexStr);
  const matchingSamples = getMatchingSamples(files, sampleRegex);

  // Determine the desired key range.
  let desiredKeys = instrumentRange.slice();
  const isLegato = (group.type === "LEGATO" || group.type === "VELOCITY_LEGATO");
  if (!isLegato) {
    if (group.legatoSemitones < 0) {
      desiredKeys = desiredKeys.slice(0, desiredKeys.length - 1);
    } else if (group.legatoSemitones > 0) {
      desiredKeys = desiredKeys.slice(1);
    }
  }

  const regionLines = [];
  const isPermutation = group.type.indexOf("PERMUTATION") >= 0;

  if (isLegato) {
    // For LEGATO and VELOCITY_LEGATO, each matching sample becomes its own region,
    // with lokey, hikey, and pitch_keycenter all set to the "to" note (sample.note),
    // and sw_previous set to the "from" note.
    matchingSamples.forEach(sample => {
      const regionProps = {
        sample: `samples/${sample.fileName}`,
        pitch_keycenter: sample.note,
        lokey: sample.note,
        hikey: sample.note
      };
      if (roundRobin && roundRobin.seq_position !== undefined) {
        regionProps.seq_position = roundRobin.seq_position;
      }
      if (sample.from) {
        regionProps.sw_previous = sample.from;
      }
      regionLines.push("<region> " + buildPropertiesLine(regionProps, false));
    });
  } else if (isPermutation) {
    // Permutation branch (unchanged)
    const groupsByNote = {};
    matchingSamples.forEach(sample => {
      if (!groupsByNote[sample.note]) {
        groupsByNote[sample.note] = [];
      }
      groupsByNote[sample.note].push(sample);
    });
    desiredKeys.forEach(key => {
      let samplesForKey = groupsByNote[key];
      if (!samplesForKey) {
        const sample = chooseSampleForKey(key, matchingSamples);
        if (sample) {
          samplesForKey = [sample];
        }
      }
      if (samplesForKey) {
        samplesForKey.forEach(sample => {
          let region = `<region> sample=samples/${sample.fileName} pitch_keycenter=${sample.note} lokey=${key} hikey=${key}`;
          const keyIndex = desiredKeys.indexOf(key);
          if (sample.from) {
            region += ` sw_previous=${sample.from}`;
          } else if (keyIndex < desiredKeys.length - 1) {
            region += ` sw_previous=${desiredKeys[keyIndex + 1]}`;
          }
          regionLines.push(region);
        });
      }
    });
  } else {
    // For non-permutation groups, group contiguous keys that choose the same sample.
    let grouped = [];
    let currentBlock = null;
    for (let key of desiredKeys) {
      let sample = chooseSampleForKey(key, matchingSamples);
      if (!sample) continue;
      // If no current block, start one.
      if (currentBlock === null) {
        currentBlock = { sample: sample, start: key, end: key };
        if (roundRobin && roundRobin.seq_position !== undefined) {
          currentBlock.seq_position = roundRobin.seq_position;
        }
        if (group.type === "LEGATO" || group.type === "VELOCITY_LEGATO") {
          if (sample.from) {
            currentBlock.sw_previous = sample.from;
          } else if (group.legatoSemitones) {
            currentBlock.sw_previous = transposeNote(key, -group.legatoSemitones);
          }
        }
      } else {
        // If the same sample (by fileName) is chosen, extend the block.
        if (sample.fileName === currentBlock.sample.fileName) {
          currentBlock.end = key;
        } else {
          grouped.push(currentBlock);
          currentBlock = { sample: sample, start: key, end: key };
          if (roundRobin && roundRobin.seq_position !== undefined) {
            currentBlock.seq_position = roundRobin.seq_position;
          }
          if (group.type === "LEGATO" || group.type === "VELOCITY_LEGATO") {
            if (sample.from) {
              currentBlock.sw_previous = sample.from;
            } else if (group.legatoSemitones) {
              currentBlock.sw_previous = transposeNote(key, -group.legatoSemitones);
            }
          }
        }
      }
    }
    if (currentBlock !== null) {
      grouped.push(currentBlock);
    }
    // Now output one region per block.
    grouped.forEach(block => {
      let regionProps = {};
      regionProps.sample = `samples/${block.sample.fileName}`;
      regionProps.pitch_keycenter = block.sample.note;
      // For non-legato groups, lokey and hikey are determined by the block range.
      regionProps.lokey = block.start;
      regionProps.hikey = block.end;
      if (block.seq_position !== undefined) {
        regionProps.seq_position = block.seq_position;
      }
      if (block.sw_previous !== undefined) {
        regionProps.sw_previous = block.sw_previous;
      }
      const regionLine = "<region> " + buildPropertiesLine(regionProps, false);
      regionLines.push(regionLine);
    });
  }

  // Build the group header properties.
  const headerProps = {};
  const allowed = [
    "trigger",
    "group",
    "note_polyphony",
    "off_by",
    "off_mode",
    "loop_mode",
    "seq_length",
    "lovel",
    "hivel",
    "volume",
    "offset"
  ];
  allowed.forEach(key => {
    if (group[key] !== undefined) headerProps[key] = group[key];
  });
  // Defaults based on type.
  if (group.type === "SUSTAIN" || group.type === "VELOCITY_SUSTAIN") {
    if (headerProps.loop_mode === undefined) headerProps.loop_mode = "loop_continuous";
    if (headerProps.ampeg_release === undefined && group.ampeg_release === undefined) {
      headerProps.ampeg_release = 0.7;
    }
  }
  if (group.type === "LEGATO" || group.type === "VELOCITY_LEGATO") {
    if (headerProps.off_mode === undefined) headerProps.off_mode = "normal";
    if (group.volume === undefined) headerProps.volume = -8;
    if (group.ampeg_attack === undefined) headerProps.ampeg_attack = 0.1;
    if (group.ampeg_decay === undefined) headerProps.ampeg_decay = 0.2;
    if (group.ampeg_hold === undefined) headerProps.ampeg_hold = 0.25;
    if (group.ampeg_sustain === undefined) headerProps.ampeg_sustain = 0;
    if (group.ampeg_release === undefined) headerProps.ampeg_release = 1;
    if (group.ampeg_decay_shape === undefined) headerProps.ampeg_decay_shape = -1.4;
  }
  if (group.type === "POST-LEGATO" || group.type === "VELOCITY_POST-LEGATO") {
    if (headerProps.off_mode === undefined) headerProps.off_mode = "normal";
    if (group.ampeg_attack === undefined) headerProps.ampeg_attack = 0.3;
    if (group.ampeg_release === undefined) headerProps.ampeg_release = 1;
    if (group.ampeg_attack_shape === undefined) headerProps.ampeg_attack_shape = 3.8;
  }
  if (group.type === "RELEASE" || group.type === "VELOCITY_RELEASE") {
    if (headerProps.off_mode === undefined) headerProps.off_mode = "normal";
    if (headerProps.volume === undefined || headerProps.volume === 0) headerProps.volume = -2;
  }
  if (roundRobin && group.seq_length !== undefined) {
    headerProps.seq_length = group.seq_length;
  }

  const comment = buildSectionComment(instrumentName, group.type, group.name);

  return {
    comment,
    headerProps,
    regions: regionLines,
    crossfadeOverlap: group.crossfadeOverlap || 0
  };
}

// ─────────────────────────────────────────────────────────────
// Main program
function main() {
  if (process.argv.length < 5) {
    console.error("Usage: node sfz-generator.js <definition.json> <inputFolder> <outputFolder>");
    process.exit(1);
  }
  const defFile = process.argv[2];
  const inputFolder = process.argv[3];
  const outputFolder = process.argv[4];

  let defContent;
  try {
    defContent = fs.readFileSync(defFile, "utf8");
  } catch (err) {
    console.error("Error reading definition file:", err);
    process.exit(1);
  }
  let definition;
  try {
    definition = JSON.parse(removeComments(defContent));
  } catch (err) {
    console.error("Error parsing definition file:", err);
    process.exit(1);
  }

  const instrumentName = definition.instrumentName;
  const lowNote = definition.lowNote;
  const highNote = definition.highNote;
  if (!instrumentName || !lowNote || !highNote) {
    console.error("Definition file must specify instrumentName, lowNote, and highNote.");
    process.exit(1);
  }
  const fullRange = getNoteRange(lowNote, highNote);

  let inputFiles;
  try {
    inputFiles = fs.readdirSync(inputFolder);
  } catch (err) {
    console.error("Error reading input folder:", err);
    process.exit(1);
  }

  const sections = [];
  const velocityGroups = [];

  definition.noteFiles.groups.forEach(group => {
    if (group.type.indexOf("VELOCITY_") === 0 && Array.isArray(group.roundRobins)) {
      let allRegions = [];
      group.roundRobins.forEach(rr => {
        const section = processGroup({
          group,
          instrumentRange: fullRange,
          files: inputFiles,
          instrumentName,
          extra: { roundRobin: rr }
        });
        allRegions = allRegions.concat(section.regions);
      });
      const baseSection = processGroup({
        group,
        instrumentRange: fullRange,
        files: inputFiles,
        instrumentName
      });
      baseSection.regions = allRegions;
      sections.push(baseSection);
      velocityGroups.push(baseSection);
    } else {
      const section = processGroup({
        group,
        instrumentRange: fullRange,
        files: inputFiles,
        instrumentName
      });
      sections.push(section);
      if (group.type.indexOf("VELOCITY_") === 0 && group.type.indexOf("LEGATO") < 0 && group.type.indexOf("RELEASE") < 0) {
        velocityGroups.push(section);
      }
    }
  });

  // Adjust velocity groups to add crossfade parameters.
  for (let i = 0; i < velocityGroups.length; i++) {
    const sec = velocityGroups[i];
    const hivel = parseInt(sec.headerProps.hivel, 10);
    const overlap = parseInt(sec.crossfadeOverlap, 10);
    if (i > 0) {
      const prevSec = velocityGroups[i - 1];
      const prevHivel = parseInt(prevSec.headerProps.hivel, 10);
      sec.headerProps.xfin_lovel = prevHivel - (parseInt(prevSec.crossfadeOverlap,10) || 0);
      sec.headerProps.xfin_hivel = prevHivel;
    }
    if (i < velocityGroups.length - 1) {
      sec.headerProps.xfout_lovel = hivel - overlap;
      sec.headerProps.xfout_hivel = hivel;
    }
  }

  let outText = "";
  sections.forEach(sec => {
    outText += sec.comment;
    outText += "<group>\n    " + buildPropertiesLine(sec.headerProps) + "\n";
    sec.regions.forEach(r => {
      outText += r + "\n";
    });
    outText += "\n";
  });

  const outFileName = instrumentName.toLowerCase().replace(/\s+/g, "_") + ".sfz";
  const outPath = path.join(outputFolder, outFileName);
  try {
    fs.writeFileSync(outPath, outText, "utf8");
    console.log("SFZ file written to", outPath);
  } catch (err) {
    console.error("Error writing output file:", err);
    process.exit(1);
  }
}

main();
