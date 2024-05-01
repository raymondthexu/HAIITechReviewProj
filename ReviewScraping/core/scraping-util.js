const cheerio = require("cheerio");
const ObjectsToCsv = require("objects-to-csv");

async function getReviewsOnPage(page, asin, file, asinIndex) {
  await page.goto(
    `https://www.amazon.com/product-reviews/${asin}/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews`
  );

  // check if on last review page
  let onLastReviewPage = await _checkIfLastReviewPage(page);
  let reviewPageIndex = 0;
  let currentReviews, currentReviewsCsvContent;
  while (!onLastReviewPage) {
    // while not on last review page
    currentReviews = await _extractReviewsOnPage(page, asin);
    currentReviewsCsvContent = (
      await new ObjectsToCsv(currentReviews).toString()
    ).split("\n"); // csv string
    if (
      asinIndex !== 0 ||
      reviewPageIndex != 0 ||
      process.env.CSVSTART.toLowerCase() === "none"
    ) {
      // if this is NOT the first ASIN
      // OR this is the first review
      // page (in other words, anything
      // but the very beginning of the
      // reviewing process)
      currentReviewsCsvContent = currentReviewsCsvContent.slice(1);
    }
    // put it back together
    currentReviewsCsvContent = currentReviewsCsvContent.join("\n");
    file.appendLine(currentReviewsCsvContent, false); // write to file

    await _sleep(5000); // wait

    // go to next page
    try {
      await page.evaluate(() =>
        document.querySelector(".a-pagination .a-last a").click()
      ); // click next button
    } catch (e) {
      console.log("Most likely reached end of the list");
    }

    onLastReviewPage = await _checkIfLastReviewPage(page);
    reviewPageIndex++; // update tally
  }
}

async function _sleep(time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

async function _checkIfLastReviewPage(page) {
  try {
    await _sleep(5000);
    return await page.evaluate(() =>
      document
        .querySelector(".a-pagination .a-last")
        .classList.contains("a-disabled")
    );
  } catch (e) {
    console.log("ERROR:");
    console.error(e);
    process.exit(1);
  }
}

async function _extractReviewsOnPage(page, asin) {
  const bodyHTML = await page.evaluate(() => document.body.innerHTML); // get html
  const $ = cheerio.load(bodyHTML); // load html into cheerio parser

  let reviewElementList = $("[id^='customer_review-']");
  let reviews = [];
  let currentElement;
  for (let i = 0; i < reviewElementList.length; i++) {
    currentElement = $(reviewElementList[i]); // initialize current element
    reviews.push({
      asin, // uses provided ASIN value
      stars: _extractStarRatingFromText(
        currentElement.find(".review-rating span").text().trim()
      ),
      title: currentElement.find(".review-title").text().trim(),
      text: currentElement
        .find(".review-text.review-text-content")
        .text()
        .trim(),
    });
  }
  return reviews;
}

function _extractStarRatingFromText(text) {
  return parseFloat(
    text
      .replace("stars", "") // remove stars
      .trim() // trim whitespace
      .split(" out of ")[0] // take first number (# of stars)
  );
}

module.exports = {
  getReviewsOnPage,
};
