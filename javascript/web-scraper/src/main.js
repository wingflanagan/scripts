// src/main.js
import puppeteer from 'puppeteer';
import pLimit from 'p-limit';
import { URLS_TO_SCRAPE, CONCURRENCY_LIMIT, OUTPUT_DIR } from '../config.js';
import { ensureDirExists, log } from './utils.js';
import { scrapeAndSave } from './scraper.js';

/**
 * The main function that orchestrates the entire scraping process.
 */
async function main() {
  log('Starting the website-to-markdown archiver...');

  // 1. Ensure the output directory exists.
  await ensureDirExists(OUTPUT_DIR);
  log(`Output directory is ready at: ${OUTPUT_DIR}`);

  // 2. Launch a single Puppeteer browser instance to be shared across tasks.
  const browser = await puppeteer.launch({ headless: true });
  log('Browser instance launched.');

  // 3. Set up the concurrency limiter.
  const limit = pLimit(CONCURRENCY_LIMIT);
  log(`Concurrency limit set to ${CONCURRENCY_LIMIT}.`);

  // 4. Create an array of scraping tasks, wrapped in the limiter.
  const tasks = URLS_TO_SCRAPE.map(url => {
    return limit(() => scrapeAndSave(browser, url));
  });

  // 5. Execute all tasks using Promise.all.
  log(`Processing ${URLS_TO_SCRAPE.length} URLs...`);
  await Promise.all(tasks);

  // 6. Clean up by closing the browser.
  await browser.close();
  log('All tasks completed. Browser closed. Exiting.');
}

// Execute the main function and handle any top-level errors.
main().catch(error => {
  log(`A critical error occurred: ${error.message}`, 'ERROR');
  process.exit(1);
});