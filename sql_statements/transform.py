calls_resolved_vs_received = '''
INSERT INTO calls_resolved_vs_received (agent_id, total_calls_received, total_calls_resolved)
SELECT
    cd.agents_grade_level AS agent_id,
    COUNT(cd.call_id) AS total_calls_received,
    COUNT(cl.id) AS total_calls_resolved
FROM
    new_call_details AS cd
LEFT JOIN
    new_call_log AS cl
ON
    cd.call_id = cl.id
WHERE
    cl.status = 'CLOSED'
GROUP BY
    cd.agents_grade_level;
'''

calls_received_vs_assigned_resolved = '''
INSERT INTO calls_received_vs_assigned_resolved (agent_id, total_calls_received, total_calls_assigned_resolved)
SELECT
    cd.agents_grade_level AS agent_id,
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
    cd.agents_grade_level;
'''

call_duration_per_agent = '''
INSERT INTO call_duration_per_agent (agent_id, total_call_duration, average_call_duration, grade_level)
SELECT
    cd.agents_grade_level AS agent_id,
    SUM(cd.duration_of_call_in_sec) AS total_call_duration,
    AVG(cd.duration_of_call_in_sec) AS average_call_duration,
    cd.agents_grade_level
FROM
    new_call_details AS cd
GROUP BY
    cd.agents_grade_level;
'''

transformed_kpi = [calls_resolved_vs_received, calls_received_vs_assigned_resolved, call_duration_per_agent]