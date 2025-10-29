// src/utils.js
import fs from 'fs/promises';
import path from 'path';

/**
 * Ensures a directory exists, creating it if it doesn't.
 * @param {string} dirPath - The path to the directory.
 */
export async function ensureDirExists(dirPath) {
  try {
    await fs.mkdir(dirPath, { recursive: true });
  } catch (error) {
    if (error.code!== 'EEXIST') {
      throw error;
    }
  }
}

/**
 * Sanitizes a URL to create a valid and readable filename.
 * @param {string} url - The URL to sanitize.
 * @returns {string} A sanitized filename with a.md extension.
 */
export function urlToFilename(url) {
  const parsedUrl = new URL(url);
  let filename = parsedUrl.hostname + parsedUrl.pathname;
  
  // Replace invalid characters with an underscore
  filename = filename.replace(/[\/\\?%*:|"<>]/g, '_');
  
  // Trim trailing underscores
  filename = filename.replace(/_+$/, '');

  return `${filename}.md`;
}

/**
 * A simple logger that prepends a timestamp to messages.
 * @param {string} message - The message to log.
 * @param {'INFO' | 'ERROR' | 'SUCCESS'} level - The log level.
 */
export function log(message, level = 'INFO') {
  const timestamp = new Date().toISOString();
  const logFunc = level === 'ERROR'? console.error : console.log;
  logFunc(`[${timestamp}][${level}] ${message}`);
}