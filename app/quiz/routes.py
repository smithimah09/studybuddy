import requests
from flask import Blueprint, render_template, request, flash
from flask_login import login_required

quiz = Blueprint('quiz', __name__, url_prefix='/quiz')

@quiz.route('/', methods=['GET', 'POST'])
@login_required
def quiz_home():
    questions = []
    if request.method == 'POST':
        amount = request.form.get('amount', 5)
        category = request.form.get('category', '')
        difficulty = request.form.get('difficulty', '')
        type_ = request.form.get('type', '')

        url = f"https://opentdb.com/api.php?amount=10"
        if category:
            url += f"&category={category}"
        if difficulty:
            url += f"&difficulty={difficulty}"
        if type_:
            url += f"&type={type_}"

        response = requests.get(url)
        data = response.json()

        if data["response_code"] == 0:
            questions = data["results"]
        else:
            flash("No questions found. Try adjusting your filters.", "warning")

    return render_template('quiz/quiz_home.html', questions=questions)
