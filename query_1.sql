SELECT s.name , round(avg(score),3) AS average_score FROM marks m 
JOIN students s ON m.student_id=s.id
GROUP BY m.student_id 
ORDER by average_score DESC 
LIMIT 5;