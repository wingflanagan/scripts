#!/usr/bin/env node
/**
 * pitchFill.js - Improved Version
 *
 * - Scans a source folder for .wav files that follow the naming convention:
 *     <baseName>_<note>.wav
 * - Fills in missing notes within the specified range (e.g., "C1-F4").
 * - Leaves original files untouched and generates new **stereo** samples.
 * - Fixes illegal characters in filenames by replacing them with "_".
 * - Skips files if the target file already exists.
 * - Logs all errors to "errors.txt".
 *
 * Usage:
 *   node pitchFill.js <source_folder> <note_range>
 * Example:
 *   node pitchFill.js /path/to/samples "C1-F4"
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ERROR_LOG_FILE = 'errors.txt';

//–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
// Command-line Arguments

if (process.argv.length < 4) {
  console.error('Usage: node pitchFill.js <source_folder> <note_range>');
  process.exit(1);
}

const sourceFolder = path.resolve(process.argv[2]);
const noteRangeStr = process.argv[3];

//–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
// Error Logging Function

function logError(message) {
  console.error(message); // Show in console
  fs.appendFileSync(ERROR_LOG_FILE, message + '\n'); // Append to error log
}

//–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
// Note Helper Functions

function parseNote(noteStr) {
  const match = noteStr.match(/^([A-G])(#?)(\d+)$/);
  if (!match) throw new Error('Invalid note format: ' + noteStr);
  return { letter: match[1], accidental: match[2], octave: parseInt(match[3], 10) };
}

function noteToMidi(noteStr) {
  const { letter, accidental, octave } = parseNote(noteStr);
  const semitones = { 'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11 };
  let midi = (octave + 1) * 12 + semitones[letter];
  if (accidental === '#') midi += 1;
  return midi;
}

function midiToNote(midi) {
  const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
  const octave = Math.floor(midi / 12) - 1;
  return noteNames[midi % 12] + octave;
}

function generateNoteRange(rangeStr) {
  const parts = rangeStr.split('-');
  if (parts.length !== 2) throw new Error('Invalid note range: ' + rangeStr);
  const startMidi = noteToMidi(parts[0]);
  const endMidi = noteToMidi(parts[1]);
  if (startMidi > endMidi) throw new Error('Start note is higher than end note in range.');
  return Array.from({ length: endMidi - startMidi + 1 }, (_, i) => midiToNote(startMidi + i));
}

const desiredNotes = generateNoteRange(noteRangeStr);

//–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
// File Helpers

function walkDir(dir, callback) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkDir(fullPath, callback);
    } else {
      callback(fullPath);
    }
  }
}

function sanitizeFileName(name) {
  return name.replace(/[^a-zA-Z0-9._-]/g, '_'); // Replace non-ASCII chars with "_"
}

function getSafeFilePath(folder, baseName, note) {
  let safeBaseName = sanitizeFileName(baseName);
  let filePath = path.join(folder, `${safeBaseName}_${note}.wav`);
  let counter = 1;
  while (fs.existsSync(filePath)) {
    logError(`File already exists: ${filePath}. Skipping.`);
    return null;
  }
  return filePath;
}

//–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
// Group .wav Files into Sample Sets

const sampleSets = {};

function processFile(filePath) {
  const fileName = path.basename(filePath);
  if (fileName.startsWith('._')) return;
  if (path.extname(fileName).toLowerCase() !== '.wav') return;

  const match = fileName.match(/^(.*)_([A-G][#]?\d)\.wav$/);
  if (!match) {
    logError(`Skipping file (naming mismatch): ${filePath}`);
    return;
  }
  const baseName = match[1];
  const note = match[2];
  const midi = noteToMidi(note);
  const relativeFolder = path.relative(sourceFolder, path.dirname(filePath));
  const key = relativeFolder + '|' + baseName;
  if (!sampleSets[key]) sampleSets[key] = [];
  sampleSets[key].push({ filePath, folder: path.dirname(filePath), baseName, note, midi });
}

walkDir(sourceFolder, processFile);

//–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
// Process Each Sample Set

for (const key in sampleSets) {
  const setFiles = sampleSets[key];
  if (setFiles.length === 0) continue;

  const { baseName } = setFiles[0];
  const availableNotes = {};
  for (const info of setFiles) availableNotes[info.note] = info;

  console.log(`\nProcessing sample set "${baseName}" in folder "${setFiles[0].folder}"`);

  for (const note of desiredNotes) {
    if (availableNotes[note]) continue;

    const targetMidi = noteToMidi(note);
    let nearest = null;
    let smallestDiff = Infinity;
    for (const availNote in availableNotes) {
      const availMidi = noteToMidi(availNote);
      const diff = Math.abs(availMidi - targetMidi);
      if (diff < smallestDiff) {
        smallestDiff = diff;
        nearest = availableNotes[availNote];
      }
    }
    if (!nearest) {
      logError(`No available sample to generate note ${note}`);
      continue;
    }

    const shiftCents = (targetMidi - nearest.midi) * 100;
    const inputFile = nearest.filePath;
    const folder = nearest.folder;
    const outputFile = getSafeFilePath(folder, baseName, note);
    if (!outputFile) continue;

    console.log(`Generating missing note ${note} from ${nearest.note} (${shiftCents} cents shift)`);
    try {
      // Get the number of channels in the input file using SoX
      const channelCount = parseInt(execSync(`sox --i -c "${inputFile}"`).toString().trim(), 10);
      if (isNaN(channelCount)) throw new Error(`Unable to determine channel count for ${inputFile}`);

      // Use same channel count in output
      execSync(`sox "${inputFile}" "${outputFile}" pitch ${shiftCents} channels ${channelCount}`, { stdio: 'inherit' });
    } catch (err) {
      logError(`Error generating ${note} from ${nearest.note}: ${err}`);
    }
  }
}

console.log('\nPitch fill processing complete.');
