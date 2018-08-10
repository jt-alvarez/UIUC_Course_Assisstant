USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///uiuc-gpa-dataset.csv" AS row
MERGE(:Subject {subjectName:row.Subject})
MERGE(:SubjectLevel {subject:row.Subject, level:100})
MERGE(:SubjectLevel {subject:row.Subject, level:200})
MERGE(:SubjectLevel {subject:row.Subject, level:300})
MERGE(:SubjectLevel {subject:row.Subject, level:400})
MERGE(:SubjectLevel {subject:row.Subject, level:500})
MERGE(:Course {course:row.Subject + row.Number, title:row.Course_Title, subject:row.Subject, num:toInt(row.Number)});


MERGE(:SubjectLevel {subject:"all", level:100});
MERGE(:SubjectLevel {subject:"all", level:200});
MERGE(:SubjectLevel {subject:"all", level:300});
MERGE(:SubjectLevel {subject:"all", level:400});
MERGE(:SubjectLevel {subject:"all", level:500});


CREATE INDEX ON :Subject(subjectName);
CREATE INDEX ON :Course(course);
CREATE INDEX ON :Course(num);
CREATE INDEX ON :SubjectLevel(level);
CREATE INDEX ON :SubjectLevel(subject);


USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///avg-gpa-dataset.csv" AS row
MATCH(course:Course {course:row.Subject + row.Number, title:row.Course_Title, subject:row.Subject, num:toInt(row.Number)})
SET course.avg_gpa = row.avg_gpa;


MATCH (SID:Subject),(CID:Course)
WHERE SID.subjectName = CID.subject
MERGE (SID)-[:SUB_TO_COR]->(CID);


MATCH (S:Subject),(SL:SubjectLevel)
WHERE S.subjectName = SL.subject AND SL.level = 100
MERGE (S)-[:LVL100]->(SL);


MATCH (S:Subject),(SL:SubjectLevel)
WHERE S.subjectName = SL.subject AND SL.level = 200
MERGE (S)-[:LVL200]->(SL);


MATCH (S:Subject),(SL:SubjectLevel)
WHERE S.subjectName = SL.subject AND SL.level = 300
MERGE (S)-[:LVL300]->(SL);


MATCH (S:Subject),(SL:SubjectLevel)
WHERE S.subjectName = SL.subject AND SL.level = 400
MERGE (S)-[:LVL400]->(SL);


MATCH (S:Subject),(SL:SubjectLevel)
WHERE S.subjectName = SL.subject AND SL.level = 500
MERGE (S)-[:LVL500]->(SL);


MATCH (SL:SubjectLevel), (C:Course)
WHERE SL.subject = C.subject AND SL.level = 100 AND C.num > 99 AND C.num < 200
MERGE (SL)-[:IS_100]->(C);


MATCH (SL:SubjectLevel), (C:Course)
WHERE SL.subject = C.subject AND SL.level = 200 AND C.num > 199 AND C.num < 300
MERGE (SL)-[:IS_200]->(C);


MATCH (SL:SubjectLevel), (C:Course)
WHERE SL.subject = C.subject AND SL.level = 300 AND C.num > 299 AND C.num < 400
MERGE (SL)-[:IS_300]->(C);


MATCH (SL:SubjectLevel), (C:Course)
WHERE SL.subject = C.subject AND SL.level = 400 AND C.num > 399 AND C.num < 500
MERGE (SL)-[:IS_400]->(C);


MATCH (SL:SubjectLevel), (C:Course)
WHERE SL.subject = C.subject AND SL.level = 500 AND C.num > 499 AND C.num < 600
MERGE (SL)-[:IS_500]->(C);


MATCH (SL:SubjectLevel), (C:Course)
WHERE SL.subject = "all" AND SL.level = 100 AND C.num > 99 AND C.num < 200
MERGE (SL)-[:IS_100]->(C);


MATCH (SL:SubjectLevel), (C:Course)
WHERE SL.subject = "all" AND SL.level = 200 AND C.num > 199 AND C.num < 300
MERGE (SL)-[:IS_200]->(C);


MATCH (SL:SubjectLevel), (C:Course)
WHERE SL.subject = "all" AND SL.level = 300 AND C.num > 299 AND C.num < 400
MERGE (SL)-[:IS_300]->(C);


MATCH (SL:SubjectLevel), (C:Course)
WHERE SL.subject = "all" AND SL.level = 400 AND C.num > 399 AND C.num < 500
MERGE (SL)-[:IS_400]->(C);


MATCH (SL:SubjectLevel), (C:Course)
WHERE SL.subject = "all" AND SL.level = 500 AND C.num > 499 AND C.num < 600
MERGE (SL)-[:IS_500]->(C);


USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///prof-gpa-dataset.csv" AS row
MERGE(:Professor {prof:row.Primary_Instructor});


USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///prof-gpa-dataset.csv" AS row
MERGE(:ProfessorLevel {prof_level:row.Primary_Instructor + " 100", prof:row.Primary_Instructor, level:100});
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///prof-gpa-dataset.csv" AS row
MERGE(:ProfessorLevel {prof_level:row.Primary_Instructor + " 200", prof:row.Primary_Instructor, level:200});
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///prof-gpa-dataset.csv" AS row
MERGE(:ProfessorLevel {prof_level:row.Primary_Instructor + " 300", prof:row.Primary_Instructor, level:300});
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///prof-gpa-dataset.csv" AS row
MERGE(:ProfessorLevel {prof_level:row.Primary_Instructor + " 400", prof:row.Primary_Instructor, level:400});
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///prof-gpa-dataset.csv" AS row
MERGE(:ProfessorLevel {prof_level:row.Primary_Instructor + " 500", prof:row.Primary_Instructor, level:500});


MATCH (P:Professor), (PL:ProfessorLevel)
WHERE P.prof = PL.prof AND PL.level = 100
MERGE (P)-[:LVL100]->(PL);
MATCH (P:Professor), (PL:ProfessorLevel)
WHERE P.prof = PL.prof AND PL.level = 200
MERGE (P)-[:LVL200]->(PL);
MATCH (P:Professor), (PL:ProfessorLevel)
WHERE P.prof = PL.prof AND PL.level = 300
MERGE (P)-[:LVL300]->(PL);
MATCH (P:Professor), (PL:ProfessorLevel)
WHERE P.prof = PL.prof AND PL.level = 400
MERGE (P)-[:LVL400]->(PL);
MATCH (P:Professor), (PL:ProfessorLevel)
WHERE P.prof = PL.prof AND PL.level = 500
MERGE (P)-[:LVL500]->(PL);


USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///prof-gpa-dataset.csv" AS row
MERGE(:ProfRecord {course:row.Subject + row.Number, title:row.Course_Title, subject:row.Subject, num:toInt(row.Number), prof:row.Primary_Instructor, avg_gpa:row.avg_prof_gpa});


MATCH (P:Professor),(PR:ProfRecord)
WHERE P.prof = PR.prof
MERGE (P)-[:INSTRUCTS]->(PR);


MATCH (PL:ProfessorLevel), (PR:ProfRecord)
WHERE PL.prof = PR.prof AND PL.level = 100 AND PR.num > 99 AND PR.num < 200
MERGE (PL)-[:IS_100]->(PR);

MATCH (PL:ProfessorLevel), (PR:ProfRecord)
WHERE PL.prof = PR.prof AND PL.level = 200 AND PR.num > 199 AND PR.num < 300
MERGE (PL)-[:IS_200]->(PR);

MATCH (PL:ProfessorLevel), (PR:ProfRecord)
WHERE PL.prof = PR.prof AND PL.level = 300 AND PR.num > 299 AND PR.num < 400
MERGE (PL)-[:IS_300]->(C);

MATCH (PL:ProfessorLevel), (PR:ProfRecord)
WHERE PL.prof = PR.prof AND PL.level = 400 AND PR.num > 399 AND PR.num < 500
MERGE (PL)-[:IS_400]->(PR);

MATCH (PL:ProfessorLevel), (PR:ProfRecord)
WHERE PL.prof = PR.prof AND PL.level = 500 AND PR.num > 499 AND PR.num < 600
MERGE (PL)-[:IS_500]->(PR);


MATCH (C:Course), (PR:ProfRecord)
WHERE C.course = PR.course AND C.title = PR.title AND C.subject = PR.subject AND C.num = PR.num
MERGE (C)-[:TAUGHT_RECORD]->(PR);


USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///prof-gpa-dataset.csv" AS row
MERGE(:ProfSubject {subject:row.Subject, prof:row.Primary_Instructor});

MATCH (P:Professor),(PS:ProfSubject)
WHERE P.prof = PS.prof
MERGE (P)-[:TEACHES_SUB]->(PS);

MATCH (PS:ProfSubject), (P:ProfRecord)
WHERE PS.prof = P.prof AND PS.subject = P.subject
MERGE (P)-[:SUB_COURSE]->(PS);
