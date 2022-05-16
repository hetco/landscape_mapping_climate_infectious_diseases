select distinct institute_name,institute.institute_id,paper.paper_id from institute
join department_institute on department_institute.institute_id = institute.institute_id
join paper_department on department_institute.department_id = paper_department.department_id
join paper on paper.paper_id = paper_department.paper_id
where reviewed
in (
'R/T?',
'R',
'R ',
'R /T?',
'T?',
'T',
'R T?',
'R/T',
'review paper',
'R',
'T? / N?',
'CT?',
'T/R',
'R/N',
'review'		
)
order by paper.paper_id