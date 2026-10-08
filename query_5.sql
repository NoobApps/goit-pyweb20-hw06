SELECT s.subject_name, t.teacher_name FROM subjects s 
JOIN teachers t on s.teacher_id=t.id
WHERE teacher_id=1;