import requests
from bs4 import BeautifulSoup
import time

def search_yahoo(keyword):
    url = f"https://search.yahoo.com/search?p={keyword}"
    response = requests.get(url)
    if response.status_code == 200: 
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a', href=True):
            if "yahoo.com" not in link['href'] and not link['href'].startswith("/"):
                print(link['href'])
    else:
        print("Failed to retrieve the page.")

# Example usage
keyword = input("Enter keyword to search on Yahoo: ")
search_yahoo(keyword)
time.sleep(5)  # Wait for 5 seconds before making another request
