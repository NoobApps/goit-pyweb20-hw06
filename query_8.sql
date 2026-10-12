SELECT t.teacher_name, round(avg(m.score),2) AS averageScore
FROM marks m
JOIN subjects s ON s.id=m.subject_id
JOIN teachers t ON s.teacher_id=t.id
WHERE t.id=4;--not every teacher has subjects because of random assignment