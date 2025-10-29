const fs = require('fs');
const path = require('path');

function processInstrument(instrument) {
  const newInstrument = { Name: instrument.Name };

  if (instrument.Regions && instrument.Regions.length > 0) {
    const processedRegions = instrument.Regions
      .map(region => {
        // Skip regions with empty Sample
        if (region.Sample === "") return null;

        // Process dimension regions
        const validDimRegions = region.DimensionRegions
          .filter(dr => dr.Sample !== "")
          .map(dr => ({
            Sample: dr.Sample,
            Gain: dr.Gain || "0dB",
            SampleStartOffset: dr.SampleStartOffset || 0,
            VelocityUpperLimit: dr.VelocityUpperLimit || 0
          }));

        // Skip regions with no valid dimension regions
        if (validDimRegions.length === 0) return null;

        return {
          Sample: region.Sample,
          KeyRange: region.KeyRange,
          VelocityRange: region.VelocityRange,
          Layers: region.Layers,
          Loops: region.Loops,
          DimensionRegions: validDimRegions
        };
      })
      .filter(region => region !== null);

    if (processedRegions.length > 0) {
      newInstrument.Regions = processedRegions;
    }
  }

  return newInstrument;
}

function processFile(filePath) {
  try {
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    const inputData = JSON.parse(fileContent);

    // Check if the JSON has an "Instruments" root element
    if (!inputData || !inputData.Instruments) {
      console.log(`Skipping file (missing "Instruments" element): ${filePath}`);
      return;
    }

    // Process the instruments
    const outputData = {
      Instruments: inputData.Instruments.map(processInstrument)
    };

    // Build output file name by inserting "_reduced" before the extension
    const dir = path.dirname(filePath);
    const ext = path.extname(filePath);
    const baseName = path.basename(filePath, ext);
    const outputFileName = `${baseName}_reduced${ext}`;
    const outputPath = path.join(dir, outputFileName);

    fs.writeFileSync(outputPath, JSON.stringify(outputData, null, 2));
    console.log(`Processed JSON saved to ${outputPath}`);
  } catch (error) {
    console.error(`Error processing file ${filePath}:`, error.message);
  }
}

function processDirectory(directoryPath) {
  // Read all entries (files and subdirectories) in the directory
  const entries = fs.readdirSync(directoryPath);
  entries.forEach(entry => {
    const fullPath = path.join(directoryPath, entry);
    const stats = fs.statSync(fullPath);

    if (stats.isDirectory()) {
      // Recursively process sub-folders
      processDirectory(fullPath);
    } else if (stats.isFile() && path.extname(entry).toLowerCase() === '.json') {
      processFile(fullPath);
    }
  });
}

// Run with command line argument: node script.js <rootFolder>
const [rootFolder] = process.argv.slice(2);
if (!rootFolder) {
  console.error('Usage: node script.js <rootFolder>');
  process.exit(1);
}

processDirectory(rootFolder);
