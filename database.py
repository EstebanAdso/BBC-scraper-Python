import sqlite3
from sqlite3 import Error
from typing import List
from models import Article

class DatabaseManager:
    def __init__(self, db_name: str = "bbc_sqlite.db"):
        import os
        output_dir = os.path.join(os.path.dirname(__file__), 'ArchivosGenerados')
        os.makedirs(output_dir, exist_ok=True)
        self.DB_NAME = os.path.join(output_dir, db_name)
        self.TABLE_NAME = "tech_articles"
        print(f"[DatabaseManager] Base de datos en: {os.path.abspath(self.DB_NAME)}")
        self._init_db()
    
    def _init_db(self):
        """Initialize the SQLite database and create table if not exists"""
        try:
            with sqlite3.connect(self.DB_NAME) as conn:
                cursor = conn.cursor()
                
                create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    summary TEXT,
                    link TEXT UNIQUE,
                    date TEXT NOT NULL,
                    source TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                );
                """
                cursor.execute(create_table_query)
                cursor.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_link ON {self.TABLE_NAME}(link)")
                conn.commit()
        except Error as e:
            print(f"Error initializing database: {e}")
    
    def store_articles(self, articles: List[Article]):
        """Store only new articles in SQLite database (no duplicados por link)"""
        try:
            with sqlite3.connect(self.DB_NAME) as conn:
                cursor = conn.cursor()
                
                insert_query = f"""
                INSERT OR IGNORE INTO {self.TABLE_NAME} (title, summary, link, date, source)
                VALUES (?, ?, ?, ?, ?)
                """
                nuevos = 0
                for article in articles:
                    cursor.execute(insert_query, (
                        article.title,
                        article.summary,
                        article.link,
                        article.date,
                        article.source
                    ))
                    if cursor.rowcount > 0:
                        nuevos += 1
                
                conn.commit()
                print(f"✅ Data stored in SQLite ({self.DB_NAME}.{self.TABLE_NAME})")
                print(f"Total records inserted: {nuevos}")
                
        except Error as e:
            print(f"Error storing in SQLite: {e}")
    
    def read_all_articles(self) -> List[dict]:
        """Read all articles from the database"""
        try:
            with sqlite3.connect(self.DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {self.TABLE_NAME}")
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Error as e:
            print(f"Error reading from database: {e}")
            return []

    def print_all_articles(self, limit: int = None):
        """Muestra todos los artículos en la consola con formato"""
        articles = self.read_all_articles()
        
        if not articles:
            print("No hay artículos en la base de datos")
            return
            
        print("\n📄 Contenido completo de la base de datos:")
        print("-" * 100)
        print(f"| {'ID':<4} | {'Fecha':<10} | {'Título':<40} | {'Resumen':<40} |")
        print("-" * 100)
        
        for idx, article in enumerate(articles[:limit], 1):
            print(f"| {article['id']:<4} | {article['date']:<10} | {article['title'][:40]:<40} | {article['summary'][:40]:<40} |")
        
        print("-" * 100)
        print(f"Total de registros: {len(articles)}")