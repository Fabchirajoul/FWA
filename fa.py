import os
from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify, send_file
import sqlite3
import bcrypt
import random
import string
import io
import base64
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from functools import wraps


matplotlib.use('Agg')  # Use a non-GUI backend

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
            Question TEXT NOT NULL,
            QuestionOption TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()


def create_question_option_table():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS QuestionsOptions (
            id INTEGER PRIMARY KEY,
            QuestionOption TEXT NOT NULL,
            Question_Id TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()
    
def create_question_option__answer_table():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS QuestionsOptionsAnswer (
            id INTEGER PRIMARY KEY,
            Question_Id TEXT NOT NULL,
            QuestionOptionAnswer TEXT NOT NULL 
        )
    ''')
    connection.commit()
    connection.close()
    
def create_answer_submission_table():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SubmittedAnswers (
            id INTEGER PRIMARY KEY,
            Firstname TEXT NOT NULL,
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
create_answer_submission_table()



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
            return render_template('login.html')

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
            return render_template('login.html')

    return render_template('login.html')


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
    return render_template('login.html', user_name=user_name)



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
        NewQuestion = request.form['new_question']
        NewQuestionOption = request.form['new_question_option']


        connection = sqlite3.connect('FoodwasteAppdatabase.db')
        cursor = connection.cursor()
        # Insert the new user into the database
        cursor.execute(
            'INSERT INTO Questions (Question, QuestionOption) VALUES (?, ?)',
            (NewQuestion, NewQuestionOption))
        connection.commit()
        connection.close()

        # Flash success message and redirect
        flash('Question successfully Added!', 'success')
        return redirect('/Administrator_account')

    # Pass business sectors to the template
    return render_template('Administrator.html', user_name=user_name)


# Add new question options
@app.route('/Add_new_question_options', methods=['GET', 'POST'])
def AddQuestioOptionsn():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    

    if request.method == 'POST':
        QuestionOptionID = request.form['Question_option_ID']
        QuestionOption = request.form['Question_option']


        connection = sqlite3.connect('FoodwasteAppdatabase.db')
        cursor = connection.cursor()
        # Insert the new user into the database
        cursor.execute(
            'INSERT INTO QuestionsOptions (QuestionOption, Question_Id) VALUES (?, ?)',
            (QuestionOption, QuestionOptionID))
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


        connection = sqlite3.connect('FoodwasteAppdatabase.db')
        cursor = connection.cursor()
        # Insert the new user into the database
        cursor.execute(
            'INSERT INTO QuestionsOptionsAnswer (Question_Id, QuestionOptionAnswer) VALUES (?, ?)',
            (QuestionOptionID, QuestionOptionAnswer))
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
    user_name = session.get('name', 'User')  # Retrieve the user's name from the session

    return render_template('userAccount.html', user_name=user_name, questions=questions)


# Function to get all questions from the Questions table
def get_all_questions():
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()

    try:
        # Select all questions and their options from the Questions table
        cursor.execute("SELECT id, Question, QuestionOption FROM Questions")
        questions = []
        for question in cursor.fetchall():
            question_id, question_text, question_option = question
            
            # Fetch options if the question type is 'Dropdown' or 'Tick box'
            if question_option in ["Dropdown", "Tick box"]:
                cursor.execute("SELECT QuestionOption FROM QuestionsOptions WHERE Question_Id=?", (question_id,))
                options = [option[0] for option in cursor.fetchall()]
            else:
                options = []  # No options for Text area or Date and time

            questions.append({
                "id": question_id,
                "text": question_text,
                "type": question_option,
                "options": options
            })
    
    finally:
        connection.close()

    return questions




# Answer route
@app.route('/user_submitted_answers', methods=['POST'])
def UserAnswers():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    questions = get_all_questions()  # Retrieve all questions with options from the database
    
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

                # Fetch question text, handling potential NoneType
                question_data = cursor.execute("SELECT Question FROM Questions WHERE id=?", (question_id,)).fetchone()
                
                if question_data:
                    question_text = question_data[0]
                    
                    # Insert the question and its answer into the SubmittedAnswers table
                    cursor.execute(
                        'INSERT INTO SubmittedAnswers (Firstname, Question, QuestionAnswer) VALUES (?, ?, ?)',
                        (user_name, question_text, answer)
                    )
                else:
                    # Log an error if the question_id does not exist in the database
                    print(f"Warning: Question ID {question_id} not found in Questions table.")

        connection.commit()
        connection.close()

        # Calculate the correct answer percentage
        correct_percentage = calculate_correct_answer_percentage(user_answers)

        # Redirect based on the correct percentage
        if correct_percentage >= 75:
            # Redirect to a new route if percentage is 75% or higher
            flash(f'Congratulations! You answered {correct_percentage:.2f}% of questions correctly! You can now take the game', 'success')
            return redirect(url_for('user_account_game'))  # Replace 'user_account_game' with your desired route function
        else:
            # Flash message indicating they need a 75% score to play the game
            flash(f'Sorry, you need to score at least 75% of the quiz before you can play the game. You scored {correct_percentage:.2f}%. Please review your answers.', 'warning')
            return redirect(url_for('user_account'))

    # Redirect to the user account if the request method is not POST
    return render_template('userAccount.html', user_name=user_name, questions=questions)




# Sample answers for the crossword game
correct_answers = {
    "4": "PACKAGING",
    "5": "FOOD",
    "6": "REFRIGERATOR",
    "7": "STORAGE"
}


# User account redirected page
@app.route('/user_account_game', methods=['GET', 'POST'])
def user_account_game():
    user_name = session.get('name', 'User')  # Retrieve the user's name from the session
    
    # Correct answers for crossword cells based on the provided layout
    correct_answers = {
        "4_1": "P", "4_2": "A", "4_3": "C", "4_4": "K", "4_5": "A", "4_6": "G", "4_7": "I", "4_8": "N", "4_9": "G",
        "5_6": "F", "5_7": "O", "5_8": "O", "5_9": "D",
        "6_1": "R", "6_2": "E", "6_3": "F", "6_4": "R", "6_5": "I", "6_6": "G", "6_7": "E", "6_8": "R", "6_9": "A", "6_10": "T", "6_11": "O", "6_12": "R",
        "7_7": "S", "7_8": "T", "7_9": "O", "7_10": "R", "7_11": "A", "7_12": "G", "7_13": "E"
    }

    if request.method == 'POST':
        # Collect user's answers from the form
        user_answers = {f"{row}_{col}": request.form.get(f"answer_{row}_{col}", "").upper()
                        for row in range(1, 13) for col in range(1, 13) if f"{row}_{col}" in correct_answers}

        # Check answers
        correct_count = sum(1 for key, value in user_answers.items() if value == correct_answers.get(key, ""))
        total_clues = len(correct_answers)

        # Calculate correctness
        if correct_count == total_clues:
            flash("Congratulations! You've solved the crossword puzzle!", "success")
        else:
            flash(f"You got {correct_count}/{total_clues} correct. Try again!", "warning")

    # Pass the correct answers dictionary to help render the crossword structure
    return render_template('userAccountGame.html', user_name=user_name, correct_answers=correct_answers)
















# Function to calculate the percentage of correct answers
def calculate_correct_answer_percentage(user_answers):
    connection = sqlite3.connect('FoodwasteAppdatabase.db')
    cursor = connection.cursor()
    
    correct_count = 0  # Number of correctly answered questions
    total_questions = len(user_answers)  # Total questions answered

    # Check each submitted answer against the correct answer in the database
    for question_id, user_answer in user_answers.items():
        # Fetch the correct answer for the question from QuestionsOptionsAnswer
        correct_answer_data = cursor.execute(
            "SELECT QuestionOptionAnswer FROM QuestionsOptionsAnswer WHERE Question_Id=?", (question_id,)
        ).fetchone()
        
        if correct_answer_data:
            correct_answer = correct_answer_data[0]
            # Compare user answer with the correct answer
            if str(user_answer).strip().lower() == str(correct_answer).strip().lower():
                correct_count += 1  # Increment if the answer is correct

    connection.close()

    # Calculate the percentage of correct answers
    if total_questions > 0:
        correct_percentage = (correct_count / total_questions) * 100
    else:
        correct_percentage = 0

    return correct_percentage



































if __name__ == '__main__':
    app.run(debug=True) 