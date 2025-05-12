# Scraping de Noticias de Tecnología BBC

Este proyecto realiza el scraping de artículos de la sección de tecnología de la BBC, almacenando los resultados tanto en una base de datos SQLite como en archivos CSV. El objetivo principal es mantener un registro histórico de noticias tecnológicas, evitando la inserción de duplicados y asegurando la organización de los archivos generados.

## Características principales

- **Extracción automática** de artículos de tecnología desde la BBC.
- **Almacenamiento estructurado** en una base de datos SQLite, con control de duplicados mediante un índice único en el campo `link`.
- **Exportación de artículos** a archivos CSV, con cada ejecución generando un archivo nuevo con marca de tiempo.
- **Organización de archivos generados** en la carpeta `ArchivosGenerados` (tanto CSV como la base de datos).
- **Pipeline automatizado** mediante GitHub Actions, que ejecuta el scraping y sube los archivos generados como artifacts en cada push o pull request.

## Estructura del proyecto

- `main.py`: Orquesta el flujo de extracción, transformación, validación y almacenamiento de los artículos.
- `scraper.py`: Contiene la lógica de scraping web.
- `database.py`: Maneja la conexión y operaciones con la base de datos SQLite.
- `file_operations.py`: Genera y guarda los archivos CSV.
- `models.py`: Define las estructuras de datos utilizadas.
- `ArchivosGenerados/`: Carpeta donde se guardan los archivos generados (CSV y base de datos).
- `.github/workflows/generate-artifacts.yml`: Workflow de GitHub Actions para automatizar la ejecución y publicación de artifacts.

## ¿Cómo ejecutar?

1. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
2. Ejecuta el pipeline:
   ```
   python main.py
   ```
3. Los archivos generados estarán en la carpeta `ArchivosGenerados`.

## Automatización en GitHub

Cada vez que se hace un push, pull request o ejecución manual del workflow, GitHub Actions:
- Instala las dependencias.
- Ejecuta el scraping.
- crea un commit nuevo en nuestro repositorio.

---

