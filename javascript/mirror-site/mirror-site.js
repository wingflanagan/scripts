const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');
const TurndownService = require('turndown');

const startUrl = 'https://sfzformat.com'; // 🔁 CHANGE THIS
const baseDomain = 'sfzformat.com';             // 🔁 CHANGE THIS
const outputDir = './mirror';

const visited = new Set();
const toVisit = [startUrl];
const turndownService = new TurndownService({
  codeBlockStyle: 'fenced',
  headingStyle: 'atx'
});

function sanitizeFilename(url) {
  return url
    .replace(/^https?:\/\//, '')
    .replace(baseDomain, '')
    .replace(/[^a-z0-9]/gi, '_')
    .replace(/^_+|_+$/g, '')
    .toLowerCase() || 'index';
}

function isSameDomain(url) {
  try {
    const parsed = new URL(url);
    return parsed.hostname.endsWith(baseDomain);
  } catch {
    return false;
  }
}

async function crawl() {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();

  while (toVisit.length > 0) {
    const url = toVisit.pop();
    if (visited.has(url)) continue;
    visited.add(url);

    try {
      console.log(`🌐 Visiting: ${url}`);
      await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });

      const fileBase = sanitizeFilename(url);

      // Save full raw HTML
      const fullHTML = await page.content();
      fs.writeFileSync(path.join(outputDir, `${fileBase}.html`), fullHTML);

      // Strip headers/footers and rewrite internal links, then get inner HTML
      const contentHTML = await page.evaluate((baseDomain) => {
        const kill = (sel) => document.querySelectorAll(sel).forEach(e => e.remove());
        kill('header');
        kill('footer');
        kill('nav');
        kill('.sidebar');
        kill('#cookie-banner');

        const anchors = document.querySelectorAll('a');
        anchors.forEach(a => {
          const href = a.getAttribute('href');
          if (!href) return;
          try {
            const url = new URL(href, window.location.href);
            if (url.hostname.endsWith(baseDomain)) {
              let pathname = url.pathname;
              if (pathname.endsWith('/')) pathname = pathname.slice(0, -1);
              const filename = pathname.split('/').filter(Boolean).join('_') || 'index';
              const newHref = `${filename}.md${url.hash || ''}`;
              a.setAttribute('href', newHref);
            }
          } catch (e) {
            // skip malformed hrefs
          }
        });

        const main = document.querySelector('main') || document.body;
        return main.innerHTML;
      }, baseDomain);

      // Save plain text
      const plainText = await page.evaluate(() => document.body.innerText);
      fs.writeFileSync(path.join(outputDir, `${fileBase}.txt`), plainText);

      // Save Markdown
      const markdown = turndownService.turndown(contentHTML);
      fs.writeFileSync(path.join(outputDir, `${fileBase}.md`), markdown);

      // Discover internal links to visit
      const links = await page.$$eval('a', as => as.map(a => a.href));
      for (const link of links) {
        if (isSameDomain(link) && !visited.has(link)) {
          toVisit.push(link);
        }
      }

    } catch (err) {
      console.warn(`⚠️ Error visiting ${url}: ${err.message}`);
    }
  }

  await browser.close();
  console.log(`✅ All done! Files saved in "${outputDir}"`);
}

fs.mkdirSync(outputDir, { recursive: true });
crawl();