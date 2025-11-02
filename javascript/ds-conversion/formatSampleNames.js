const fs = require('fs');
const path = require('path');
const glob = require('glob');
const { WaveFile } = require('wavefile');

// Convert note (like "C#1") to a MIDI number for sorting
function noteToMidi(note) {
  const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
  const match = note.match(/([A-G]#?)(\d+)/);
  if (!match) return null;
  const pitchClass = match[1];
  const octave = parseInt(match[2], 10);
  const noteIndex = noteNames.indexOf(pitchClass);
  if (noteIndex === -1) return null;
  return noteIndex + octave * 12;
}

// Use glob to scan for files matching the pattern
function scanWavFiles(pattern) {
  return new Promise((resolve, reject) => {
    try {
      const files = glob.sync(pattern, { nodir: true });
      resolve(files);
    } catch (err) {
      reject(err);
    }
  });
}

// Get loop points using the wavefile library.
// It expects that the WAV file contains a "smpl" chunk with loop data.
async function getLoopPoints(filePath) {
  try {
    const buffer = await fs.promises.readFile(filePath);
    let wav = new WaveFile(buffer);
    // Check if the file contains a 'smpl' chunk with loops.
    if (wav.smpl && wav.smpl.loops && wav.smpl.loops.length > 0) {
      let loop = wav.smpl.loops[0]; // use the first loop
      let loopStart = loop.start;
      let loopEnd = loop.end;
      return { loopStart, loopEnd };
    }
    return { loopStart: 0, loopEnd: 0 };
  } catch (error) {
    console.error(`Error reading WAV file ${filePath}:`, error);
    return { loopStart: 0, loopEnd: 0 };
  }
}

// Format a sample line for output in DecentSampler dspreset format
function formatSampleLine(filePath, note, loopStart, loopEnd) {
  const relativePath = path.relative(process.cwd(), filePath);
  return `<sample path="${relativePath}" rootNote="${note}" loNote="${note}" hiNote="${note}" loopStart=${loopStart} loopEnd=${loopEnd}/>`;
}

// Main function to process all WAV files matching the given pattern
async function processSamples(pattern) {
  try {
    const files = await scanWavFiles(pattern);
    const sampleData = [];

    for (let file of files) {
      const fileName = path.basename(file, '.wav');
      // Expect filenames ending with the note (e.g., "BP-L_oV_nA_sus_p_A#1")
      const match = fileName.match(/(.*?)([A-G]#?)(\d+)$/);
      if (match) {
        const note = match[2] + match[3];
        const midi = noteToMidi(note);
        if (midi === null) continue;
        
        const { loopStart, loopEnd } = await getLoopPoints(file);
        sampleData.push({ file, note, loopStart, loopEnd });
      } else {
        console.error(`Filename does not match expected pattern: ${fileName}`);
      }
    }

    // Sort by MIDI note number
    sampleData.sort((a, b) => noteToMidi(a.note) - noteToMidi(b.note));

    sampleData.forEach(sample => {
      console.log(formatSampleLine(sample.file, sample.note, sample.loopStart, sample.loopEnd));
    });
  } catch (err) {
    console.error('Error processing samples:', err);
  }
}

// Run the program with the provided wildcard path from the command line
const pattern = process.argv[2];
if (pattern) {
  processSamples(pattern);
} else {
  console.error('Please provide a path with wildcards as a command-line argument.');
}
