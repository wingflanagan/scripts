#!/usr/bin/env node

import fs from 'fs';
import { spawn } from 'child_process';

/**
 * gigdump2json_minimal.mjs
 *
 * This version processes the gigdump output and then creates a minimal text file.
 * For each region (or for each dimension region if available) it outputs one line as:
 *   Sample=<name>, KeyRange=<key range>, VelocityRange=<velocity range>, Volume=<gain>
 *
 * Duplicate sample entries are removed.
 */

async function gigdump2json(gigPath, outputPath) {
  return new Promise((resolve, reject) => {
    const result = { Instruments: [] };
    let foundAvailableInstruments = false;
    let currentInstrument = null;
    let currentRegion = null;
    let currentDimensionRegions = null;
    let currentDimensions = null;

    function newInstrument() {
      return {
        Name: '',
        MIDIBank: '',
        MIDIProgram: '',
        ScriptSlots: '',
        Regions: [],
        UnknownTags: []
      };
    }

    function newRegion() {
      return {
        Sample: '',
        SampleRate: '',
        KeyRange: '',
        VelocityRange: '',
        Layers: '',
        Loops: '',
        UnknownTags: [],
        Dimensions: [],
        DimensionRegions: []
      };
    }

    function parseKeyValuePairs(line, targetObj, unknownTagsArray) {
      // Handle DimensionUpperLimits[] first
      let dimULMatch = line.match(/DimensionUpperLimits\[\]=\{[^}]+\}/);
      if (dimULMatch) {
        assignKeyValue(dimULMatch[0], targetObj, unknownTagsArray);
        line = line.replace(dimULMatch[0], '');
      }
      const chunks = line.split(',').map(c => c.trim()).filter(Boolean);
      for (let chunk of chunks) {
        let parenMatch = chunk.match(/^(.*?)(\([^)]+\))$/);
        if (parenMatch) {
          const prefix = parenMatch[1].trim();
          const parenContent = parenMatch[2].trim().replace(/^\(|\)$/g, '');
          if (!assignKeyValue(prefix, targetObj, unknownTagsArray)) {
            unknownTagsArray.push(prefix);
          }
          let subObjMatch = parenContent.match(/^(\S+)\s+(.*)$/);
          if (subObjMatch) {
            const subObjName = subObjMatch[1];
            const subObjKVs = subObjMatch[2];
            targetObj[subObjName] = targetObj[subObjName] || {};
            parseKeyValuePairs(subObjKVs, targetObj[subObjName], unknownTagsArray);
          } else {
            unknownTagsArray.push(parenContent);
          }
        } else {
          if (!assignKeyValue(chunk, targetObj, unknownTagsArray)) {
            unknownTagsArray.push(chunk);
          }
        }
      }
    }

    function assignKeyValue(chunk, targetObj, unknownTagsArray) {
      // Special handling for <NO_VALID_SAMPLE_REFERENCE>
      if (chunk.includes("<NO_VALID_SAMPLE_REFERENCE>")) {
        if (!targetObj.Sample) targetObj.Sample = "";
        chunk = chunk.replace("<NO_VALID_SAMPLE_REFERENCE>", "").trim();
      }
      let dimMatch = chunk.match(/^DimensionUpperLimits\[\]\s*=\s*\{(.*)\}$/);
      if (dimMatch) {
        let arrText = dimMatch[1];
        let arrParts = arrText.split(',').map(x => x.trim()).filter(Boolean);
        let arr = [];
        for (let p of arrParts) {
          let eqMatch = p.match(/^\[\d+\]=(.*)$/);
          if (eqMatch) {
            arr.push(parseUnknownString(eqMatch[1]));
          } else {
            unknownTagsArray.push(p);
          }
        }
        targetObj['DimensionUpperLimits'] = arr;
        return true;
      }
      let eqMatch = chunk.match(/^([^:=]+)\s*[:=]\s*(.*)$/);
      if (!eqMatch) {
        return false;
      }
      const key = eqMatch[1].trim();
      let val = eqMatch[2].trim();
      // Handle adjacent key-value pairs without commas.
      let subsequentMatches = val.match(/\s+\S+=/);
      if (subsequentMatches) {
        let parts = val.split(/\s+(?=\S+=)/);
        targetObj[key] = parseUnknownString(parts.shift().replace(/^"(.*)"$/, '$1').replace(/^'(.*)'$/, '$1'));
        for (let part of parts) {
          let m = part.match(/^([^:=\s]+)\s*[:=]\s*(.*)$/);
          if (m) {
            let subKey = m[1].trim();
            let subVal = m[2].trim();
            subVal = subVal.replace(/^"(.*)"$/, '$1').replace(/^'(.*)'$/, '$1');
            targetObj[subKey] = parseUnknownString(subVal);
          } else {
            unknownTagsArray.push(part);
          }
        }
        return true;
      }
      val = val.replace(/^"(.*)"$/, '$1').replace(/^'(.*)'$/, '$1');
      targetObj[key] = parseUnknownString(val);
      return true;
    }

    function parseSampleAndRate(line, targetObj, unknownTagsArray) {
      // Updated regex to handle quoted names and <NO_VALID_SAMPLE_REFERENCE>
      let sampleMatch = line.match(/Sample:\s*(?:"([^"]+)"|<NO_VALID_SAMPLE_REFERENCE>)\s*,?\s*(.*)$/);
      if (sampleMatch) {
        targetObj.Sample = sampleMatch[1] !== undefined ? sampleMatch[1] : "";
        let leftover = sampleMatch[2].trim();
        if (!leftover) return;
        let rateMatch = leftover.match(/^(\d+Hz)\s*,?\s*(.*)$/);
        if (rateMatch) {
          targetObj.SampleRate = rateMatch[1];
          leftover = rateMatch[2].trim();
        }
        if (leftover) {
          parseKeyValuePairs(leftover, targetObj, unknownTagsArray);
        }
      } else {
        unknownTagsArray.push(line);
      }
    }

    function parseUnknownString(str) {
      if (/^[+-]?\d+$/.test(str)) return parseInt(str, 10);
      if (/^[+-]?(\d*\.)?\d+$/.test(str)) return parseFloat(str);
      return str;
    }

    let buffer = '';
    const proc = spawn('gigdump', [gigPath]);

    proc.stdout.on('data', (data) => {
      buffer += data.toString();
      let lines = buffer.split('\n');
      buffer = lines.pop();

      for (let line of lines) {
        line = line.trim();
        if (!line) continue;
        if (!foundAvailableInstruments) {
          if (line.startsWith('Available Instruments:')) {
            foundAvailableInstruments = true;
          }
          continue;
        }
        let instrMatch = line.match(/^Instrument\s+(\d+)\)\s+"([^"]+)"\s*,?\s*(.*)$/);
        if (instrMatch) {
          currentInstrument = newInstrument();
          result.Instruments.push(currentInstrument);
          currentInstrument.Name = instrMatch[2];
          let leftover = instrMatch[3].trim();
          parseKeyValuePairs(leftover, currentInstrument, currentInstrument.UnknownTags);
          currentRegion = null;
          currentDimensions = null;
          currentDimensionRegions = null;
          continue;
        }
        let regionMatch = line.match(/^Region\s+(\d+)\)\s*(.*)$/);
        if (regionMatch && currentInstrument) {
          currentRegion = newRegion();
          currentInstrument.Regions.push(currentRegion);
          currentDimensions = currentRegion.Dimensions;
          currentDimensionRegions = currentRegion.DimensionRegions;
          let leftover = regionMatch[2].trim();
          if (leftover.startsWith('Sample:')) {
            parseSampleAndRate(leftover, currentRegion, currentRegion.UnknownTags);
          } else {
            parseKeyValuePairs(leftover, currentRegion, currentRegion.UnknownTags);
          }
          continue;
        }
        let dimRegionMatch = line.match(/^Dimension\s+Region\s+(\d+)\)\s*(.*)$/);
        if (dimRegionMatch && currentRegion) {
          let dimObj = { UnknownTags: [] };
          currentDimensionRegions.push(dimObj);
          let leftover = dimRegionMatch[2].trim();
          if (leftover.startsWith('Sample:')) {
            parseSampleAndRate(leftover, dimObj, dimObj.UnknownTags);
          } else {
            parseKeyValuePairs(leftover, dimObj, dimObj.UnknownTags);
          }
          continue;
        }
        let dimensionLineMatch = line.match(/^Dimension\[(\d+)\]:\s*(.*)$/);
        if (dimensionLineMatch && currentRegion) {
          let dimObj = { UnknownTags: [] };
          currentDimensions.push(dimObj);
          let leftover = dimensionLineMatch[2].trim();
          parseKeyValuePairs(leftover, dimObj, dimObj.UnknownTags);
          continue;
        }
        if (line.startsWith('Sample:')) {
          if (currentDimensionRegions && currentDimensionRegions.length > 0) {
            let dimObj = currentDimensionRegions[currentDimensionRegions.length - 1];
            parseSampleAndRate(line, dimObj, dimObj.UnknownTags);
          } else if (currentRegion) {
            parseSampleAndRate(line, currentRegion, currentRegion.UnknownTags);
          }
          continue;
        }
        let handled = false;
        if (currentDimensionRegions && currentDimensionRegions.length > 0) {
          let dimObj = currentDimensionRegions[currentDimensionRegions.length - 1];
          parseKeyValuePairs(line, dimObj, dimObj.UnknownTags);
          handled = true;
        } else if (currentRegion) {
          parseKeyValuePairs(line, currentRegion, currentRegion.UnknownTags);
          handled = true;
        } else if (currentInstrument) {
          parseKeyValuePairs(line, currentInstrument, currentInstrument.UnknownTags);
          handled = true;
        }
        if (!handled && currentInstrument) {
          currentInstrument.UnknownTags.push(line);
        }
      }
    });

    proc.stderr.on('data', (errData) => {
      console.error(errData.toString());
    });

    proc.on('close', (code) => {
      if (buffer.trim()) {
        // Process any remaining data if necessary.
      }
      if (code !== 0) {
        return reject(new Error(`gigdump process exited with code ${code}`));
      }
      // Remove empty UnknownTags recursively
      function removeEmptyUnknownTags(obj) {
        if (Array.isArray(obj)) {
          for (let x of obj) removeEmptyUnknownTags(x);
        } else if (typeof obj === 'object' && obj !== null) {
          for (let k of Object.keys(obj)) {
            if (k === 'UnknownTags' && Array.isArray(obj[k]) && obj[k].length === 0) {
              delete obj[k];
            } else {
              removeEmptyUnknownTags(obj[k]);
            }
          }
        }
      }
      removeEmptyUnknownTags(result);

      // --- Create a minimal output ---
      // We'll output one line per unique sample with these keys:
      //   Sample, KeyRange, VelocityRange, Volume (from Gain if available)
      const sampleLines = new Set();

      result.Instruments.forEach(instr => {
        if (!instr.Regions || instr.Regions.length === 0) return;
        instr.Regions.forEach(region => {
          // Prepare base key-range and velocity-range from region
          const keyRange = region.KeyRange || '';
          const velocityRange = region.VelocityRange || '';
          // If dimension regions exist, output each one
          if (region.DimensionRegions && region.DimensionRegions.length > 0) {
            region.DimensionRegions.forEach(dim => {
              // Use the Gain field for volume if available
              const volume = dim.Gain || '';
              const sampleName = dim.Sample || region.Sample || '';
              const line = `Sample=${sampleName}, KeyRange=${keyRange}, VelocityRange=${velocityRange}, Volume=${volume}`;
              sampleLines.add(line);
            });
          } else {
            // Otherwise, output region's sample info
            const sampleName = region.Sample || '';
            const line = `Sample=${sampleName}, KeyRange=${keyRange}, VelocityRange=${velocityRange}, Volume=`;
            sampleLines.add(line);
          }
        });
      });

      // Write the minimal output (one comma-delimited line per sample)
      fs.writeFile(outputPath, Array.from(sampleLines).join('\n'), (err) => {
        if (err) return reject(err);
        console.log(`Wrote minimal sample lookup data to ${outputPath}`);
        resolve();
      });
    });
  });
}

if (process.argv[1] === new URL(import.meta.url).pathname) {
  const gigPath = process.argv[2];
  const outputPath = process.argv[3];
  if (!gigPath || !outputPath) {
    console.error('Usage: node gigdump2json_minimal.mjs <input.gig> <output.txt>');
    process.exit(1);
  }
  gigdump2json(gigPath, outputPath)
    .then(() => console.log('Done!'))
    .catch(err => {
      console.error('ERROR:', err);
      process.exit(1);
    });
}
