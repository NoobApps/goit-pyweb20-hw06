SELECT d.subject_name, g.group_name, ROUND(AVG(m.score), 1) AS AverageMark
FROM groups g
JOIN students s ON g.id = s.group_id
JOIN marks m ON s.id = m.student_id
JOIN subjects d ON d.id = m.subject_id
WHERE d.id = 1
GROUP BY g.id;