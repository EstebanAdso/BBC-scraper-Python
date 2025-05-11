import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
from typing import Optional, List
from models import Article
from database import DatabaseManager
from file_operations import FileManager

class BBCScraper:
    def __init__(self):
        self.BASE_URL = "https://www.bbc.com"
        self.TECH_URL = f"{self.BASE_URL}/news/technology"
        self.HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def extract(self) -> Optional[str]:
        print(" Extracting data from BBC Technology...")
        try:
            response = requests.get(self.TECH_URL, headers=self.HEADERS, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Extraction error: {e}")
            return None
    
    def transform(self, html_content: str) -> List[Article]:
        print(" Transforming data...")
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []
        
        news_containers = soup.find_all('div', {'data-testid': 'edinburgh-card'}) or \
                         soup.find_all('div', class_='ssrcss-1f3bvyz-Stack')
        
        for container in news_containers:
            try:
                title = container.find('h2').get_text(strip=True) if container.find('h2') else "No title"
                
                link = "#"
                link_tag = container.find('a', href=True)
                if link_tag:
                    link = urljoin(self.BASE_URL, link_tag['href'])
                
                summary = container.find('p').get_text(strip=True) if container.find('p') else "No summary"
                
                articles.append(Article(
                    title=title,
                    summary=summary,
                    link=link,
                    date=datetime.now().strftime('%Y-%m-%d')
                ))
            except Exception as e:
                print(f"Error processing article: {e}")
                continue
        
        return articles
    
    def validate(self, articles: List[Article]) -> List[Article]:
        print(" Validating data...")
        valid_articles = []
        
        for article in articles:
            if article.title and article.title != "No title" and article.date:
                valid_articles.append(article)
            else:
                print(f"Invalid article discarded: {article.title}")
        
        print(f"Valid articles: {len(valid_articles)}/{len(articles)}")
        return valid_articles