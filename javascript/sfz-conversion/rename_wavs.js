#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

if (process.argv.length < 3) {
  console.error('Usage: node renameWav.js <root-folder>');
  process.exit(1);
}

const rootFolder = process.argv[2];

/**
 * Sanitize a filename by:
 *   - Replacing any Unicode replacement characters with a dash.
 *   - Normalizing to NFKD and removing combining diacritical marks.
 *   - Converting German umlauts (ä, ö, ü, Ä, Ö, Ü) and ß to their Anglicized equivalents.
 *   - Replacing any character not in [A-Za-z0-9_.# -] with a dash.
 *
 * @param {string} name - The filename (or part of it) to sanitize.
 * @returns {string} - The sanitized filename.
 */
function sanitizeFilename(name) {
  // Replace any Unicode replacement characters (often resulting from decoding errors)
  name = name.replace(/\uFFFD/g, '-');

  // Normalize to NFKD so that letters with diacritics are decomposed.
  try {
    name = name.normalize('NFKD');
  } catch (e) {
    // In case normalization fails, continue with the original string.
  }
  // Remove combining diacritical marks.
  name = name.replace(/[\u0300-\u036F]/g, '');

  // Replace German umlauts and ess-zet.
  name = name.replace(/ä/g, 'ae')
             .replace(/Ä/g, 'Ae')
             .replace(/ö/g, 'oe')
             .replace(/Ö/g, 'Oe')
             .replace(/ü/g, 'ue')
             .replace(/Ü/g, 'Ue')
             .replace(/ß/g, 'ss');

  // Now replace any character that is not an ASCII letter, digit, underscore, dash,
  // period, hash, or space with a dash.
  name = name.replace(/[^A-Za-z0-9_.# \-]/g, '-');

  return name;
}

/**
 * Recursively process a directory.
 *
 * Reads directory entries as raw Buffers (to capture the exact byte sequence) and
 * decodes them using "latin1". Then for each .wav file, if its name matches the
 * expected pattern (something ending with an uppercase letter A–G, an underscore,
 * a single digit, then ".wav"), it replaces that underscore with a '#' and then
 * sanitizes the filename.
 *
 * If the file does not match the pattern, a debug message is printed.
 *
 * @param {string} dir - The directory to process.
 */
function processDirectory(dir) {
  let items;
  try {
    // Read directory entries as raw buffers.
    items = fs.readdirSync(dir, { encoding: 'buffer' });
  } catch (err) {
    console.error(`Error reading directory ${dir}: ${err}`);
    return;
  }

  items.forEach(itemBuffer => {
    // Decode the raw filename with 'latin1' to get a one-to-one byte-to-character mapping.
    const itemName = itemBuffer.toString('latin1');
    const fullPath = path.join(dir, itemName);

    let stats;
    try {
      stats = fs.statSync(fullPath);
    } catch (err) {
      if (err.code === 'ENOENT') {
        console.warn(`Skipping ${fullPath}: file not found`);
        return;
      } else {
        console.error(`Error accessing ${fullPath}: ${err}`);
        return;
      }
    }

    if (stats.isDirectory()) {
      processDirectory(fullPath);
    } else if (stats.isFile() && path.extname(itemName).toLowerCase() === '.wav') {
      // This regex expects filenames ending with an uppercase letter A–G, an underscore,
      // a single digit, then ".wav". For example, "Tuba_ff_G_3.wav".
      const regex = /^(.+[A-G])_([\d])(\.wav)$/;
      const match = itemName.match(regex);
      if (match) {
        // Build the new filename by replacing the underscore with a '#'
        let newFileName = `${match[1]}#${match[2]}${match[3]}`;
        // Sanitize the new filename to remove any non-US-English characters.
        newFileName = sanitizeFilename(newFileName);
        const newFullPath = path.join(dir, newFileName);

        // If a file already exists with the new name, remove it.
        if (fs.existsSync(newFullPath)) {
          try {
            fs.unlinkSync(newFullPath);
            console.log(`Removed existing file: ${newFullPath}`);
          } catch (err) {
            console.error(`Error removing ${newFullPath}: ${err}`);
            return;
          }
        }

        try {
          fs.renameSync(fullPath, newFullPath);
          console.log(`Renamed: ${fullPath} -> ${newFullPath}`);
        } catch (err) {
          console.error(`Error renaming ${fullPath} to ${newFullPath}: ${err}`);
        }
      } else {
        // Log the filename if it does not match our expected pattern.
        console.log(`Filename did not match expected pattern: "${itemName}"`);
      }
    }
  });
}

processDirectory(rootFolder);
