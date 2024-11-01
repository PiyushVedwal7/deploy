import requests
from bs4 import BeautifulSoup
import time

def search_for_keyword(url, keyword):
    response = requests.get(url)
    
    if response.status_code == 200: 
        soup = BeautifulSoup(response.content, 'html.parser')
        found_links = []

        for link in soup.find_all('a', href=True):
            link_url = link['href']
          
            if keyword.lower() in link_url.lower() and not link_url.startswith("/"):
                found_links.append(link_url)
        
        # Print the found links
        if found_links:
            print(f"Found links containing '{keyword}':")
            for found_link in found_links:
                print(found_link)
        else:
            print(f"No links found containing '{keyword}'.")
    else:
        print(f"Failed to retrieve the page at {url}.")


url = input("Enter the URL to search: ")
keyword = input("Enter the keyword to filter links: ")
search_for_keyword(url, keyword)


time.sleep(5)  
