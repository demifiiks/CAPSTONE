###========================star schema

schema = """
CREATE SCHEMA IF NOT EXISTS {};
"""

fact_call_log = """
CREATE TABLE IF NOT EXISTS staging.fact_call_log (
    id SERIAL PRIMARY KEY,
    call_id INT NOT NULL,
    agent_id INT NOT NULL,
    complaint VARCHAR(255) NOT NULL,
    resolution_duration_in_hours INT NOT NULL,
    assigned_to DECIMAL(8, 2) NOT NULL,
    status_id INT NOT NULL,
    UNIQUE (call_id),
    FOREIGN KEY (agent_id) REFERENCES staging.dim_agent (agent_id),
    FOREIGN KEY (complaint) REFERENCES staging.dim_status (status_id),
    FOREIGN KEY (call_id) REFERENCES staging.dim_call (call_id)
);
"""

dim_call ="""
CREATE TABLE IF NOT EXISTS staging.dim_call (
    call_id SERIAL PRIMARY KEY,
    call_type VARCHAR(255) NOT NULL,
    call_duration_in_seconds INT NOT NULL,
    call_ended_by_agent BOOLEAN NOT NULL
);
"""

dim_status = """
CREATE TABLE IF NOT EXISTS staging.dim_status (
    status_id SERIAL PRIMARY KEY,
    status VARCHAR(255) NOT NULL
);
"""

dim_agent = """
CREATE TABLE IF NOT EXISTS staging.dim_agent (
    agent_id SERIAL PRIMARY KEY,
    grade_level VARCHAR(255) NOT NULL
);
"""

#====================================== TRANSFORMED KPI


calls_resolved_vs_received = """
CREATE TABLE IF NOT EXISTS transform.calls_resolved_vs_received (
    agent_id VARCHAR(10),
    total_calls_received INT,
    total_calls_resolved INT
);
"""

calls_received_vs_assigned_resolved = """
CREATE TABLE IF NOT EXISTS transform.calls_received_vs_assigned_resolved (
    agent_id VARCHAR(10),
    total_calls_received INT,
    total_calls_assigned_resolved INT
);
"""

call_duration_per_agent = """
CREATE TABLE IF NOT EXISTS transform.call_duration_per_agent (
    agent_id VARCHAR(10),
    total_call_duration INT,
    average_call_duration FLOAT,
    grade_level VARCHAR(1)
);
"""


raw_data_schema = [fact_call_log, dim_call, dim_status, dim_agent]

transformed_kpi = [calls_resolved_vs_received, calls_received_vs_assigned_resolved, call_duration_per_agent]
