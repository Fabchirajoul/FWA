import os
from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify, send_file
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from functools import wraps


matplotlib.use('Agg') 

app = Flask(__name__)
app.secret_key = 'secret_key'





# Database setup functions
def create_user_table():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY,
            Firstname TEXT NOT NULL,
            Lastname TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()
    
def create_administrative_user_table():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AdministrativeUser (
            id INTEGER PRIMARY KEY,
            Firstname TEXT NOT NULL,
            Lastname TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()
    
    
def create_question_table():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Questions (
            id INTEGER PRIMARY KEY,
            Question_id INTEGER NOT NULL,
            GeneralKNowledge TEXT NOT NULL,
            Question TEXT NOT NULL,
            QuestionOption TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

def create_common_cause_question_table():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CommonCauseQuestions (
            id INTEGER PRIMARY KEY,
            Question_id INTEGER NOT NULL,
            CoomonCause TEXT NOT NULL,
            Question TEXT NOT NULL,
            QuestionOption TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()
    
def create_food_wastre_on_environment_question_table():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS EnvironmentWasteQuestions (
            id INTEGER PRIMARY KEY,
            Question_id INTEGER NOT NULL,
            Environment TEXT NOT NULL,
            Question TEXT NOT NULL,
            QuestionOption TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()
  
def create_food_wastre_prevention_method_question_table():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PrevemtionMethodQuestions (
            id INTEGER PRIMARY KEY,
            Question_id INTEGER NOT NULL,
            Environment TEXT NOT NULL,
            Question TEXT NOT NULL,
            QuestionOption TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()


def create_food_waste_management_method_question_table():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ManagementMethodQuestions (
            id INTEGER PRIMARY KEY,
            Question_id INTEGER NOT NULL,
            Environment TEXT NOT NULL,
            Question TEXT NOT NULL,
            QuestionOption TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()





# Question option management
def create_question_option_table():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS QuestionsOptions (
            id INTEGER PRIMARY KEY,
            Category TEXT NOT NULL,
            QuestionOption TEXT NOT NULL,
            Question_Id TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()
    



# Question option answers
def create_question_option__answer_table():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS QuestionsOptionsAnswer (
            id INTEGER PRIMARY KEY,
            Category TEXT NOT NULL,
            Question_Id TEXT NOT NULL,
            QuestionOptionAnswer TEXT NOT NULL 
        )
    ''')
    connection.commit()
    connection.close()
    
def create_user_answer_submission_table():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SubmitAnswers (
            id INTEGER PRIMARY KEY,
            Question_Id TEXT NOT NULL,
            Firstname TEXT NOT NULL,
            Category TEXT NOT NULL,
            Question TEXT NOT NULL,
            QuestionAnswer TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

# Create tables
create_user_table()
create_administrative_user_table()
create_question_table()
create_question_option_table()
create_question_option__answer_table()
create_common_cause_question_table()
create_food_wastre_on_environment_question_table() 
create_food_wastre_prevention_method_question_table()
create_food_waste_management_method_question_table()
create_user_answer_submission_table()  







@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return render_template('index.html')






# Register app route
@app.route('/register', methods=['GET', 'POST'])
def register():
    

    

    return render_template('register.html')

# Login app route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        if not email or not password:
            flash("Please fill in all the required fields.")
            return render_template('index.html')

        # Connect to the database
        connection = sqlite3.connect('FoodwasteAppdatabase.db')
        cursor = connection.cursor()

        # Check in AdministrativeUser table first
        cursor.execute('SELECT * FROM AdministrativeUser WHERE email=?', (email,))
        admin_user = cursor.fetchone()

        if admin_user and password == admin_user[4]:  # Plain text password comparison
            # Set session for admin and redirect to Administrator page
            session['email'] = admin_user[2]
            session['name'] = admin_user[1]
            session['is_admin'] = True
            session['logged_in'] = True
            connection.close()
            return redirect(url_for('administrator'))  # Redirect to admin page

        # Check in User table if not found in AdministrativeUser
        cursor.execute('SELECT * FROM User WHERE email=?', (email,))
        user = cursor.fetchone()
        connection.close()

        if user and password == user[4]:  # Plain text password comparison
            # Set session for regular user and redirect to UserAccount page
            session['email'] = user[2]
            session['name'] = user[1]
            session['is_admin'] = False
            session['logged_in'] = True
            return redirect(url_for('user_account'))  # Redirect to user account page

        else:
            flash("Invalid credentials. Please make sure to enter the correct email and password.")
            return render_template('index.html')

    return render_template('index.html')


# Registration app route
@app.route('/Userregister', methods=['GET', 'POST'])
def Adminregister():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    

    if request.method == 'POST':
        FIrstname = request.form['firstName']
        lastName = request.form['Lastname']
        email = request.form['email']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']

        # Check if passwords match
        if password != confirmpassword:
            flash('Passwords do not match')
            return render_template('regiser.html')

        # Check if the user already exists
        connection = sqlite3.connect('FoodwasteAppdatabase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM User WHERE email=?', (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            connection.close()
            flash('User with this email already exists')
            return render_template('register.html',)



        # Insert the new user into the database
        cursor.execute(
            'INSERT INTO User (Firstname, Lastname, email, password) VALUES (?, ?, ?, ?)',
            (FIrstname, lastName, email, password))
        connection.commit()
        connection.close()

        # Flash success message and redirect
        flash('User successfully registered!', 'success')
        return redirect('/login')

    # Pass business sectors to the template
    return render_template('index.html', user_name=user_name)



# Administrator redicted page
@app.route('/Administrator_account', methods=['GET', 'POST'])
def administrator():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    

    return render_template('Administrator.html', user_name=user_name)




# Add new question
@app.route('/Add_new_question', methods=['GET', 'POST'])
def AddQuestion():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session

    if request.method == 'POST':
        Category = request.form['new_question_category']
        NewQuestion = request.form['new_question']
        NewQuestionOption = request.form['new_question_option']
        NewQuestionnumber = request.form['Question_option_ID_number']

        connection = sqlite3.connect('FoodwasteAppdatabase.db')
        cursor = connection.cursor()

        # Check the category and insert into the respective table
        if Category == 'FOOD WASTE GENERAL KNOWLEDGE':
            cursor.execute(
                'INSERT INTO Questions (Question_id, GeneralKNowledge, Question, QuestionOption) VALUES (?, ?, ?, ?)',
                (NewQuestionnumber, Category, NewQuestion, NewQuestionOption)
            )
        elif Category == 'COMMON CAUSES AND MISCONCEPTION OF FOOD WASTE':
            cursor.execute(
                'INSERT INTO CommonCauseQuestions (Question_id, CoomonCause, Question, QuestionOption) VALUES (?, ?, ?, ?)',
                (NewQuestionnumber, Category, NewQuestion, NewQuestionOption)
            )
        elif Category == 'FOOD WASTE ON THE ENVIRONMENT':
            cursor.execute(
                'INSERT INTO EnvironmentWasteQuestions (Question_id, Environment, Question, QuestionOption) VALUES (?, ?, ?, ?)',
                (NewQuestionnumber, Category, NewQuestion, NewQuestionOption)
            )
        elif Category == 'FOOD WASTE PREVENTION METHOD':
            cursor.execute(
                'INSERT INTO PrevemtionMethodQuestions (Question_id, Environment, Question, QuestionOption) VALUES (?, ?, ?, ?)',
                (NewQuestionnumber, Category, NewQuestion, NewQuestionOption)
            )
        elif Category == 'FOOD WASTE MANAGEMENT METHOD':
            cursor.execute(
                'INSERT INTO ManagementMethodQuestions (Question_id, Environment, Question, QuestionOption) VALUES (?, ?, ?, ?)',
                (NewQuestionnumber, Category, NewQuestion, NewQuestionOption)
            )
        
        connection.commit()
        connection.close()

        # Flash success message and redirect
        flash('Question successfully added!', 'success')
        return redirect('/Administrator_account')

    # Pass user name to the template
    return render_template('Administrator.html', user_name=user_name)



# Add new question options
@app.route('/Add_new_question_options', methods=['GET', 'POST'])
def AddQuestioOptionsn():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    

    if request.method == 'POST':
        QuestionOptionID = request.form['Question_option_ID']
        QuestionOption = request.form['Question_option']
        Category = request.form['new_question_category']


        connection = sqlite3.connect('FoodwasteAppdatabase.db')
        cursor = connection.cursor()
        # Insert the new user into the database
        cursor.execute(
            'INSERT INTO QuestionsOptions (Category, QuestionOption, Question_Id) VALUES (?, ?, ?)',
            (Category, QuestionOption, QuestionOptionID))
        connection.commit()
        connection.close()

        # Flash success message and redirect
        flash('Question option successfully Added!', 'success')
        return redirect('/Administrator_account')

    # Pass business sectors to the template
    return render_template('Administrator.html', user_name=user_name)

# Provide question option answer
@app.route('/provide_question_option_answers', methods=['GET', 'POST'])
def ProvideAnswers():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    

    if request.method == 'POST':
        QuestionOptionID = request.form['Question_option_ID']
        QuestionOptionAnswer = request.form['Question_option_answer']
        Category = request.form['new_question_category']


        connection = sqlite3.connect('FoodwasteAppdatabase.db')
        cursor = connection.cursor()
        # Insert the new user into the database
        cursor.execute(
            'INSERT INTO QuestionsOptionsAnswer (Category, Question_Id, QuestionOptionAnswer) VALUES (?, ?, ?)',
            (Category, QuestionOptionID, QuestionOptionAnswer))
        connection.commit()
        connection.close()

        # Flash success message and redirect
        flash('Question answer successfully Added!', 'success')
        return redirect('/Administrator_account')

    # Pass business sectors to the template
    return render_template('Administrator.html', user_name=user_name)








# User account redirected page
@app.route('/User_account', methods=['GET', 'POST'])
def user_account():
    questions = get_all_questions()  # Retrieve all questions with options from the database
    questions_prevention_method = get_all_questions_for_prevention_method() 
    questions_management_method = get_all_questions_for_management_waste()
    questions_env = get_all_questions_for_environmental_waste()
    questions_common_cuase = get_all_questions_for_common_cause_waste()
    
    user_name = session.get('name', 'User')  # Retrieve the user's name from the session

    return render_template('homepage.html', user_name=user_name, questions=questions, 
                           questions_env=questions_env, questions_prevention_method=questions_prevention_method,
                           questions_management_method=questions_management_method, questions_common_cuase=questions_common_cuase)





# Get all question option for misconception and common cause food management

def get_all_questions_for_common_cause_waste():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()

    questions = []
    try:
        # Select all questions and their options for the specified category
        cursor.execute("SELECT Question_id, CoomonCause, Question, QuestionOption FROM CommonCauseQuestions WHERE CoomonCause = 'COMMON CAUSES AND MISCONCEPTION OF FOOD WASTE'")
        
        for question_row in cursor.fetchall():
            question_id, category, question_text, question_option = question_row
            
            # Fetch options if the question type is 'Dropdown' or 'Tick box'
            if question_option in ["Dropdown", "Tick box"]:
                cursor.execute("SELECT QuestionOption FROM QuestionsOptions WHERE Question_Id = ? AND Category = ?", (question_id, category))
                options = [option[0] for option in cursor.fetchall()]
            else:
                options = []  # No options for types other than 'Dropdown' or 'Tick box'

            # Append each question along with its options (if any) to the list
            questions.append({
                "id": question_id,
                "category": category,
                "text": question_text,
                "type": question_option,
                "options": options
            })
    finally:
        connection.close()

    return questions

# Getting all questions for the Environmental waste
def get_all_questions_for_environmental_waste():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()

    questions = []
    try:
        # Select all questions and their options for the specified category
        cursor.execute("SELECT Question_id, Environment, Question, QuestionOption FROM EnvironmentWasteQuestions WHERE Environment = 'FOOD WASTE ON THE ENVIRONMENT'")
        
        for question_row in cursor.fetchall():
            question_id, category, question_text, question_option = question_row
            
            # Fetch options if the question type is 'Dropdown' or 'Tick box'
            if question_option in ["Dropdown", "Tick box"]:
                cursor.execute("SELECT QuestionOption FROM QuestionsOptions WHERE Question_Id = ? AND Category = ?", (question_id, category))
                options = [option[0] for option in cursor.fetchall()]
            else:
                options = []  # No options for types other than 'Dropdown' or 'Tick box'

            # Append each question along with its options (if any) to the list
            questions.append({
                "id": question_id,
                "category": category,
                "text": question_text,
                "type": question_option,
                "options": options
            })
    finally:
        connection.close()

    return questions




# Get all question option for FOOD WASTE MANAGEMENT METHOD
def get_all_questions_for_management_waste():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()

    questions = []
    try:
        # Select all questions and their options for the specified category
        cursor.execute("SELECT Question_id, Environment, Question, QuestionOption FROM ManagementMethodQuestions WHERE Environment = 'FOOD WASTE MANAGEMENT METHOD'")
        
        for question_row in cursor.fetchall():
            question_id, category, question_text, question_option = question_row
            
            # Fetch options if the question type is 'Dropdown' or 'Tick box'
            if question_option in ["Dropdown", "Tick box"]:
                cursor.execute("SELECT QuestionOption FROM QuestionsOptions WHERE Question_Id = ? AND Category = 'FOOD WASTE MANAGEMENT METHOD'", (question_id,))
                options = [option[0] for option in cursor.fetchall()]
            else:
                options = []  # No options for types other than 'Dropdown' or 'Tick box'

            # Append each question along with its options (if any) to the list
            questions.append({
                "id": question_id,
                "category": category,
                "text": question_text,
                "type": question_option,
                "options": options
            })
    finally:
        connection.close()

    return questions



# Get all question option for prevention method
def get_all_questions_for_prevention_method():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()

    questions = []
    try:
        # Select all questions and their options for the specified category
        cursor.execute("SELECT Question_id, Environment, Question, QuestionOption FROM PrevemtionMethodQuestions WHERE Environment = 'FOOD WASTE PREVENTION METHOD'")
        
        for question_row in cursor.fetchall():
            question_id, category, question_text, question_option = question_row
            
            # Fetch options if the question type is 'Dropdown' or 'Tick box'
            if question_option in ["Dropdown", "Tick box"]:
                cursor.execute("SELECT QuestionOption FROM QuestionsOptions WHERE Question_Id = ? AND Category = 'FOOD WASTE PREVENTION METHOD'", (question_id,))
                options = [option[0] for option in cursor.fetchall()]
            else:
                options = []  # No options for types other than 'Dropdown' or 'Tick box'

            # Append each question along with its options (if any) to the list
            questions.append({
                "id": question_id,
                "category": category,
                "text": question_text,
                "type": question_option,
                "options": options
            })
    finally:
        connection.close()

    return questions


# Function to get all questions for the FOOD WASTE GENERAL KNOWLEDGE category
def get_all_questions():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()

    questions = []
    try:
        # Select all questions and their options for the specified category
        cursor.execute("SELECT Question_id, GeneralKNowledge, Question, QuestionOption FROM Questions WHERE GeneralKNowledge = 'FOOD WASTE GENERAL KNOWLEDGE'")
        
        for question_row in cursor.fetchall():
            question_id, category, question_text, question_option = question_row
            
            # Fetch options if the question type is 'Dropdown' or 'Tick box'
            if question_option in ["Dropdown", "Tick box"]:
                cursor.execute("SELECT QuestionOption FROM QuestionsOptions WHERE Question_Id = ? AND Category = ?", (question_id, category))
                options = [option[0] for option in cursor.fetchall()]
            else:
                options = []  # No options for types other than 'Dropdown' or 'Tick box'

            # Append each question along with its options (if any) to the list
            questions.append({
                "id": question_id,
                "category": category,
                "text": question_text,
                "type": question_option,
                "options": options
            })
    finally:
        connection.close()

    return questions






# Answer route for general waste
@app.route('/user_submitted_answers', methods=['POST'])
def UserAnswers():
    questions = get_all_questions()  # Retrieve all questions with options from the database
    questions_prevention_method = get_all_questions_for_prevention_method()
    questions_management_method = get_all_questions_for_management_waste()
    questions_env = get_all_questions_for_environmental_waste()
    questions_common_cuase = get_all_questions_for_common_cause_waste()
    submitted_category = "FOOD WASTE GENERAL KNOWLEDGE"
    user_name = session.get('name', 'User')  # Retrieve the user's name from session

    if request.method == 'POST':
        connection = sqlite3.connect('FoodwasteAppdatabase.db')
        cursor = connection.cursor()

        # Gather user answers for comparison
        user_answers = {}

        # Loop through form data to retrieve each question's answer
        for key, answer in request.form.items():
            if key.startswith("answer_"):
                question_id = key.split("_")[1]  # Extract question ID from the input name
                user_answers[question_id] = answer  # Store the answer in user_answers dictionary

                # Fetch question text and handle NoneType
                question_data = cursor.execute("SELECT Question FROM Questions WHERE Question_id=?", (question_id,)).fetchone()
                
                if question_data:
                    question_text = question_data[0]
                    # Insert the question and its answer into the SubmitAnswers table
                    cursor.execute(
                        'INSERT INTO SubmitAnswers (Question_Id, Firstname, Category, Question, QuestionAnswer) VALUES (?, ?, ?, ?, ?)',
                        (question_id, user_name, submitted_category, question_text, answer)
                    )

        connection.commit()
        connection.close()

        # Calculate the correct answer percentage and get incorrect questions
        correct_percentage, incorrect_questions = calculate_correct_answer_percentage(user_answers, "FOOD WASTE GENERAL KNOWLEDGE")

        # Flash messages based on the score
        if correct_percentage >= 1:
            flash(f'Congratulations! You answered {correct_percentage:.2f}% of questions correctly! You can now take the game', 'success')
        else:
            flash(f'Sorry, you need to score at least 1% of the quiz before you can play the game. You scored {correct_percentage:.2f}%. Please review your answers.', 'warning')

        # Render the template with incorrect questions, if any
        return render_template('homepage.html', user_name=user_name, incorrect_questions=incorrect_questions, questions=questions,
                               questions_env=questions_env, questions_prevention_method=questions_prevention_method,
                               questions_management_method=questions_management_method, questions_common_cuase=questions_common_cuase)

    return render_template('homepage.html', user_name=user_name, questions=questions,
                           questions_env=questions_env, questions_prevention_method=questions_prevention_method,
                           questions_management_method=questions_management_method, questions_common_cuase=questions_common_cuase)



# Function to calculate the percentage of correct answers
def calculate_correct_answer_percentage(user_answers, category):
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()

    correct_count = 0
    total_questions = len(user_answers)
    incorrect_questions = []

    for question_id, user_answer in user_answers.items():
        # Select the appropriate query based on the category
        if category == "FOOD WASTE GENERAL KNOWLEDGE":
            cursor.execute(
                "SELECT q.Question, qoa.QuestionOptionAnswer "
                "FROM Questions q "
                "JOIN QuestionsOptionsAnswer qoa ON q.Question_id = qoa.Question_Id "
                "WHERE q.Question_id = ?",
                (question_id,)
            )
        elif category == "COMMON CAUSES AND MISCONCEPTION OF FOOD WASTE":
            cursor.execute(
                "SELECT ccq.Question, qoa.QuestionOptionAnswer "
                "FROM CommonCauseQuestions ccq "
                "JOIN QuestionsOptionsAnswer qoa ON ccq.Question_id = qoa.Question_Id "
                "WHERE ccq.Question_id = ?",
                (question_id,)
            )
        elif category == "FOOD WASTE ON THE ENVIRONMENT":
            cursor.execute(
                "SELECT env.Question, qoa.QuestionOptionAnswer "
                "FROM EnvironmentWasteQuestions env "
                "JOIN QuestionsOptionsAnswer qoa ON env.Question_id = qoa.Question_Id "
                "WHERE env.Question_id = ?",
                (question_id,)
            )
        elif category == "FOOD WASTE PREVENTION METHOD":
            cursor.execute(
                "SELECT prv.Question, qoa.QuestionOptionAnswer "
                "FROM PrevemtionMethodQuestions prv "
                "JOIN QuestionsOptionsAnswer qoa ON prv.Question_id = qoa.Question_Id "
                "WHERE prv.Question_id = ?",
                (question_id,)
            )
        elif category == "FOOD WASTE MANAGEMENT METHOD":
            cursor.execute(
                "SELECT mng.Question, qoa.QuestionOptionAnswer "
                "FROM ManagementMethodQuestions mng "
                "JOIN QuestionsOptionsAnswer qoa ON mng.Question_id = qoa.Question_Id "
                "WHERE mng.Question_id = ?",
                (question_id,)
            )

        # Fetch the result
        question_data = cursor.fetchone()

        if question_data:
            question_text, correct_answer = question_data
            # Check if the user's answer matches the correct answer
            if str(user_answer).strip().lower() == str(correct_answer).strip().lower():
                correct_count += 1
            else:
                # Append the question details to the incorrect_questions list if the answer is wrong
                incorrect_questions.append({
                    "question_id": question_id,
                    "category": category,
                    "question_text": question_text,
                    "user_answer": user_answer,
                    "correct_answer": correct_answer
                })

    # Close the database connection
    connection.close()

    # Calculate the percentage of correct answers
    correct_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0

    return correct_percentage, incorrect_questions







# app route for the common cause management
@app.route('/user_submitted_answers_for_common_cause', methods=['POST'])
def UserAnswersCommonCause():
    questions = get_all_questions()  # Retrieve all questions with options from the database
    questions_prevention_method = get_all_questions_for_prevention_method() 
    questions_management_method = get_all_questions_for_management_waste()
    questions_env = get_all_questions_for_environmental_waste()
    questions_common_cuase = get_all_questions_for_common_cause_waste()
    submitted_category = "COMMON CAUSES AND MISCONCEPTION OF FOOD WASTE"
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    
    if request.method == 'POST':
        connection = sqlite3.connect('FoodwasteAppdatabase.db')
        cursor = connection.cursor()

        # Gather user answers for comparison
        user_answers = {}

        # Loop through form data to retrieve each question's answer
        for key, answer in request.form.items():
            if key.startswith("answer_"):
                question_id = key.split("_")[1]  # Extract question ID from the input name
                user_answers[question_id] = answer  # Store the answer in user_answers dictionary

                # Fetch question text and handle NoneType
                question_data = cursor.execute("SELECT Question FROM CommonCauseQuestions WHERE Question_id=?", (question_id,)).fetchone()
                
                if question_data:
                    question_text = question_data[0]
                    
                    # Insert the question and its answer into the SubmitAnswers table
                    cursor.execute(
                        'INSERT INTO SubmitAnswers (Question_Id, Firstname, Category, Question, QuestionAnswer) VALUES (?, ?, ?, ?, ?)',
                        (question_id, user_name, submitted_category, question_text, answer)
                    )
                else:
                    # Log an error if the question_id does not exist in the database
                    print(f"Warning: Question ID {question_id} not found in CommonCauseQuestions table.")

        connection.commit()
        connection.close()

        # Calculate the correct answer percentage and get incorrect questions
        correct_percentage, incorrect_questions = calculate_correct_answer_percentage(user_answers, "COMMON CAUSES AND MISCONCEPTION OF FOOD WASTE")

        # Redirect based on the correct percentage
        if correct_percentage >= 1:
            flash(f'Congratulations! You answered {correct_percentage:.2f}% of questions correctly! You can now take the game', 'success')
            return redirect(url_for('user_account'))
        else:
            flash(f'Sorry, you need to score at least 1% of the quiz before you can proceed. You scored {correct_percentage:.2f}%. Please review your answers.', 'warning')
            return render_template('homepage.html', user_name=user_name, incorrect_questions=incorrect_questions, questions=questions, 
                           questions_env=questions_env, questions_prevention_method=questions_prevention_method,
                           questions_management_method=questions_management_method, questions_common_cuase=questions_common_cuase)

    return render_template('homepage.html', user_name=user_name, questions=questions, 
                           questions_env=questions_env, questions_prevention_method=questions_prevention_method,
                           questions_management_method=questions_management_method, questions_common_cuase=questions_common_cuase)







# FOOD WASTE ON THE ENVIRONMENT
@app.route('/user_submitted_answers_for_environmental_management', methods=['POST'])
def UserAnswersEnvironmentalManagement():
    questions = get_all_questions()  # Retrieve all questions with options from the database
    questions_prevention_method = get_all_questions_for_prevention_method() 
    questions_management_method = get_all_questions_for_management_waste()
    questions_env = get_all_questions_for_environmental_waste()
    questions_common_cuase = get_all_questions_for_common_cause_waste()
    submitted_category = "FOOD WASTE ON THE ENVIRONMENT"
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    
    if request.method == 'POST':
        connection = sqlite3.connect('FoodwasteAppdatabase.db')
        cursor = connection.cursor()

        # Gather user answers for comparison
        user_answers = {}

        # Loop through form data to retrieve each question's answer
        for key, answer in request.form.items():
            if key.startswith("answer_"):
                question_id = key.split("_")[1]  # Extract question ID from the input name
                user_answers[question_id] = answer  # Store the answer in user_answers dictionary

                # Fetch question text and handle NoneType
                question_data = cursor.execute("SELECT Question FROM EnvironmentWasteQuestions WHERE Question_id=?", (question_id,)).fetchone()
                
                if question_data:
                    question_text = question_data[0]
                    
                    # Insert the question and its answer into the SubmitAnswers table
                    cursor.execute(
                        'INSERT INTO SubmitAnswers (Question_Id, Firstname, Category, Question, QuestionAnswer) VALUES (?, ?, ?, ?, ?)',
                        (question_id, user_name, submitted_category, question_text, answer)
                    )
                else:
                    # Log an error if the question_id does not exist in the database
                    print(f"Warning: Question ID {question_id} not found in EnvironmentWasteQuestions table.")

        connection.commit()
        connection.close()

        # Calculate the correct answer percentage and get incorrect questions
        correct_percentage, incorrect_questions = calculate_correct_answer_percentage(user_answers, "FOOD WASTE ON THE ENVIRONMENT")

        # Redirect based on the correct percentage
        if correct_percentage >= 1:
            flash(f'Congratulations! You answered {correct_percentage:.2f}% of questions correctly! You can now take the game', 'success')
            return redirect(url_for('user_account'))
        else:
            flash(f'Sorry, you need to score at least 1% of the quiz before you can proceed. You scored {correct_percentage:.2f}%. Please review your answers.', 'warning')
            return render_template('homepage.html', user_name=user_name, incorrect_questions=incorrect_questions, questions=questions, 
                           questions_env=questions_env, questions_prevention_method=questions_prevention_method,
                           questions_management_method=questions_management_method, questions_common_cuase=questions_common_cuase)

    return render_template('homepage.html', user_name=user_name, questions=questions, 
                           questions_env=questions_env, questions_prevention_method=questions_prevention_method,
                           questions_management_method=questions_management_method, questions_common_cuase=questions_common_cuase)



# Food waste prevention method
@app.route('/user_submitted_answers_for_food_waste_prevention_methof', methods=['POST'])
def UserAnswersPreventionMethod():
    questions = get_all_questions()  # Retrieve all questions with options from the database
    questions_prevention_method = get_all_questions_for_prevention_method() 
    questions_management_method = get_all_questions_for_management_waste()
    questions_env = get_all_questions_for_environmental_waste()
    questions_common_cuase = get_all_questions_for_common_cause_waste()
    submitted_category = "FOOD WASTE PREVENTION METHOD"
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    
    if request.method == 'POST':
        connection = sqlite3.connect('FoodwasteAppdatabase.db')
        cursor = connection.cursor()

        # Gather user answers for comparison
        user_answers = {}

        # Loop through form data to retrieve each question's answer
        for key, answer in request.form.items():
            if key.startswith("answer_"):
                question_id = key.split("_")[1]  # Extract question ID from the input name
                user_answers[question_id] = answer  # Store the answer in user_answers dictionary

                # Fetch question text and handle NoneType
                question_data = cursor.execute("SELECT Question FROM PrevemtionMethodQuestions WHERE Question_id=?", (question_id,)).fetchone()
                
                if question_data:
                    question_text = question_data[0]
                    
                    # Insert the question and its answer into the SubmitAnswers table
                    cursor.execute(
                        'INSERT INTO SubmitAnswers (Question_Id, Firstname, Category, Question, QuestionAnswer) VALUES (?, ?, ?, ?, ?)',
                        (question_id, user_name, submitted_category, question_text, answer)
                    )
                else:
                    # Log an error if the question_id does not exist in the database
                    print(f"Warning: Question ID {question_id} not found in PrevemtionMethodQuestions table.")

        connection.commit()
        connection.close()

        # Calculate the correct answer percentage and get incorrect questions
        correct_percentage, incorrect_questions = calculate_correct_answer_percentage(user_answers, "FOOD WASTE PREVENTION METHOD")

        # Redirect based on the correct percentage
        if correct_percentage >= 1:
            flash(f'Congratulations! You answered {correct_percentage:.2f}% of questions correctly! You can now take the game', 'success')
            return redirect(url_for('user_account'))
        else:
            flash(f'Sorry, you need to score at least 1% of the quiz before you can proceed. You scored {correct_percentage:.2f}%. Please review your answers.', 'warning')
            return render_template('homepage.html', user_name=user_name, incorrect_questions=incorrect_questions, questions=questions, 
                           questions_env=questions_env, questions_prevention_method=questions_prevention_method,
                           questions_management_method=questions_management_method, questions_common_cuase=questions_common_cuase)

    return render_template('homepage.html', user_name=user_name, questions=questions, 
                           questions_env=questions_env, questions_prevention_method=questions_prevention_method,
                           questions_management_method=questions_management_method, questions_common_cuase=questions_common_cuase)



# FOOD WASTE MANAGEMENT METHOD

@app.route('/user_submitted_answers_for_food_waste_management_method', methods=['POST'])
def UserAnswersManagementMethod():
    questions = get_all_questions()  # Retrieve all questions with options from the database
    questions_prevention_method = get_all_questions_for_prevention_method() 
    questions_management_method = get_all_questions_for_management_waste()
    questions_env = get_all_questions_for_environmental_waste()
    questions_common_cuase = get_all_questions_for_common_cause_waste()
    submitted_category = "FOOD WASTE PREVENTION METHOD"
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    
    if request.method == 'POST':
        connection = sqlite3.connect('FoodwasteAppdatabase.db')
        cursor = connection.cursor()

        # Gather user answers for comparison
        user_answers = {}

        # Loop through form data to retrieve each question's answer
        for key, answer in request.form.items():
            if key.startswith("answer_"):
                question_id = key.split("_")[1]  # Extract question ID from the input name
                user_answers[question_id] = answer  # Store the answer in user_answers dictionary

                # Fetch question text and handle NoneType
                question_data = cursor.execute("SELECT Question FROM ManagementMethodQuestions WHERE Question_id=?", (question_id,)).fetchone()
                
                if question_data:
                    question_text = question_data[0]
                    
                    # Insert the question and its answer into the SubmitAnswers table
                    cursor.execute(
                        'INSERT INTO SubmitAnswers (Question_Id, Firstname, Category, Question, QuestionAnswer) VALUES (?, ?, ?, ?, ?)',
                        (question_id, user_name, submitted_category, question_text, answer)
                    )
                else:
                    # Log an error if the question_id does not exist in the database
                    print(f"Warning: Question ID {question_id} not found in ManagementMethodQuestions table.")

        connection.commit()
        connection.close()

        # Calculate the correct answer percentage and get incorrect questions
        correct_percentage, incorrect_questions = calculate_correct_answer_percentage(user_answers, "FOOD WASTE PREVENTION METHOD")

        # Redirect based on the correct percentage
        if correct_percentage >= 1:
            flash(f'Congratulations! You answered {correct_percentage:.2f}% of questions correctly! You can now take the game', 'success')
            return redirect(url_for('user_account'))
        else:
            flash(f'Sorry, you need to score at least 1% of the quiz before you can proceed. You scored {correct_percentage:.2f}%. Please review your answers.', 'warning')
            return render_template('homepage.html', user_name=user_name, incorrect_questions=incorrect_questions, questions=questions, 
                           questions_env=questions_env, questions_prevention_method=questions_prevention_method,
                           questions_management_method=questions_management_method, questions_common_cuase=questions_common_cuase)

    return render_template('homepage.html', user_name=user_name, questions=questions, 
                           questions_env=questions_env, questions_prevention_method=questions_prevention_method,
                           questions_management_method=questions_management_method, questions_common_cuase=questions_common_cuase)






















































import random


# User account redirected page
@app.route('/user_account_game', methods=['GET', 'POST'])
def user_account_game():
    questions = get_all_questions()  # Retrieve all questions with options from the database
    questions_prevention_method = get_all_questions_for_prevention_method() 
    questions_management_method = get_all_questions_for_management_waste()
    questions_env = get_all_questions_for_environmental_waste()
    questions_common_cuase = get_all_questions_for_common_cause_waste()
    submitted_category = "FOOD WASTE PREVENTION METHOD"
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    
    grid = create_word_search()

    # Enumerate the grid for use in the template
    enumerated_grid = [(i, [(j, cell) for j, cell in enumerate(row)]) for i, row in enumerate(grid)]

    return render_template('userAccountGame.html', user_name=user_name, questions=questions, 
                           questions_env=questions_env, questions_prevention_method=questions_prevention_method,
                           questions_management_method=questions_management_method, questions_common_cuase=questions_common_cuase, 
                           grid=enumerated_grid, words=words)


# Words to be included in the word search
words = [
    "FOOD",
    "WASTE",
    "MANAGEMENT",
    "PREVENTION",
    "CHIETA",
    "COMMON",
    "CAUSES",
    "METHODS",
    "ENVIRONMENT",
    "KNOWLEDGE",
    "GENERAL"
]

grid_size = 12

def create_word_search():
    """Generate the word search grid and place the words."""
    grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]

    def can_place_word(word, row, col, direction):
        """Check if a word can be placed starting at (row, col) in a given direction."""
        for i in range(len(word)):
            if direction == 'row':
                if col + len(word) > grid_size or (grid[row][col + i] != ' ' and grid[row][col + i] != word[i]):
                    return False
            elif direction == 'column':
                if row + len(word) > grid_size or (grid[row + i][col] != ' ' and grid[row + i][col] != word[i]):
                    return False
            elif direction == 'diagonal':
                if row + len(word) > grid_size or col + len(word) > grid_size or (grid[row + i][col + i] != ' ' and grid[row + i][col + i] != word[i]):
                    return False
        return True

    def place_word(word):
        """Place a word on the grid in a random direction."""
        directions = ['row', 'column', 'diagonal']
        placed = False
        while not placed:
            direction = random.choice(directions)
            row = random.randint(0, grid_size - 1)
            col = random.randint(0, grid_size - 1)

            if can_place_word(word, row, col, direction):
                for i in range(len(word)):
                    if direction == 'row':
                        grid[row][col + i] = word[i]
                    elif direction == 'column':
                        grid[row + i][col] = word[i]
                    elif direction == 'diagonal':
                        grid[row + i][col + i] = word[i]
                placed = True

    # Place all words in the grid
    for word in words:
        place_word(word)

    # Fill empty cells with random letters
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == ' ':
                grid[i][j] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    return grid

















































if __name__ == '__main__':
    app.run(debug=True) 