from flask import Blueprint, render_template, request, redirect, url_for, Response
from flask_login import current_user
from models import db, Quiz, QuizSet

make_quizset_get = Blueprint('make_quizset_get', __name__)
make_quizset_post = Blueprint('make_quizset_post', __name__)

# クイズセット作成画面へ遷移
@make_quizset_get.route("/make/quizset",methods=['GET'])
def get_make_quizset():
    quizzes = Quiz.query.all()
    return render_template('make_quiz_set.html', quizzes=quizzes)

# 作成したクイズセットの送信
@make_quizset_post.route("/make/quizset", methods=['POST'])
def make_quizset():
    quizset = QuizSet(
        title=request.form["title"],
        author_id=current_user.id
    )
    ids = request.form.getlist("id")
    setted_quiz = []
    for id in ids:
        quiz = Quiz.query.get(id)
        setted_quiz.append(quiz)

    quizset.quiz = setted_quiz

    db.session.add(quizset)
    db.session.commit()
    return redirect(url_for('home_get'))
