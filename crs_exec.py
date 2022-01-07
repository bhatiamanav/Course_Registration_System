import psycopg2
import sys

con = psycopg2.connect(database="crs", user="postgres",
                       password="abcdef", host="127.0.0.1", port="5432")
print("Database opened successfully")

if(con.closed != 1):
    print("Database Connected")

input_str = '''exit. To Exit
1. Inserting a Student 
2. Show all students details
3. Show all courses 
4. Show all courses done till now
5. Show all courses of a Particular Type
'''

with con:
    while(1):
        cur = con.cursor()
        inp = input("Welcome :")

        if inp == 'help':
            print(input_str)

        elif inp == 'exit':
            sys.exit()

        elif inp == "1":
            query = "INSERT INTO student (student_id,student_name, student_email) VALUES (2018102038, 'Tanmay Khabia', 'tanmay.khabia@students.iiit.ac.in')"
            cur.execute(query)
            con.commit()

        elif inp == "2":
            query = "SELECT * FROM student"
            cur.execute(query)
            result = cur.fetchall()
            for i in result:
                #print("Name:", i[1], "Roll Number:", i[0], "Email ID:", i[2])
                print(i)
            con.commit()

        elif inp == "3":
            query = '''SELECT 
                       course.*,prof.prof_name 
                       FROM 
                            prof 
                        INNER JOIN 
                            course 
                        ON 
                            prof.prof_id=course.prof_id'''
            cur.execute(query)
            result = cur.fetchall()
            for i in result:
                print(i)
            con.commit()

        elif inp == "4":
            inp2 = int(input("Give Student ID: "))
            query = '''SELECT 
                      all_course_data.*, course.course_name 
                      FROM 
                        course
                      INNER JOIN
                        all_course_data
                      ON
                        course.course_id = all_course_data.course_id  
                      WHERE
                        student_id = '%(bigint)s'
                      '''
            cur.execute(query, {'bigint': inp2})
            result = cur.fetchall()
            for i in result:
                print(i)
            con.commit()

        elif inp == "5":
            inp2 = int(input("Please enter Student ID: "))
            inp3 = input("Please enter Course Type: ")
            print(type(inp3))
            query = '''SELECT 
                      all_course_data.*, course.course_name 
                      FROM 
                        course
                      INNER JOIN
                        all_course_data
                      ON
                        course.course_id = all_course_data.course_id  
                      WHERE
                        student_id = '%(bigint)s'
                      AND
                        as_type = %(str)s
                      '''
            cur.execute(query, {'bigint': inp2, 'str': inp3})
            result = cur.fetchall()
            for i in result:
                print(i)
            con.commit()
