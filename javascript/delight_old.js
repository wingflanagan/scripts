#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const PNG = require('pngjs').PNG;
const jpeg = require('jpeg-js');
const cliProgress = require('cli-progress');

// Function to parse command-line arguments
function parseArgs() {
    const args = process.argv.slice(2);
    if (args.length !== 5) {
        console.error('Usage: node remove_lighting.js <source_file> <target_folder> <blur_radius> <epsilon> <iterations>');
        process.exit(1);
    }
    const sourceFile = args[0];
    const targetFolder = args[1];
    const blurRadius = parseInt(args[2], 10);
    const epsilon = parseFloat(args[3]);
    const iterations = parseInt(args[4], 10);

    if (!fs.existsSync(sourceFile)) {
        console.error(`Source file does not exist: ${sourceFile}`);
        process.exit(1);
    }

    if (!fs.existsSync(targetFolder)) {
        console.error(`Target folder does not exist: ${targetFolder}`);
        process.exit(1);
    }

    if (isNaN(blurRadius) || blurRadius <= 0) {
        console.error('Blur radius must be a positive integer.');
        process.exit(1);
    }

    if (isNaN(epsilon) || epsilon <= 0) {
        console.error('Epsilon must be a positive number.');
        process.exit(1);
    }

    if (isNaN(iterations) || iterations <= 0) {
        console.error('Iterations must be a positive integer.');
        process.exit(1);
    }

    return { sourceFile, targetFolder, blurRadius, epsilon, iterations };
}

// Function to apply box blur to a grayscale image
function boxBlurGray(data, width, height, radius) {
    const output = new Float32Array(data.length);
    const kernelSize = 2 * radius + 1;

    // Horizontal blur
    for (let y = 0; y < height; y++) {
        let sum = 0;
        for (let x = -radius; x <= radius; x++) {
            const idx = y * width + Math.max(0, Math.min(width - 1, x));
            sum += data[idx];
        }
        for (let x = 0; x < width; x++) {
            const idx = y * width + x;

            if (x - radius - 1 >= 0) {
                sum -= data[y * width + x - radius - 1];
            }
            if (x + radius < width) {
                sum += data[y * width + x + radius];
            }

            output[idx] = sum / kernelSize;
        }
    }

    // Vertical blur
    const temp = new Float32Array(output.length);
    for (let x = 0; x < width; x++) {
        let sum = 0;
        for (let y = -radius; y <= radius; y++) {
            const idx = Math.max(0, Math.min(height - 1, y)) * width + x;
            sum += output[idx];
        }
        for (let y = 0; y < height; y++) {
            const idx = y * width + x;

            if (y - radius - 1 >= 0) {
                sum -= output[(y - radius - 1) * width + x];
            }
            if (y + radius < height) {
                sum += output[(y + radius) * width + x];
            }

            temp[idx] = sum / kernelSize;
        }
    }

    return temp;
}

// Main processing function
function processImage({ sourceFile, targetFolder, blurRadius, epsilon, iterations }) {
    const ext = path.extname(sourceFile).toLowerCase();
    const fileName = path.basename(sourceFile, ext);
    const outputFileName = `${fileName}_de-lit${ext}`;
    const outputPath = path.join(targetFolder, outputFileName);

    const imageData = fs.readFileSync(sourceFile);
    let image;
    let isPNG = false;

    // Read image data
    if (ext === '.png') {
        image = PNG.sync.read(imageData);
        isPNG = true;
    } else if (ext === '.jpg' || ext === '.jpeg') {
        image = jpeg.decode(imageData);
    } else {
        console.error('Unsupported image format. Please use PNG or JPEG.');
        process.exit(1);
    }

    const { width, height } = image;
    let data = new Float32Array(image.data.length);

    // Copy image data to Float32Array for precise computations
    for (let i = 0; i < image.data.length; i++) {
        data[i] = image.data[i];
    }

    // Initialize progress bar
    const totalSteps = iterations * 4;
    const progressBar = new cliProgress.SingleBar({
        format: 'Processing [{bar}] {percentage}% | Iteration {iteration}/{iterations}',
        barCompleteChar: '#',
        barIncompleteChar: '-',
        hideCursor: true,
    });
    progressBar.start(totalSteps, 0, { iteration: 1, iterations });

    // Perform multiple iterations
    for (let iter = 0; iter < iterations; iter++) {
        // Prepare arrays
        const numPixels = width * height;
        const luminance = new Float32Array(numPixels);

        // Step 1: Compute luminance
        for (let i = 0; i < numPixels; i++) {
            const idx = i * 4;
            const r = data[idx] / 255;
            const g = data[idx + 1] / 255;
            const b = data[idx + 2] / 255;

            // Compute luminance
            luminance[i] = 0.299 * r + 0.587 * g + 0.114 * b;
        }
        progressBar.update(iter * 4 + 1, { iteration: iter + 1 });

        // Step 2: Estimate illumination by blurring luminance
        const illumination = boxBlurGray(luminance, width, height, blurRadius);
        progressBar.update(iter * 4 + 2, { iteration: iter + 1 });

        // Step 3: Normalize the image
        // Find average illumination to maintain overall brightness
        let totalIllumination = 0;
        for (let i = 0; i < numPixels; i++) {
            totalIllumination += illumination[i];
        }
        const avgIllumination = totalIllumination / numPixels;

        for (let i = 0; i < numPixels; i++) {
            const idx = i * 4;
            const r = data[idx] / 255;
            const g = data[idx + 1] / 255;
            const b = data[idx + 2] / 255;

            const illum = illumination[i] + epsilon;

            // Normalize RGB values
            let newR = (r / illum) * avgIllumination;
            let newG = (g / illum) * avgIllumination;
            let newB = (b / illum) * avgIllumination;

            // Clamp to [0,1]
            newR = Math.min(1, Math.max(0, newR));
            newG = Math.min(1, Math.max(0, newG));
            newB = Math.min(1, Math.max(0, newB));

            data[idx] = newR * 255;
            data[idx + 1] = newG * 255;
            data[idx + 2] = newB * 255;
            // Alpha channel remains unchanged
        }
        progressBar.update(iter * 4 + 3, { iteration: iter + 1 });

        // Optional: Adjust parameters between iterations if needed
        // For example, increase blurRadius or adjust epsilon
        progressBar.update(iter * 4 + 4, { iteration: iter + 1 });
    }

    progressBar.stop();

    // Convert data back to Uint8Array for saving
    const outputData = Buffer.alloc(data.length);
    for (let i = 0; i < data.length; i++) {
        outputData[i] = Math.round(Math.min(255, Math.max(0, data[i])));
    }

    // Write output image
    let outputBuffer;
    if (isPNG) {
        const outputImage = new PNG({ width, height });
        outputImage.data = outputData;
        outputBuffer = PNG.sync.write(outputImage);
    } else {
        const outputImageData = { data: outputData, width, height };
        outputBuffer = jpeg.encode(outputImageData, 100).data;
    }

    fs.writeFileSync(outputPath, outputBuffer);
    console.log(`Processed image saved to: ${outputPath}`);
}

// Run the script
const args = parseArgs();
processImage(args);

