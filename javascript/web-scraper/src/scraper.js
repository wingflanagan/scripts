// src/scraper.js
import puppeteer from 'puppeteer';
import TurndownService from 'turndown';
import { gfm } from 'turndown-plugin-gfm';
import fs from 'fs/promises';
import path from 'path';
import { PUPPETEER_OPTIONS, OUTPUT_DIR } from '../config.js';
import { urlToFilename, log } from './utils.js';

// Initialize the Turndown service once to be reused.
const turndownService = new TurndownService({
  headingStyle: 'atx',
  codeBlockStyle: 'fenced',
});
turndownService.use(gfm);

/**
 * Scrapes a single web page, converts it to Markdown, and saves it to a file.
 * This function encapsulates the entire process for one URL.
 * @param {puppeteer.Browser} browser - The Puppeteer browser instance.
 * @param {string} url - The URL to scrape.
 */
export async function scrapeAndSave(browser, url) {
  let page;
  try {
    // Open a new page in the browser.
    page = await browser.newPage();

    // Navigate to the URL with the specified waiting strategy and timeout.
    log(`Navigating to: ${url}`);
    await page.goto(url, PUPPETEER_OPTIONS);
    log(`Page loaded: ${url}`);

    // Extract the full HTML content of the page.
    const htmlContent = await page.content();
    if (!htmlContent) {
      throw new Error('Failed to retrieve HTML content.');
    }
    log(`HTML content captured for: ${url}`);

    // Convert the HTML to Markdown using the Turndown service.
    const markdown = turndownService.turndown(htmlContent);
    log(`Converted to Markdown for: ${url}`);

    // Generate a valid filename from the URL.
    const filename = urlToFilename(url);
    const outputPath = path.join(OUTPUT_DIR, filename);

    // Save the Markdown content to the output file.
    await fs.writeFile(outputPath, markdown);
    log(`File saved: ${outputPath}`, 'SUCCESS');

  } catch (error) {
    // The per-task error handling ensures one failure doesn't stop everything.
    log(`Failed to process ${url}. Reason: ${error.message}`, 'ERROR');
  } finally {
    // Ensure the page is closed to free up resources, even if an error occurred.
    if (page) {
      await page.close();
    }
  }
}