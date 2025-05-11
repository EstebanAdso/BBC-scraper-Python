import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import pandas as pd
from urllib.parse import urljoin
import sqlite3
from sqlite3 import Error

class BBCScraper:
    def __init__(self):
        self.BASE_URL = "https://www.bbc.com"
        self.TECH_URL = f"{self.BASE_URL}/news/technology"
        self.HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.DB_NAME = "bbc_sqlite.db"
        self.TABLE_NAME = "tech_articles"
        
        # Inicializar la base de datos
        self._init_db()
    
    def _init_db(self):
        """Inicializa la base de datos SQLite y crea la tabla si no existe"""
        try:
            conn = sqlite3.connect(self.DB_NAME)
            cursor = conn.cursor()
            
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                summary TEXT,
                link TEXT,
                date TEXT NOT NULL,
                source TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_table_query)
            conn.commit()
            conn.close()
        except Error as e:
            print(f"Error al inicializar la base de datos: {e}")
    
    # Etapa 1: Extracción
    def extract(self):
        print("🔍 Extrayendo datos de BBC Technology...")
        try:
            response = requests.get(self.TECH_URL, headers=self.HEADERS, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error en extracción: {e}")
            return None
    
    # Etapa 2: Transformación
    def transform(self, html_content):
        print("🔄 Transformando datos...")
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []
        
        # Buscar contenedores de noticias
        news_containers = soup.find_all('div', {'data-testid': 'edinburgh-card'}) or \
                         soup.find_all('div', class_='ssrcss-1f3bvyz-Stack')
        
        for container in news_containers[:15]:  # Limitar a 15 artículos
            try:
                title = container.find('h2').get_text(strip=True) if container.find('h2') else "Sin título"
                
                # Extraer enlace si existe
                link = "#"
                link_tag = container.find('a', href=True)
                if link_tag:
                    link = urljoin(self.BASE_URL, link_tag['href'])
                
                summary = container.find('p').get_text(strip=True) if container.find('p') else "Sin resumen"
                
                articles.append({
                    'title': title,
                    'summary': summary,
                    'link': link,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'BBC Technology'
                })
            except Exception as e:
                print(f"Error procesando artículo: {e}")
                continue
        
        return articles
    
    # Etapa 3: Validación
    def validate(self, articles):
        print("✅ Validando datos...")
        valid_articles = []
        required_fields = ['title', 'summary', 'date']
        
        for article in articles:
            if all(field in article and article[field] for field in required_fields):
                valid_articles.append(article)
            else:
                print(f"Artículo inválido descartado: {article.get('title', 'Sin título')}")
        
        print(f"Artículos válidos: {len(valid_articles)}/{len(articles)}")
        return valid_articles
    
    # Etapa 4: Almacenamiento
    def store(self, data, format='csv'):
        print("💾 Almacenando datos...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        output_file = None
        
        if format == 'csv':
            filename = f"bbc_tech_{timestamp}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print(f"Datos guardados en {filename}")
            output_file = filename
        
        elif format == 'dataframe':
            return pd.DataFrame(data)
        
        # Almacenar en SQLite
        self._store_to_sqlite(data)
        
        return output_file
    
    def _store_to_sqlite(self, data):
        """Almacena los artículos en la base de datos SQLite"""
        try:
            conn = sqlite3.connect(self.DB_NAME)
            cursor = conn.cursor()
            
            insert_query = f"""
            INSERT INTO {self.TABLE_NAME} (title, summary, link, date, source)
            VALUES (?, ?, ?, ?, ?)
            """
            
            for article in data:
                cursor.execute(insert_query, (
                    article['title'],
                    article['summary'],
                    article['link'],
                    article['date'],
                    article['source']
                ))
            
            conn.commit()
            print(f"✅ Datos almacenados en SQLite ({self.DB_NAME}.{self.TABLE_NAME})")
            print(f"Total registros insertados: {len(data)}")
            
        except Error as e:
            print(f"Error al almacenar en SQLite: {e}")
        finally:
            if conn:
                conn.close()
    
    # Etapa 5: Análisis (opcional)
    def analyze(self, data):
        print("📊 Analizando datos...")
        df = pd.DataFrame(data)
        
        print("\nResumen estadístico:")
        print(f"- Total artículos: {len(df)}")
        print(f"- Palabras promedio en títulos: {df['title'].apply(lambda x: len(x.split())).mean():.1f}")
        print(f"- Artículos con resumen: {df[df['summary'] != 'Sin resumen'].shape[0]}")
        
        return df
    
    # Ejecutar pipeline completo
    def run_pipeline(self):
        # 1. Extracción
        html_content = self.extract()
        if not html_content:
            return None
        
        # 2. Transformación
        raw_data = self.transform(html_content)
        
        # 3. Validación
        clean_data = self.validate(raw_data)
        
        # 4. Almacenamiento
        output_file = self.store(clean_data)
        
        # 5. Análisis (opcional)
        analysis_result = self.analyze(clean_data)
        
        return {
            'raw_data': raw_data,
            'clean_data': clean_data,
            'output_file': output_file,
            'analysis': analysis_result
        }

# Ejecutar el pipeline
if __name__ == "__main__":
    pipeline = BBCScraper()
    results = pipeline.run_pipeline()
    
    if results:
        print("\n🎉 Pipeline ejecutado con éxito!")
        print(f"Artículos extraídos: {len(results['clean_data'])}")
        print(f"Archivo CSV generado: {results.get('output_file', 'N/A')}")
        print(f"Datos almacenados en SQLite: bbc_articles.db.tech_articles")