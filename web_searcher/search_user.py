import requests
from bs4 import BeautifulSoup

def search_yahoo(keyword):
    url = f"https://search.yahoo.com/search?p={keyword}"
    response = requests.get(url)
    if response.status_code == 200: 
        # 200 means sucess
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a', href=True):
            # Filtering out ads or unrelated links
            if "yahoo.com" not in link['href'] and not link['href'].startswith("/"):
                print(link['href'])
    else:
        print("Failed to retrieve the page.")

# Example usage
keyword = input("Enter keyword to search on Yahoo: ")
search_yahoo(keyword)
