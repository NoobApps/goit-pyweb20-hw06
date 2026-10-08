SELECT d.subject_name, g.group_name, s.name, m.score
FROM groups g
JOIN students s ON s.group_id = g.id
JOIN marks m ON m.student_id = s.id
JOIN subjects d ON d.id = m.subject_id
WHERE d.id = 1 AND g.id = 1
ORDER BY m.score DESC;