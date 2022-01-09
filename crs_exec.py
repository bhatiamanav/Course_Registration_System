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
4. Show all courses done till now(For a Student)
5. Show all courses of a Particular Type(For a Student)
6. Approving a course for a student
'''


def execute_query(query: str, cur) -> list:
    try:
        cur.execute(query)
        return cur.fetchall()
    except Exception as e:
        con.rollback()
        print(e)
        print("Unable to execute the following query")
        print(query)
        return []


def is_valid(student_id, course_id, course_type):
    query = "SELECT COUNT(*) FROM all_course_data WHERE student_id = %(bigint)s AND course_id = %(str)s"
    cur.execute(query, {'bigint': student_id, 'str': course_id})
    result = cur.fetchall()
    con.commit()
    print(result[0][0])
    if result[0][0] == 0:
        query = "SELECT COUNT(*) FROM all_course_data WHERE student_id = %(bigint)s AND as_type = %(str)s"
        cur.execute(query, {'bigint': student_id,
                    'str': course_id, 'str': course_type})
        result = cur.fetchall()
        con.commit()
        if(course_type == "Humanities" and result[0][0] < 3):
            return True
        elif(course_type == "Maths" and result[0][0] < 2):
            return True
        elif(course_type == "Open" and result[0][0] < 5):
            return True
        elif(course_type == 'Science' and result[0][0] < 2):
            return True
        else:
            return False
    else:
        return False


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
            result = execute_query(query, cur)
            con.commit()

        elif inp == "2":
            query = "SELECT * FROM student"

            result = execute_query(query=query, cur=cur)
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

            result = execute_query(query, cur)
            for i in result:
                print(i)
            con.commit()

        elif inp == "4":
            inp2 = int(input("Give Student ID: "))
            query = f'''SELECT 
                      all_course_data.*, course.course_name 
                      FROM 
                        course
                      INNER JOIN
                        all_course_data
                      ON
                        course.course_id = all_course_data.course_id  
                      WHERE
                        student_id = {inp2}
                      '''

            result = execute_query(query, cur)
            for i in result:
                print(i)
            con.commit()

        elif inp == "5":
            inp2 = int(input("Please enter Student ID: "))
            inp3 = input("Please enter Course Type: ")
            print(type(inp3))
            query = f'''SELECT 
                      all_course_data.*, course.course_name 
                      FROM 
                        course
                      INNER JOIN
                        all_course_data
                      ON
                        course.course_id = all_course_data.course_id  
                      WHERE
                        student_id = {inp2}
                      AND
                        as_type = '{inp3}'
                      '''

            result = execute_query(query, cur)
            for i in result:
                print(i)
            con.commit()

        elif inp == "6":
            inp2 = int(input("Please enter Student ID: "))
            inp3 = (input("Enter course_id: "))
            inp4 = input("Please enter Course Type: ")
            query = '''SELECT 
                       COUNT(*) FROM cr_approved 
                       WHERE 
                       course_id = %(str)s'''
            cur.execute(query, {'str': inp3})
            result = cur.fetchall()
            curr_students = result[0][0]
            con.commit()

            query2 = f"SELECT course_cap FROM course WHERE course_id = '{inp3}'"

            result = execute_query(query2, cur)
            course_capacity = result[0][0]
            con.commit()

            if curr_students < course_capacity:
                if(is_valid(inp2, inp3, inp4)):
                    query3 = f"INSERT INTO cr_approved  VALUES ({inp2},'{inp3}', '{inp4}')"
                    cur.execute(query3)
                    print("Course approved successfully")
                    con.commit()
                else:
                    print('PENDING1')
            else:
                print('PENDING2')
