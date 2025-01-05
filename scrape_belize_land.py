from playwright.sync_api import sync_playwright
import time
import csv

def scrape_land_listings():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # List to store all listings
        all_listings = []
        
        # Start with page 1
        current_page = 1
        
        while True:
            url = f"https://belizerealestatesearch.com/land-for-sale-in-belize/page/{current_page}/?view=Grid"
            page.goto(url)
            time.sleep(2)  # Wait for content to load
            
            # Check if we've reached the end of listings
            if "No properties were found" in page.content():
                break
                
            # Get all property listings on current page
            listings = page.query_selector_all(".property-item")
            
            if not listings:
                break
                
            for listing in listings:
                try:
                    # Extract data from each listing
                    title = listing.query_selector(".property-title a")
                    price = listing.query_selector(".price")
                    lot_size = listing.query_selector(".lot-size")
                    link = listing.query_selector(".property-title a")
                    
                    listing_data = {
                        'title': title.inner_text() if title else 'N/A',
                        'price': price.inner_text().strip() if price else 'N/A',
                        'lot_size': lot_size.inner_text() if lot_size else 'N/A',
                        'link': link.get_attribute('href') if link else 'N/A'
                    }
                    
                    all_listings.append(listing_data)
                    
                except Exception as e:
                    print(f"Error scraping listing: {e}")
                    continue
            
            current_page += 1
            
        browser.close()
        
        # Save to CSV
        with open('belize_land_listings.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'price', 'lot_size', 'link'])
            writer.writeheader()
            writer.writerows(all_listings)
        
        return all_listings

if __name__ == "__main__":
    listings = scrape_land_listings()
    print(f"Successfully scraped {len(listings)} listings")
