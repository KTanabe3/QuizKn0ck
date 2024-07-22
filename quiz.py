from flask import Blueprint, render_template, request, redirect, url_for, Response
from models import db, Quiz

make_quiz_get = Blueprint('make_quiz_get', __name__)
make_quiz_post = Blueprint('make_quiz_post', __name__)

# クイズ作成画面へ遷移
@make_quiz_get.route("/make/quiz",methods=['GET'])
def get_make_quiz():
    return render_template('make_quiz.html')

# 作成したクイズの送信
@make_quiz_post.route("/make/quiz", methods=['POST'])
def make_quiz():
    quiz = Quiz(
        title=request.form["title"],
        text=request.form["text"],
        ans=request.form["ans"],
        cand1=request.form["cand1"],
        cand2=request.form["cand2"],
        cand3=request.form["cand3"]
    )
    db.session.add(quiz)
    db.session.commit()
    return redirect(url_for('home_get'))
