SELECT d.subject_name, m.score,s.name,g.group_name, m.date
FROM subjects d
JOIN marks m ON d.id=m.subject_id
JOIN students s ON s.id=m.student_id
JOIN groups g ON g.id=s.group_id
WHERE d.id=1 AND g.id=2
GROUP BY s.id
HAVING max(m.date)
ORDER BY s.name, m.id DESC;