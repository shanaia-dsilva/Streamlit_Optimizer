# SciPy_OSRM - VRP solver

#### Jupyter Notebook files only, direct saving back to csv files
##### no frontend

Route optimization project to minimize dead kilometers
-Distance matrix from osrm
-Hungarian algorithm for optimization
-data preprocessing using haversine distance

# Streamlit Optimization Dashboard

## Features
- Upload CSVs for new optimization projects
- Store and analyze project data in MySQL
- Interactive dashboard, charts, maps, and tables
- Download project data and summaries

## Setup

1. **Clone the repo and install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up MySQL database:**
   - Create a database (e.g., `optimizer_db`).
   - Set credentials in a `.env` file (see `.env.example`):
     ```
     MYSQL_HOST=localhost
     MYSQL_USER=youruser
     MYSQL_PASSWORD=yourpassword
     MYSQL_DB=optimizer_db
     MYSQL_PORT=3306
     ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Deployment

- **Streamlit Community Cloud:**
  - Add your `.env` variables in the "Secrets" section.
  - Upload all project files.
- **AWS/Other Cloud:**
  - Set environment variables in your deployment environment.
  - Ensure MySQL is accessible from your app.

## Notes
- Tables are auto-created on first run.
- All color and style requirements are in `style.css`.
- Example CSV: `sample_project.csv`
- For any issues, check database connectivity and environment variables.