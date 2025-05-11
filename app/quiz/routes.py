import requests
from flask import Blueprint, render_template, request, flash, jsonify, session
from flask_login import login_required

quiz = Blueprint('quiz', __name__, url_prefix='/quiz')

@quiz.route('/', methods=['GET', 'POST'])
@login_required
def quiz_home():
    questions = []
    if request.method == 'POST':
        amount = request.form.get('amount', '')
        category = request.form.get('category', '')
        difficulty = request.form.get('difficulty', '')
        type_ = request.form.get('type', '')
        
        # Validate form inputs
        if not amount or int(amount) < 1:
            flash("Please select a valid number of questions.", "warning")
            return render_template('quiz/quiz_home.html', questions=[])
        
        # Build the API URL with the correct parameters
        url = f"https://opentdb.com/api.php?amount={amount}"
        if category:
            url += f"&category={category}"
        if difficulty:
            url += f"&difficulty={difficulty}"
        if type_:
            url += f"&type={type_}"

        try:
            response = requests.get(url)
            data = response.json()

            if data["response_code"] == 0 and data["results"]:
                questions = data["results"]
            else:
                flash("No questions found. Try adjusting your filters.", "warning")
        except Exception as e:
            flash(f"Error connecting to quiz API. Please try again.", "danger")
            print(f"API Error: {str(e)}")
            questions = []

    # Store questions in session for retrieval later
    if questions:
        session['quiz_questions'] = questions
    else:
        session.pop('quiz_questions', None)
    
    return render_template('quiz/quiz_home.html', questions=questions)


@quiz.route('/get_question_data', methods=['GET'])
@login_required
def get_question_data():
    """Get question data for a specific index"""
    index = request.args.get('index', 0, type=int)
    questions = session.get('quiz_questions', [])
    
    if not questions or index >= len(questions):
        return jsonify({})
    
    return jsonify(questions[index])
