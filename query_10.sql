SELECT t.teacher_name, s.name as student_name,d.subject_name 
FROM teachers t
JOIN subjects d ON d.teacher_id=t.id
JOIN marks m ON  m.subject_id=d.id
JOIN students s ON s.id=m.student_id
WHERE t.id=4 AND s.id=1
GROUP BY d.id
ORDER BY d.subject_name;