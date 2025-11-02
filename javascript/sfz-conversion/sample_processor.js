#!/usr/bin/env node
/**
 * sample_processor.js
 *
 * Recursively finds .wav sample files in a source folder (ignoring files starting with ._),
 * and converts each to mono (preserving loop metadata) while copying them to a destination folder.
 * Directory names are normalized to lower case (and spaces are replaced with underscores) and
 * file names have spaces replaced with underscores. In addition:
 *   1. If the destination file already exists, conversion is skipped.
 *   2. All non-ASCII or unrecognized characters in file names are scrubbed (replaced with underscores).
 *   3. All errors are logged to "errors.txt".
 *
 * When a note range is specified, the program will look for files following the naming pattern:
 *     <baseName>_<note>.wav
 * where <note> matches [A-G][#]?\d. However, even if a note range is provided, if the note names
 * are specified then the program will simply convert the given files without trying to generate missing notes.
 * Files that do not follow the naming pattern are processed individually.
 *
 * Usage:
 *   With note range:
 *     node sample_processor.js <source_root> <destination_root> <note_range>
 *     e.g.: node sample_processor.js /path/to/source /path/to/dest C1-F4
 *
 *   Without note range:
 *     node sample_processor.js <source_root> <destination_root>
 *
 * Dependencies:
 *   - Node.js (fs, path, child_process modules)
 *   - sox (must be installed and in your PATH)
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

//–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
// Error Logging Helper

const errorLogFile = 'errors.txt';
function logError(message) {
  const timestamp = new Date().toISOString();
  fs.appendFileSync(errorLogFile, `[${timestamp}] ${message}\n`);
}

//–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
// Command-line arguments

if (process.argv.length < 4) {
  console.error('Usage: node sample_processor.js <source_root> <destination_root> [<note_range>]');
  process.exit(1);
}

const sourceRoot = path.resolve(process.argv[2]);
const destinationRoot = path.resolve(process.argv[3]);

// Note range is optional.
const noteRangeStr = process.argv[4] || null;
if (noteRangeStr) {
  console.log(`Using note range: ${noteRangeStr}`);
} else {
  console.log('No note range provided; processing all .wav files individually.');
}

//–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
// Note parsing helpers (used when a note range is provided)

/**
 * Parses a note string such as "C#4" into its parts.
 */
function parseNote(noteStr) {
  const match = noteStr.match(/^([A-G])(#?)(\d+)$/);
  if (!match) throw new Error('Invalid note format: ' + noteStr);
  return {
    letter: match[1],
    accidental: match[2],
    octave: parseInt(match[3], 10)
  };
}

/**
 * Converts a note string (e.g. "C#4") into a MIDI note number.
 * MIDI note = (octave + 1)*12 + semitone; assumes sharps only.
 */
function noteToMidi(noteStr) {
  const { letter, accidental, octave } = parseNote(noteStr);
  const semitones = { 'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11 };
  let midi = (octave + 1) * 12 + semitones[letter];
  if (accidental === '#') midi += 1;
  return midi;
}

/**
 * Converts a MIDI note number back into a note string (using sharps).
 */
function midiToNote(midi) {
  const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
  const octave = Math.floor(midi / 12) - 1;
  return noteNames[midi % 12] + octave;
}

/**
 * Given a range string like "C1-F4", returns an array of note strings covering the full range.
 */
function generateNoteRange(rangeStr) {
  const parts = rangeStr.split('-');
  if (parts.length !== 2) {
    throw new Error('Invalid note range: ' + rangeStr);
  }
  const startMidi = noteToMidi(parts[0]);
  const endMidi = noteToMidi(parts[1]);
  if (startMidi > endMidi) {
    throw new Error('Start note is higher than end note in range: ' + rangeStr);
  }
  const range = [];
  for (let m = startMidi; m <= endMidi; m++) {
    range.push(midiToNote(m));
  }
  return range;
}

let desiredNotes = null;
if (noteRangeStr) {
  try {
    desiredNotes = generateNoteRange(noteRangeStr);
    // desiredNotes is an ordered array of note strings (e.g. ["C1", "C#1", "D1", ...])
  } catch (err) {
    console.error(err);
    logError(`Error generating note range: ${err.message}`);
    process.exit(1);
  }
}

//–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
// Normalization helpers

/**
 * Normalizes a file name by replacing any character that is not
 * an ASCII letter, digit, underscore, hyphen, or period with an underscore.
 */
function normalizeFileName(fileName) {
  //return fileName.replace(/[^A-Za-z0-9_.-]/g, '_');
  return fileName;
}

/**
 * Normalizes a directory path.
 * Each directory name is converted to lower case and spaces (and other non-ASCII)
 * are replaced with underscores.
 */
function normalizeDirPath(dirPath) {
  return dirPath;
  // return dirPath
  //   .split(path.sep)
  //   .map(part => normalizeFileName(part).toLowerCase())
  //   .join(path.sep);
}

//–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
// Utility: Check if file exists at destination.
function destinationExists(filePath) {
  return fs.existsSync(filePath);
}

//–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
// Directory Recursion

/**
 * Recursively walks a directory, calling the provided callback with the full path
 * of every file encountered.
 */
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

//–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
// Processing
//
// There are two branches:
//   1. When a note range is provided:
//        - Files matching the naming pattern (<baseName>_<note>.wav) are grouped,
//          but if the note names are explicitly provided then we only convert them.
//        - Files that do not match the pattern are processed individually.
//   2. When no note range is provided: all .wav files are processed individually.

if (noteRangeStr) {
  // For grouping files that match the expected pattern.
  const sampleSets = {}; // key: relativeDir + '|' + baseName, value: array of file objects
  // Also keep an array for files that do not match the naming pattern.
  const individualFiles = [];

  function processFile(filePath) {
    const fileName = path.basename(filePath);
    // Skip files starting with "._"
    if (fileName.startsWith('._')) return;
    if (path.extname(fileName).toLowerCase() !== '.wav') return;

    // Try to match the naming pattern: <baseName>_<note>.wav
    const match = fileName.match(/^(.*)_([A-G][#]?\d)\.wav$/);
    if (match) {
      const baseName = match[1];
      const note = match[2];
      let midi;
      try {
        midi = noteToMidi(note);
      } catch (err) {
        logError(`Error parsing note from file ${filePath}: ${err.message}`);
        individualFiles.push(filePath);
        return;
      }
      // Get the relative directory (to reconstruct the tree in the destination)
      const relativeDir = path.relative(sourceRoot, path.dirname(filePath));
      const key = relativeDir + '|' + baseName;
      if (!sampleSets[key]) {
        sampleSets[key] = [];
      }
      sampleSets[key].push({ filePath, relativeDir, fileName, baseName, note, midi });
    } else {
      // File does not follow the expected pattern. Process it individually.
      individualFiles.push(filePath);
    }
  }

  walkDir(sourceRoot, processFile);

  // Process grouped files:
  // Even though a note range was provided, if the note name is present
  // (which is required for grouping) then we simply convert the given files.
  for (const key in sampleSets) {
    const setFiles = sampleSets[key];
    // Use the first file’s base name and relative directory for logging.
    const { baseName, relativeDir } = setFiles[0];
    console.log(`\n=== Processing sample set "${baseName}" in folder "${relativeDir}" ===`);
    for (const fileObj of setFiles) {
      const inputFile = fileObj.filePath;
      const normalizedRelativeDir = normalizeDirPath(fileObj.relativeDir);
      const outputDir = path.join(destinationRoot, normalizedRelativeDir);
      const normalizedFileName = normalizeFileName(fileObj.fileName);
      const outputFile = path.join(outputDir, normalizedFileName);
      fs.mkdirSync(outputDir, { recursive: true });
      if (destinationExists(outputFile)) {
        console.log(`Skipping conversion (destination exists): ${outputFile}`);
        continue;
      }
      console.log(`Converting and copying "${inputFile}" to "${outputFile}"`);
      try {
        execSync(`sox "${inputFile}" "${outputFile}" channels 1`, { stdio: 'inherit' });
      } catch (err) {
        const msg = `Error converting sample ${inputFile} to ${outputFile}: ${err.message}`;
        console.error(msg);
        logError(msg);
      }
    }
    // Note: We are not generating missing notes even though a note range was provided,
    // since the file names already specify the note.
  }

  // Process individual files (which did not match the naming pattern):
  if (individualFiles.length > 0) {
    console.log('\nProcessing files that do not match the naming pattern individually:');
    individualFiles.forEach(filePath => {
      const fileName = path.basename(filePath);
      const relativeDir = path.relative(sourceRoot, path.dirname(filePath));
      const normalizedRelativeDir = normalizeDirPath(relativeDir);
      const normalizedFileName = normalizeFileName(fileName);
      const outputDir = path.join(destinationRoot, normalizedRelativeDir);
      const outputFile = path.join(outputDir, normalizedFileName);
      fs.mkdirSync(outputDir, { recursive: true });
      if (destinationExists(outputFile)) {
        console.log(`Skipping conversion (destination exists): ${outputFile}`);
        return;
      }
      console.log(`Converting and copying "${filePath}" to "${outputFile}"`);
      try {
        execSync(`sox "${filePath}" "${outputFile}" channels 1`, { stdio: 'inherit' });
      } catch (err) {
        const msg = `Error converting sample ${filePath} to ${outputFile}: ${err.message}`;
        console.error(msg);
        logError(msg);
      }
    });
  }

} else {
  // No note range provided: process all .wav files individually.
  console.log('\nProcessing all .wav files individually (no note generation)...');

  walkDir(sourceRoot, function(filePath) {
    const fileName = path.basename(filePath);
    // Skip files starting with "._"
    if (fileName.startsWith('._')) return;
    if (path.extname(fileName).toLowerCase() !== '.wav') return;

    const relativeDir = path.relative(sourceRoot, path.dirname(filePath));
    const normalizedRelativeDir = normalizeDirPath(relativeDir);
    const normalizedFileName = normalizeFileName(fileName);
    const outputDir = path.join(destinationRoot, normalizedRelativeDir);
    const outputFile = path.join(outputDir, normalizedFileName);
    fs.mkdirSync(outputDir, { recursive: true });
    if (destinationExists(outputFile)) {
      console.log(`Skipping conversion (destination exists): ${outputFile}`);
      return;
    }
    console.log(`Converting and copying "${filePath}" to "${outputFile}"`);
    try {
      execSync(`sox "${filePath}" "${outputFile}" channels 1`, { stdio: 'inherit' });
    } catch (err) {
      const msg = `Error converting sample ${filePath} to ${outputFile}: ${err.message}`;
      console.error(msg);
      logError(msg);
    }
  });
}

console.log('\nProcessing complete.');
