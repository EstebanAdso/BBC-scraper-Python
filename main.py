from scraper import BBCScraper
from database import DatabaseManager
from file_operations import FileManager

def run_pipeline():
    # Initialize components
    scraper = BBCScraper()
    db_manager = DatabaseManager()
    
    # 1. Extraction
    html_content = scraper.extract()
    if not html_content:
        return None
    
    # 2. Transformation
    raw_data = scraper.transform(html_content)
    
    # 3. Validation
    clean_data = scraper.validate(raw_data)
    
    # 4. Storage
    # Save to CSV
    csv_file = FileManager.create_csv(clean_data)
    
    # Save to database
    db_manager.store_articles(clean_data)

    # Print all articles
    db_manager.print_all_articles()
    
    # Read from database (optional)
    db_content = db_manager.read_all_articles()
    print(f"Total articles in database: {len(db_content)}")
    
    return {
        'csv_file': csv_file,
        'db_content': db_content
    }

if __name__ == "__main__":
    results = run_pipeline()
    
    if results:
        print("\n🎉 Pipeline executed successfully!")
        print(f"CSV file generated: {results.get('csv_file', 'N/A')}")
        print(f"Database records: {len(results['db_content'])}")