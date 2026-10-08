SELECT s.name, d.subject_name
FROM students s
JOIN marks m ON m.student_id = s.id
JOIN subjects d ON d.id = m.subject_id
WHERE s.id = 1
GROUP BY d.id
ORDER BY d.subject_name;