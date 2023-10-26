###========================star schema
fact_call_log = """"
CREATE TABLE IF NOT EXISTS "fact_call_log" (
    "id" SERIAL PRIMARY KEY,
    "call_id" INT UNIQUE NOT NULL,
    "agent_id" INT NOT NULL,
    "compliant" VARCHAR(255) NOT NULL,
    "resolution_duration_in_hours" INT NOT NULL,
    "assigned_to" DECIMAL(8, 2) NOT NULL,
    "status_id" INT NOT NULL
);
 """

dim_call = '''
CREATE TABLE IF NOT EXISTS "dim_call" (
    "call_id" SERIAL PRIMARY KEY,
    "call_type" VARCHAR(255) NOT NULL,
    "call_duration_in_seconds" INT NOT NULL,
    "call_ended_by_agent" BOOLEAN NOT NULL
);
'''

dim_status = '''
CREATE TABLE IF NOT EXISTS "dim_status" (
    "status_id" SERIAL PRIMARY KEY,
    "status" VARCHAR(255) NOT NULL
);
'''

dim_agent = '''
CREATE TABLE IF NOT EXISTS "dim_agent" (
    "agent_id" SERIAL PRIMARY KEY,
    "grade_level" VARCHAR(255) NOT NULL
);
'''


ALTER TABLE "fact_call_log" ADD CONSTRAINT "fact_call_log_agent_id_foreign" FOREIGN KEY ("agent_id") REFERENCES "dim_agent" ("agent_id");
ALTER TABLE "fact_call_log" ADD CONSTRAINT "fact_call_log_compliant_foreign" FOREIGN KEY ("compliant") REFERENCES "dim_status" ("status_id");
ALTER TABLE "fact_call_log" ADD CONSTRAINT "fact_call_log_call_id_foreign" FOREIGN KEY ("call_id") REFERENCES "dim_call" ("call_id");

#====================================== TRANSFORMED KPI

calls_resolved_vs_received = """
CREATE TABLE calls_resolved_vs_received (
    agent_id VARCHAR(10),
    total_calls_received INT,
    total_calls_resolved INT
);
"""

calls_received_vs_assigned_resolved = """
CREATE TABLE calls_received_vs_assigned_resolved (
    agent_id VARCHAR(10),
    total_calls_received INT,
    total_calls_assigned_resolved INT
);
"""

call_duration_per_agent = """
CREATE TABLE call_duration_per_agent (
    agent_id VARCHAR(10),
    total_call_duration INT,
    average_call_duration FLOAT,
    grade_level VARCHAR(1)
);
"""


raw_data_schema = [fact_call_log, dim_call, dim_status, dim_agent]
transformed_kpi = [calls_resolved_vs_received, calls_received_vs_assigned_resolved, call_duration_per_agent]
