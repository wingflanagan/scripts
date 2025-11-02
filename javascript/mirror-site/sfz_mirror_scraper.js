// sfz_mirror_scraper_generalized.js
// Mirrors sfzformat.com including markdown conversion, image downloading, and recursive route discovery (including opcodes and similar nested pages)

const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer");
const { URL } = require("url");
const pLimit = require("p-limit").default;
const TurndownService = require("turndown");

const BASE_URL = "https://sfzformat.com";
const OUTPUT_DIR = path.resolve(__dirname, "sfz-mirror");

const turndownService = new TurndownService();

turndownService.addRule("pre", {
  filter: ["pre"],
  replacement: function (content) {
    return "\n```\n" + content + "\n```\n";
  },
});

turndownService.addRule("internal-links", {
  filter: function (node) {
    return (
      node.nodeName === "A" &&
      node.getAttribute("href") &&
      node.getAttribute("href").startsWith("/")
    );
  },
  replacement: function (content, node) {
    const href = node.getAttribute("href").split("#")[0].split("?")[0];
    const markdownFile = sanitizeFileName(href || "home") + ".md";
    return `[${content}](${markdownFile})`;
  },
});

function sanitizeFileName(name) {
  return name.replace(/[^a-z0-9]/gi, "_").toLowerCase();
}

function ensureDirSync(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

async function downloadImage(imgUrl, pageUrl, folder) {
  try {
    const imgAbsUrl = new URL(imgUrl, pageUrl).toString();
    const imgPath = new URL(imgAbsUrl).pathname;
    let imgName = sanitizeFileName(path.basename(imgPath));
    if (!imgName) {
      console.warn(`⚠️ Skipping image with no valid filename: ${imgAbsUrl}`);
      return imgUrl;
    }

    ensureDirSync(folder);
    const destPath = path.join(folder, imgName);
    const res = await fetch(imgAbsUrl);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const buffer = await res.arrayBuffer();
    fs.writeFileSync(destPath, Buffer.from(buffer));
    return path.relative(OUTPUT_DIR, destPath);
  } catch (err) {
    console.warn(`⚠️ Failed to download ${imgUrl}: ${err.message}`);
    return imgUrl;
  }
}

async function crawlPage(browser, route) {
  const url = BASE_URL + route;
  console.log(`🔗 Navigating: ${url}`);
  const page = await browser.newPage();
  try {
    await page.goto(url, { waitUntil: "networkidle2", timeout: 30000 });

    const images = await page.$$eval("img", imgs => imgs.map(i => i.src || i.getAttribute("src")));
    for (let src of images) {
      const localPath = await downloadImage(src, url, path.join(OUTPUT_DIR, "images"));
      await page.$$eval(
        "img",
        (imgs, oldSrc, newSrc) => {
          imgs.forEach(img => {
            if ((img.src && img.src === oldSrc) || img.getAttribute("src") === oldSrc) {
              img.setAttribute("src", newSrc);
            }
          });
        },
        src,
        localPath
      );
    }

    const html = await page.content();
    const markdown = turndownService.turndown(html);
    const safeName = sanitizeFileName(route || "home") + ".md";
    fs.writeFileSync(path.join(OUTPUT_DIR, safeName), markdown);
    console.log(`✅ Saved: ${safeName}`);
  } catch (err) {
    console.error(`❌ Error crawling ${route}: ${err.message}`);
  } finally {
    await page.close();
  }
}

async function discoverRoutes(browser) {
  const visited = new Set();
  const toVisit = new Set(["/"]);

  const crawlQueue = async (route) => {
    const url = BASE_URL + route;
    const page = await browser.newPage();
    try {
      await page.goto(url, { waitUntil: "networkidle2", timeout: 30000 });
      const links = await page.$$eval("a", anchors =>
        anchors.map(a => a.getAttribute("href")).filter(h => h && h.startsWith("/"))
      );

      for (const href of links) {
        const clean = href.split("#")[0].split("?")[0];
        if (!visited.has(clean)) toVisit.add(clean);
      }
    } catch (err) {
      console.warn(`⚠️ Could not inspect ${route}: ${err.message}`);
    } finally {
      await page.close();
    }
  };

  while (toVisit.size > 0) {
    const next = toVisit.values().next().value;
    toVisit.delete(next);
    visited.add(next);
    await crawlQueue(next);
  }

  console.log(`🔍 Discovered ${visited.size} internal routes:`);
  visited.forEach(r => console.log(" -", r));
  return Array.from(visited);
}

(async () => {
  ensureDirSync(OUTPUT_DIR);
  ensureDirSync(path.join(OUTPUT_DIR, "images"));

  const browser = await puppeteer.launch({ headless: "new" });
  try {
    const routes = await discoverRoutes(browser);
    const limit = pLimit(5);
    const crawlTasks = routes.map(route => limit(() => crawlPage(browser, route)));
    await Promise.all(crawlTasks);
    console.log(`🎉 All done. Content saved to ${OUTPUT_DIR}`);
  } catch (err) {
    console.error("Fatal error during crawling:", err);
  } finally {
    await browser.close();
  }
})();
