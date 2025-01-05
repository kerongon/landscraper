from playwright.sync_api import sync_playwright
import time
import csv
import json

def scrape_land_listings():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to False for debugging
        page = browser.new_page()

        # List to store all listings
        all_listings = []
        
        # Start with page 1
        current_page = 1
        
        while True:
            print(f"Scraping page {current_page}")
            url = f"https://belizerealestatesearch.com/land-for-sale-in-belize/page/{current_page}/?view=Grid"
            page.goto(url)
            time.sleep(3)  # Increased wait time
            
            # Get all property listings on current page
            listings = page.query_selector_all(".prop-det")
            
            print(f"Found {len(listings)} listings on page {current_page}")
            
            if not listings:
                print("No listings found on this page, breaking...")
                break
                
            for listing in listings:
                try:
                    # Extract data from each listing using multiple selectors
                    title = listing.query_selector(".prop-title h1")
                    title2 = listing.query_selector(".prop-desc h1")
                    price = listing.query_selector(".list-price span")
                    link = listing.query_selector(".prop-title a")
                    description = listing.query_selector(".prop-desc")
                    image = listing.query_selector(".listing-item img")
                    
                    # Get the text and clean it up
                    title_text = (title1.inner_text() if title1 else '') or \
                                (title2.inner_text() if title2 else '') or \
                                (title3.inner_text() if title3 else '')
                    price_text = price.inner_text() if price else ''
                    link_href = link.get_attribute('href') if link else ''
                    desc_text = description.inner_text() if description else ''
                    image_url = image.get_attribute('src') if image else ''
                    
                    if not any([title_text, price_text, link_href, desc_text]):
                        continue
                        
                    listing_data = {
                        'title': title_text.strip(),
                        'price': price_text.strip(),
                        'description': desc_text.strip(),
                        'link': link_href.strip(),
                        'image_url': image_url.strip()
                    }
                    
                    print(f"Extracted listing: {listing_data['title']} - {listing_data['price']}")
                    all_listings.append(listing_data)
                    
                except Exception as e:
                    print(f"Error scraping listing: {e}")
                    continue
            
            # Check for next page
            next_page = page.query_selector(f"a[href*='page/{current_page + 1}']")
            if not next_page:
                print("No next page found, breaking...")
                break
                
            current_page += 1
            
        browser.close()
        
        # Save to CSV and JSON
        if all_listings:
            # Save CSV
            with open('belize_land_listings.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['title', 'price', 'description', 'link', 'image_url'])
                writer.writeheader()
                writer.writerows(all_listings)
            print(f"Saved {len(all_listings)} listings to CSV")
            
            # Save JSON
            with open('belize_land_listings.json', 'w', encoding='utf-8') as f:
                json.dump(all_listings, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(all_listings)} listings to JSON")
        else:
            print("No listings were collected")
        
        return all_listings

if __name__ == "__main__":
    listings = scrape_land_listings()
    print(f"Successfully scraped {len(listings)} listings")
