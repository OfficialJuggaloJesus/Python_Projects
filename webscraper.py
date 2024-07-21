import requests
from bs4 import BeautifulSoup

# URL of the website you want to scrape
url = 'https://www.coinabk.com'

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all <a> tags (which define hyperlinks)
    links = soup.find_all('a')
    
    # Iterate over all found <a> tags
    for link in links:
        # Get the href attribute of each link
        href = link.get('href')
        
        # Print the link if the href attribute exists
        if href:
            print(href)
else:
    # Print an error message if the request was not successful
    print(f'Failed to retrieve page: {response.status_code}')
