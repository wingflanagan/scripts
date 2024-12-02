// delight.js

const cv = require('opencv4nodejs');
const path = require('path');

// Get the input and output paths from command-line arguments
const args = process.argv.slice(2);

if (args.length < 2) {
    console.log('Usage: node delight.js <inputImagePath> <outputImagePath>');
    process.exit(1);
}

const inputImagePath = args[0];
const outputImagePath = args[1];

try {
    // Read the input image
    const image = cv.imread(inputImagePath);

    // Convert to LAB color space
    const labImage = image.cvtColor(cv.COLOR_BGR2Lab);

    // Split the LAB image into separate channels
    let labChannels = labImage.split();
    const lChannel = labChannels[0];

    // Apply CLAHE to the L-channel to even out lighting
    const clahe = new cv.CLAHE(2.0, new cv.Size(8,8));
    const cl = clahe.apply(lChannel);

    // Merge the CLAHE enhanced L-channel back with A and B channels
    labChannels[0] = cl;
    const mergedLab = new cv.Mat();
    cv.merge(labChannels, mergedLab);

    // Convert back to BGR color space
    const finalImage = mergedLab.cvtColor(cv.COLOR_Lab2BGR);

    // Save the output image
    cv.imwrite(outputImagePath, finalImage);

    console.log('Processing completed. Output saved to', outputImagePath);
} catch (err) {
    console.error('Error processing image:', err);
}
