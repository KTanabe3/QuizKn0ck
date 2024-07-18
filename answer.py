from flask import Blueprint, render_template, request, redirect, url_for, Response
from models import db, Quiz, QuizSet, User

quizset_get = Blueprint('quiz_get', __name__)
quizset_id_get = Blueprint('quiz_id_get', __name__)
answer_get = Blueprint('answer_get', __name__)
answer_post = Blueprint('answer_post', __name__)

# クイズへの遷移選択画面へ遷移
@quizset_get.route("/quiz",methods=['GET'])
def get_quizset():
    quizsets = QuizSet.query.all()
    return render_template('answer_quiz.html', quizsets=quizsets)

# クイズセットの詳細画面へ遷移
@quizset_id_get.route("/quiz/<id>", methods=['GET'])
def get_quizset_id(id):
    quizset = QuizSet.query.get(id)
    quizzes = quizset.quiz
    quiz = Quiz.query.all()
    return render_template('answer_quiz_id.html', quizset = quizset, quizzes = quizzes, quiz = quiz)

# クイズセットの解答画面へ遷移
@answer_get.route("/quiz/<id>/answer", methods=['GET'])
def get_answer(id):
    quizset = QuizSet.query.get(id)
    quizzes = quizset.quiz
    quiz = Quiz.query.all()

    # シャッフルされた選択肢を含む辞書のリストを作成
    quizzes_with_choices = []
    for quiz in quizzes:
        choices = [quiz.ans, quiz.cand1, quiz.cand2, quiz.cand3]
        random.shuffle(choices)
        quiz_dict = {
            'id': quiz.id,
            'title': quiz.title,
            'text': quiz.text,
            'choices': choices
        }
        quizzes_with_choices.append(quiz_dict)

    return render_template('answer.html', quizset=quizset, quizzes=quizzes_with_choices)

# クイズの解答を送信し、正答数を算出
@answer_post.route("/quiz/<id>/answer", methods=['POST'])
def post_answer(id):    
    quizset = QuizSet.query.get(id)
    quizzes = quizset.quiz
    count = 0
    for quiz in quizzes:
        ans = request.form.get(f"quiz_{quiz.id}")
        if ans == quiz.ans:
            count += 1

    return redirect(url_for('home_get'))
