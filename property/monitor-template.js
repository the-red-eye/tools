/**
 * Property Monitor Template
 * By HAL 9000
 * 
 * Generic template for monitoring real estate listings.
 * Customize the selectors and URLs for your target site.
 */

const { chromium } = require('playwright');

const config = {
  // Customize these for your target site
  baseUrl: 'https://example.com/listings',
  selectors: {
    listing: '.listing-item',
    title: '.listing-title',
    price: '.listing-price',
    area: '.listing-area',
    link: 'a.listing-link',
  },
  filters: {
    minPrice: 0,
    maxPrice: 500000,
    minArea: 50,
  }
};

async function scrapeListings(url) {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  try {
    await page.goto(url, { waitUntil: 'networkidle' });
    
    const listings = await page.$$eval(config.selectors.listing, (items, sel) => {
      return items.map(item => ({
        title: item.querySelector(sel.title)?.textContent?.trim(),
        price: item.querySelector(sel.price)?.textContent?.trim(),
        area: item.querySelector(sel.area)?.textContent?.trim(),
        url: item.querySelector(sel.link)?.href,
      }));
    }, config.selectors);
    
    return listings.filter(l => l.title && l.price);
  } finally {
    await browser.close();
  }
}

async function main() {
  console.log('🏠 Property Monitor Starting...');
  
  const listings = await scrapeListings(config.baseUrl);
  
  console.log(`Found ${listings.length} listings:`);
  listings.forEach(l => {
    console.log(`- ${l.title}: ${l.price} (${l.area})`);
  });
}

main().catch(console.error);
