calls_resolved_vs_received = '''
    INSERT INTO transformed.calls_resolved_vs_received (agent_id, total_calls_received, total_calls_resolved)
    SELECT agent_id, 
       COUNT(*)AS total_calls_received,
       COUNT(*) FILTER (WHERE status = 'Resolved') AS total_calls_resolved
    FROM new_call_log
    GROUP BY agent_id;
'''

calls_received_vs_assigned_resolved = '''
INSERT INTO transformed.calls_received_vs_assigned_resolved (agent_id, total_calls_received, total_calls_assigned_resolved)
SELECT
    cl.agent_id AS agent_id,
    COUNT(cd.call_id) AS total_calls_received,
    COUNT(cl.id) AS total_calls_assigned_resolved
FROM
    new_call_details AS cd
LEFT JOIN
    new_call_log AS cl
ON
    cd.call_id = cl.id
WHERE
    cl.status IN ('CLOSED', 'RESOLVED')
GROUP BY
    cl.agent_id;
'''

call_duration_per_agent = '''
INSERT INTO transformed.call_duration_per_agent (agent_id, total_call_duration, average_call_duration, grade_level)
SELECT
    cl.agent_id AS agent_id,
    SUM(cl.resolution_duration_in_hours) AS total_call_duration,
    AVG(cl.resolution_duration_in_hours) AS average_call_duration,
    cd.agents_grade_level
FROM
    new_call_details AS cd
GROUP BY
    cl.agent_id;
'''

insert_into_transformed_kpi = [calls_resolved_vs_received, calls_received_vs_assigned_resolved, call_duration_per_agent]

