// config.js

// Array of URLs to scrape. Add any URLs you want to process here.
export const URLS_TO_SCRAPE = [
  'http://sfzformat.com/', 
];

// Directory where the final Markdown files will be saved.
export const OUTPUT_DIR = './output';

// Concurrency limit for p-limit.
// This is the maximum number of pages that will be scraped simultaneously.
// A value between 3 and 5 is a safe starting point.
export const CONCURRENCY_LIMIT = 5;

// Puppeteer navigation settings.
export const PUPPETEER_OPTIONS = {
  // Wait until the network is almost idle.
  waitUntil: 'networkidle2',
  // Timeout in milliseconds for page navigation.
  timeout: 60000, // 60 seconds
};