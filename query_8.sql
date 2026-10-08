SELECT t.teacher_name,s.subject_name, round(avg(m.score),2) AS averageScore
FROM teachers t
JOIN subjects s ON s.teacher_id=t.id
JOIN marks m ON m.subject_id=s.id
WHERE t.id=1
GROUP BY s.id
ORDER BY s.subject_name;