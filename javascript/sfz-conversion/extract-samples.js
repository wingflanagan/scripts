#!/usr/bin/env node
/**
 * extract-samples.js - Improved Version
 *
 * Usage:
 *   node extract-samples.js /path/to/source /path/to/destination
 *
 * Recursively walks the source directory, reproducing its folder structure in the destination.
 * For each .gig file found, it creates a folder (named after the file without its extension) in the
 * corresponding destination directory. Within that folder, it creates a "samples" subfolder and uses
 * `gigextract` (from the gigtools package) to extract sample .wav files into that subfolder.
 *
 * - Removes numeric prefixes from extracted .wav files.
 * - Cleans non-ASCII characters in all filenames and directory names.
 * - Ensures no file is overwritten due to renaming conflicts.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ERROR_LOG_FILE = 'errors.txt';

//–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
// Helper Functions

/**
 * Logs errors to a text file.
 */
function logError(message) {
  console.error(message);
  fs.appendFileSync(ERROR_LOG_FILE, message + '\n');
}

/**
 * Removes numeric prefix from a filename (e.g., "97_sample.wav" -> "sample.wav").
 */
function removeNumericPrefix(filename) {
  return filename.replace(/^\d+_/, '');
}

/**
 * Sanitizes a filename by replacing non-ASCII characters with "_".
 */
function sanitizeFileName(name) {
  return name.replace(/[^a-zA-Z0-9._-]/g, '_');
}

/**
 * Ensures a unique file name by appending a counter if a conflict exists.
 */
function getUniqueFilePath(directory, fileName) {
  let base = path.basename(fileName, path.extname(fileName));
  let ext = path.extname(fileName);
  let sanitizedBase = sanitizeFileName(base);
  let uniqueFileName = sanitizedBase + ext;
  let filePath = path.join(directory, uniqueFileName);
  let counter = 1;

  while (fs.existsSync(filePath)) {
    uniqueFileName = `${sanitizedBase}_${counter}${ext}`;
    filePath = path.join(directory, uniqueFileName);
    counter++;
  }

  return filePath;
}

/**
 * Processes a single directory by:
 *   - Reproducing the directory structure in destDir with sanitized names.
 *   - Processing .gig files and extracting their samples.
 *   - Copying other files while ensuring safe file names.
 */
function processDirectory(srcDir, destDir) {
  // Ensure the sanitized destination directory exists.
  fs.mkdirSync(destDir, { recursive: true });

  // Read items in the source directory.
  const items = fs.readdirSync(srcDir, { withFileTypes: true });
  for (const item of items) {
    const srcPath = path.join(srcDir, item.name);
    const sanitizedItemName = sanitizeFileName(item.name);
    const destPath = path.join(destDir, sanitizedItemName);

    if (item.isDirectory()) {
      processDirectory(srcPath, destPath);
    } else if (item.isFile()) {
      if (path.extname(item.name).toLowerCase() === '.gig') {
        console.log(`Processing .gig file: ${srcPath}`);

        const gigBaseName = path.basename(item.name, '.gig');
        const sanitizedGigBaseName = sanitizeFileName(gigBaseName);
        const gigDestFolder = path.join(destDir, sanitizedGigBaseName);
        fs.mkdirSync(gigDestFolder, { recursive: true });

        const samplesDir = path.join(gigDestFolder, 'samples');
        fs.mkdirSync(samplesDir, { recursive: true });

        try {
          execSync(`gigextract "${srcPath}" "${samplesDir}"`, { stdio: 'inherit' });
        } catch (err) {
          logError(`Error extracting samples from ${srcPath}: ${err}`);
          continue;
        }

        try {
          const sampleFiles = fs.readdirSync(samplesDir);
          sampleFiles.forEach(file => {
            const newName = removeNumericPrefix(file);
            const sanitizedNewName = sanitizeFileName(newName);

            if (sanitizedNewName !== file) {
              const oldPath = path.join(samplesDir, file);
              const newPath = getUniqueFilePath(samplesDir, sanitizedNewName);
              if (oldPath !== newPath) {
                fs.renameSync(oldPath, newPath);
                console.log(`Renamed ${file} -> ${path.basename(newPath)}`);
              }
            }
          });
        } catch (renameErr) {
          logError(`Error renaming sample files in ${samplesDir}: ${renameErr}`);
        }

      } else {
        try {
          const destFilePath = getUniqueFilePath(destDir, sanitizedItemName);
          fs.copyFileSync(srcPath, destFilePath);
          console.log(`Copied file: ${srcPath} -> ${destFilePath}`);
        } catch (copyErr) {
          logError(`Error copying file ${srcPath}: ${copyErr}`);
        }
      }
    }
  }
}

/**
 * Main entry point.
 */
function main() {
  if (process.argv.length < 4) {
    console.error('Usage: node extract-samples.js <source directory> <destination directory>');
    process.exit(1);
  }

  const srcRoot = path.resolve(process.argv[2]);
  const destRoot = path.resolve(process.argv[3]);

  if (!fs.existsSync(srcRoot)) {
    console.error(`Source directory does not exist: ${srcRoot}`);
    process.exit(1);
  }

  console.log(`Starting processing:
    Source: ${srcRoot}
    Destination: ${destRoot}`);

  processDirectory(srcRoot, destRoot);

  console.log('Processing complete.');
}

main();
