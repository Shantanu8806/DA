import requests
from bs4 import BeautifulSoup
import time

# List to hold the product information as dictionaries
products = []

for i in range(2, 12):
    url = f'https://www.flipkart.com/search?q=mobiles+under+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={i}'
    r = requests.get(url)
    
    # Log the status of the request
    print(f"Fetching page {i}: Status code {r.status_code}")
    
    if r.status_code == 429:
        print("Rate limited. Waiting for a while before retrying...")
        time.sleep(60)  # Wait for 60 seconds before retrying
        r = requests.get(url)
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        box = soup.find("div", class_="DOjaWF gdgoEp")
        
        if box:
            names = box.find_all("div", class_='KzDlHZ')
            prices = box.find_all("div", class_="Nx9bqj _4b5DiR")
            desc = box.find_all("ul", class_="G4BRas")
            reviews = box.find_all("div", class_="XQDdHH")

            for j in range(len(names)):
                try:
                    product = {
                        'name': names[j].text,
                        'price': prices[j].text,
                        'description': desc[j].text,
                        'review': reviews[j].text
                    }
                    products.append(product)
                except IndexError:
                    print(f"Data mismatch at page {i}, index {j}")
        
            print(f"Page {i} data collected:")
            print(products[-len(names):])  # Print the last collected products for this page
        else:
            print(f"No product box found on page {i}")
    else:
        print(f"Failed to fetch page {i} after waiting.")
    
    # Delay between requests to avoid rate limiting
    time.sleep(5)  # Wait for 5 seconds before the next request

# Convert the list of dictionaries to a DataFrame
import pandas as pd

df = pd.DataFrame(products)
df.to_csv('flipkart_mobiles.csv', index=False)
