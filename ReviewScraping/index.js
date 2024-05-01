const fs = require("fs");
const path = require("path");

const puppeteer = require("puppeteer");
const UserAgent = require("user-agents");

const FileUtil = require("./core/file-util");
const { getASINWithRegex } = require("./core/amazon-util");
const { getReviewsOnPage } = require("./core/scraping-util");

// ASINs to scrape
const ITEM_ASINS = require("./resources/items-to-scrape.json")
  .map((item) => getASINWithRegex(item))
  .filter((asin) => asin !== null);

console.log(ITEM_ASINS);

const csvWriteStream = fs.createWriteStream(
  path.join(__dirname, "output/output.csv"),
  { flags: "a" }
);
const outputFileUtil = new FileUtil(csvWriteStream);

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--no-sandbox"],
  });

  const page = await browser.newPage();

  let asin;
  for (let i = 0; i < ITEM_ASINS.length; i++) {
    asin = ITEM_ASINS[i];

    // set random user agent for Amazon rate limit purposes
    const ua = new UserAgent({
      // platform: "Win32",
      deviceCategory: "desktop",
    }).toString();
    console.log(`ASIN: ${asin} | Scraping with user agent ${ua}`);
    await page.setUserAgent(ua);

    await getReviewsOnPage(page, asin, outputFileUtil, i);
  }
})();
