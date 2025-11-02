const WaveFile = require('wavefile').WaveFile;
const fs = require('fs');
const path = require('path');

function processWavFile(filePath) {
    try {
        const buffer = fs.readFileSync(filePath);
        let wav;
        try {
            wav = new WaveFile(buffer);
        } catch (e) {
            console.error(`Error parsing ${filePath}: ${e.message}`);
            return;
        }

        // Access chunks safely
        const chunks = wav.chunks || [];
        const smplChunk = chunks.find(c => c.id === 'smpl');
        
        if (!smplChunk?.data?.loops?.length) {
            console.log(`No valid loops found in ${filePath}, skipping.`);
            return;
        }

        // Get loop metadata
        const loopEnd = smplChunk.data.loops[0].end;
        const numChannels = wav.fmt.numChannels;
        const bytesPerSample = wav.fmt.bitsPerSample / 8;

        // Find data chunk
        const dataChunk = chunks.find(c => c.id === 'data');
        if (!dataChunk) {
            console.log(`No audio data in ${filePath}, skipping.`);
            return;
        }

        // Calculate byte positions
        const byteStart = loopEnd * numChannels * bytesPerSample;
        const releaseData = dataChunk.chunkData.subarray(byteStart);
        
        if (releaseData.length === 0) {
            console.log(`No release data in ${filePath}, skipping.`);
            return;
        }

        // Create new WAV file
        const releaseWav = new WaveFile();
        releaseWav.fromScratch(
            wav.fmt.numChannels,
            wav.fmt.sampleRate,
            wav.fmt.bitsPerSample,
            wav.fmt.audioFormat,
            releaseData
        );

        // Remove all non-essential chunks
        ['smpl', 'cue', 'LIST'].forEach(chunk => {
            if (releaseWav[chunk]) releaseWav.deleteChunk(chunk);
        });

        // Save output
        const newPath = path.format({
            dir: path.dirname(filePath),
            name: path.basename(filePath, '.wav') + '_release',
            ext: '.wav'
        });

        fs.writeFileSync(newPath, releaseWav.toBuffer());
        console.log(`Created: ${newPath}`);

    } catch (e) {
        console.error(`Error processing ${filePath}: ${e.message}`);
    }
}

// Main execution
const folder = process.argv[2];
if (!folder) {
    console.error('Usage: node extract-release.js <folder>');
    process.exit(1);
}

fs.readdirSync(folder)
    .filter(f => f.toLowerCase().endsWith('.wav'))
    .forEach(f => processWavFile(path.join(folder, f)));