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

## Deployment (Detailed)

### Streamlit Community Cloud
1. Go to https://share.streamlit.io/ and sign in.
2. Click 'New app', select your repo and branch.
3. In 'Advanced settings', add your MySQL credentials as secrets:
   - `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`, `MYSQL_PORT`
4. Deploy. The app will auto-create tables on first run.
5. Ensure your MySQL instance is accessible from the cloud (public IP, correct firewall rules).

### AWS EC2/Elastic Beanstalk
1. Launch an EC2 instance (Ubuntu recommended) or Elastic Beanstalk Python app.
2. SSH in and clone your repo.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set environment variables in your shell or via `.env` file:
   ```bash
   export MYSQL_HOST=your-host
   export MYSQL_USER=your-user
   export MYSQL_PASSWORD=your-password
   export MYSQL_DB=optimizer_db
   export MYSQL_PORT=3306
   ```
5. Run the app:
   ```bash
   streamlit run app.py --server.port 80
   ```
6. Open the public IP in your browser.

### SQL DDL for Manual DB Setup
```sql
CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(128) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE project_summaries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT UNIQUE,
    total_routes INT,
    total_drivers INT,
    total_dead_km FLOAT,
    optimized_dead_km FLOAT,
    swap_chains INT,
    deviations INT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE TABLE project_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    driver VARCHAR(64),
    pickup_point VARCHAR(128),
    lat FLOAT,
    lon FLOAT,
    original_dead_km FLOAT,
    optimized_dead_km FLOAT,
    swap_chain VARCHAR(64),
    deviation FLOAT,
    UNIQUE KEY _project_driver_pickup_uc (project_id, driver, pickup_point),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

## Notes
- Tables are auto-created on first run.
- All color and style requirements are in `style.css`.
- Example CSV: `sample_project.csv`
- For any issues, check database connectivity and environment variables.