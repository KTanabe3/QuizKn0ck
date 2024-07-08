from flask import Flask, render_template, request, Response, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from models import db, User, quiz_quizsets, Quiz, QuizSet
from login import post_login, get_login, logout
from register import get_users, post_users, get_users_id, post_users_id

app = Flask(__name__)

DB_USER = "docker"
DB_PASS = "docker"
DB_HOST = "db"
DB_NAME = "flask_app"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = "secret"

migrate = Migrate(app, db)
login = LoginManager(app)

### 実装する機能の設定 #########################
app.register_blueprint(post_login)
app.register_blueprint(get_login)
app.register_blueprint(logout)

app.register_blueprint(get_users)
app.register_blueprint(post_users)
app.register_blueprint(get_users_id)
app.register_blueprint(post_users_id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/',methods=['GET'])
def top_get():
    return render_template('top.html')

@app.route('/home',methods=['GET'])
@login_required
def home_get():
    return render_template('home.html')


@app.route("/quiz",methods=['GET'])
def quiz_get():
    quizsets = QuizSet.query.all()
    return render_template('answer_quiz.html', quizsets=quizsets)

@app.route("/quiz/<id>", methods=['GET'])
def quiz_id_get(id):
    quizset = QuizSet.query.get(id)
    quizzes = quizset.quiz
    return render_template('answer_quiz_id.html', quizset = quizset, quizzes = quizzes)

@app.route("/make/quizset",methods=['GET'])
def make_quizset_get():
    quizzes = Quiz.query.all()
    return render_template('make_quiz_set.html', quizzes=quizzes)

@app.route("/make/quiz",methods=['GET'])
def make_quiz_get():
    return render_template('make_quiz.html')

@app.route("/view",methods=['GET'])
def view_get():
    return render_template('view_answer.html')

@app.route("/owner_view",methods=['GET'])
def owner_view_get():
    return render_template('view_other_answer.html')

@app.route("/make/quizset", methods=['POST'])
def make_quizset():
    quizset = QuizSet(
        title=request.form["title"]
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

@app.route("/make/quiz", methods=['POST'])
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

db.init_app(app)

@app.before_request
def init():
    db.create_all()
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
