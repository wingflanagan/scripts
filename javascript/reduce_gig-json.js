const fs = require('fs');

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

function main(inputPath, outputPath) {
    const inputData = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));
    const outputData = {
        Instruments: inputData.Instruments.map(processInstrument)
    };
    fs.writeFileSync(outputPath, JSON.stringify(outputData, null, 2));
}

// Run with command line arguments
const [inputFile, outputFile] = process.argv.slice(2);
if (!inputFile || !outputFile) {
    console.error('Usage: node script.js <input.json> <output.json>');
    process.exit(1);
}

main(inputFile, outputFile);
console.log(`Processed JSON saved to ${outputFile}`);