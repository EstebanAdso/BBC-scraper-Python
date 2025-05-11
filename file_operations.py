import csv
from datetime import datetime
from typing import List
from models import Article

class FileManager:
    @staticmethod
    def create_csv(articles: List[Article]) -> str:
        print(" Creating CSV file...")
        import os
        output_dir = os.path.join(os.path.dirname(__file__), 'ArchivosGenerados')
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        filename = f"bbc_tech_{timestamp}.csv"
        filepath = os.path.join(output_dir, filename)
        
        if not articles:
            print("No articles to save")
            return ""
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=articles[0].to_dict.keys())
            writer.writeheader()
            writer.writerows([article.to_dict for article in articles])
        
        print(f"Data saved in {filepath}")
        return filepath