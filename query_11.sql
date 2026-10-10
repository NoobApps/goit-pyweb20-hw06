SELECT t.teacher_name,p.name, round(avg(m.score),2) AS averageScore
FROM teachers t
JOIN subjects s ON s.teacher_id=t.id
JOIN marks m ON m.subject_id=s.id
JOIN students p ON p.id=m.student_id
WHERE t.id=1 AND p.id=1;