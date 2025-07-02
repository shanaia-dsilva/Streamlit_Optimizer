<<<<<<< HEAD
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
=======
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
>>>>>>> d3f6fb7d51a260ae1366c1d54cb2e1143dc7d9d3
); 