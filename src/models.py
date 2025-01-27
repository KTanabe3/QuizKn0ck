from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

#ユーザテーブル
class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    mail = db.Column(db.String(128), unique=True)
    # True: 教師, False: 学生
    role = db.Column(db.Boolean)
    password = db.Column(db.String(256))
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)

# 関係テーブル(Quiz <--> QuizSet)
quiz_quizsets = db.Table('quiz_quizsets',
    db.Column('quiz_id', db.Integer, db.ForeignKey('Quizzes.id'), primary_key=True),
    db.Column('quizset_id', db.Integer, db.ForeignKey('QuizSets.id'), primary_key=True)
)

# クイズテーブル
class Quiz(db.Model):
    __tablename__ = 'Quizzes'
    #問題のID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

class QuizSet(db.Model):
    __tablename__ = 'QuizSets'
    #問題セットのID
    id = db.Column(db.Integer, primary_key=True)
    #問題セットのタイトル
    title = db.Column(db.String(128))
    #双方の中間テーブルの設定
    quiz = db.relationship('Quiz', secondary=quiz_quizsets, backref=db.backref('quizsets', lazy=True))
    #作成者
    author_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    author = db.relationship('User', backref=db.backref('quizsets', lazy=True))

class Result(db.Model):
    __tablename__ = 'Results'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    total = db.Column(db.Integer)
    quizset_id = db.Column(db.Integer, db.ForeignKey('QuizSets.id'))
    quizset = db.relationship('QuizSet', backref=db.backref('results', lazy=True))
    answerer_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    answerer = db.relationship('User', backref=db.backref('results', lazy=True))

class Answer(db.Model):
    __tablename__ = 'Answers'
    id = db.Column(db.Integer, primary_key=True)
    ans = db.Column(db.String(128))
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quizzes.id'))
    quiz = db.relationship('Quiz', backref=db.backref('answers', lazy=True))
    result_id = db.Column(db.Integer, db.ForeignKey('Results.id'))
    result = db.relationship('Result', backref=db.backref('answers', lazy=True))
