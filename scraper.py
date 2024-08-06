import requests
from bs4 import BeautifulSoup
import csv

def get_article_urls(base_url, num_pages):
    article_urls = []
    for page_num in range(1, num_pages + 1):
        url = f"{base_url}/page/{page_num}/"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('h2', class_='entry-title')
            for article in articles:
                article_link = article.find('a')['href']
                article_urls.append(article_link)
    return article_urls

def get_article_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        content_element = soup.find('div', class_='entry-content')
        if content_element:
            content = content_element.get_text(separator='\n').strip()
            return content
    return ''

def output_csv(content, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Content'])
        writer.writerow([content])
    print(f'Saved to {filename}.')

def extract_and_save_content(article_urls):
    for index, url in enumerate(article_urls, start=1):
        article_content = get_article_content(url)
        if article_content:
            filename = f'article_{index}.csv'
            output_csv(article_content, filename)
            print(f"Content of article {index} extracted and saved successfully.")
        else:
            print(f"Failed to extract content for article {index}.")

if __name__ == "__main__":
    base_url = "https://mikrobotik.com/wp2"
    num_pages = 11
    article_urls = get_article_urls(base_url, num_pages)
    extract_and_save_content(article_urls)
