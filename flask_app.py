from flask import Flask, render_template, request, url_for, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    try:
        db = sqlite3.connect('courses.db')
        sql = '''
        SELECT * FROM Courses
        '''
        cursor = db.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        db.close()
        
    except Exception as e:
        print(e)
        
    max_users = []
    for ele in data:
        try:
            id = int(ele[0])
            db = sqlite3.connect('courses.db')
            sql = '''
            SELECT COUNT(*) FROM Users
            WHERE CourseID = {}
            '''.format(id)
            cursor = db.execute(sql)
            num = cursor.fetchone()[0]
            cursor.close()
            db.close()
            
            max_users.append(num)
            
        except Exception as e:
            print(e)
    
    return render_template('index.html', data=data, max_users=max_users)
    
    
@app.route('/join_course/<int:course_id>', methods=["GET", "POST"])
def join_course(course_id):
    if request.method == "POST":
        user_email = request.form['email']
        print(course_id)
        print(user_email)
        try:
            db = sqlite3.connect('courses.db')
            sql = '''
            INSERT INTO Users
            VALUES
            ({}, '{}')
            '''.format(int(course_id), user_email)
            db.execute(sql)
            db.commit()
            db.close()
            
        except sqlite3.IntegrityError:
            return render_template('join_failed.html')
            
        except Exception as e:
            print("Another error occured-line 63")
            return "An Error Occured"
            
        return render_template("join_success.html")
    
    else:
    
        try:
            db = sqlite3.connect('courses.db')
            sql = '''
            SELECT COUNT(*) FROM Users
            WHERE CourseID = {}
            '''.format(course_id)
            cursor = db.execute(sql)
            num = int(cursor.fetchone()[0])
            cursor.close()
            db.close()
            
        except Exception as e:
            print(e)
            
        try:
            db = sqlite3.connect('courses.db')
            sql = '''
            SELECT MaxUsers FROM Courses
            WHERE CourseID = {}
            '''.format(course_id)
            cursor = db.execute(sql)
            max_users = int(cursor.fetchone()[0])
            cursor.close()
            db.close()
            
        except Exception as e:
            print(e) 
            
        if num < max_users:
            
            try:
                db = sqlite3.connect('courses.db')
                sql = '''
                SELECT CourseName FROM COURSES
                WHERE CourseID = {}
                '''.format(int(course_id))
                
                cursor = db.execute(sql)
                data = cursor.fetchone()[0]
                cursor.close()
                db.close()
            
            except Exception as e:
                print(e)
        
            return render_template('join.html', data=data, course_id=course_id)
        
        else:
            return render_template('full.html')
        

@app.route('/show_courses/<int:course_id>')
def show_courses(course_id):
    try:
        db = sqlite3.connect('courses.db')
        sql = '''
        SELECT UserEmail FROM Users
        WHERE CourseID = {}
        '''.format(int(course_id))
        cursor = db.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        db.close()
        
    except Exception as e:
        print(e)
        
    try:
        db = sqlite3.connect('courses.db')
        sql = '''
        SELECT CourseName FROM COURSES
        WHERE CourseID = {}
        '''.format(int(course_id))
        
        cursor = db.execute(sql)
        course_name = cursor.fetchone()[0]
        cursor.close()
        db.close()
        
    except Exception as e:
        print(e)
        
    return render_template('show_courses.html', data=data, course_name=course_name)
    

@app.route('/add_course/', methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
        course_name = request.form["name"]
        max_users = int(request.form["max_users"])
        
        try:
            db = sqlite3.connect('courses.db')
            sql = '''
            INSERT INTO Courses
            (CourseName, MaxUsers)
            VALUES
            ('{}', {})
            '''.format(course_name, max_users)
            db.execute(sql)
            db.commit()
            db.close()
            
        except Exception as e:
            print(e)
            
        return redirect(url_for('index'))
    
    else:
        return render_template('add_course.html')


if __name__ == "__main__":
    app.run(debug=True)
