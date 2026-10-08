SELECT d.subject_name, s.name, ROUND(AVG(m.score), 2) as mark FROM marks m
JOIN students s ON m.student_id = s.id
JOIN subjects d ON m.subject_id = d.id
WHERE d.id = 1
ORDER BY mark DESC
LIMIT 1;