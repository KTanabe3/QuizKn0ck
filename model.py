from flask_sqlalchemy import SQLAlchemy

class Quiz(db.Model):
    #問題のID
    id = db.Column(db.Integer, primary_key=True)
    #問題のタイトル
    title = db.Column(db.String(128))
    #問題の本文
    text = db.Column(db.String(128))
    #問題の正答
    ans = db.Column(db.String(128))
    #以下ダミー候補
    cand1 = db.Column(db.String(128))
    cand2 = db.Column(db.String(128))
    cand3 = db.Column(db.String(128))

class Relation(db.Model):
    #問題セットのID
    set = db.Column(db.Integer)
    #問題のID
    quiz = db.Column(db.Integer)

class QuizSet(db.Model):
    #問題セットのID
    id = db.Column(db.Integer, primary_key=True)
    #セット作成者のuserID
    author = db.Column(db.Integer)
    #問題セットのタイトル
    title = db.Column(db.String(128))