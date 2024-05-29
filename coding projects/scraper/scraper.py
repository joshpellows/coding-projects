import requests
from bs4 import BeautifulSoup
import csv

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Example: Scraping article titles and links from a blog
    articles = soup.find_all('article')
    data = []
    for article in articles:
        title = article.find('h2').text
        link = article.find('a')['href']
        data.append([title, link])
    
    return data

def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link'])
        writer.writerows(data)

if __name__ == "__main__":
    url = 'https://example-blog.com'
    data = scrape_website(url)
    save_to_csv(data, 'articles.csv')
    print("Data saved to articles.csv")
