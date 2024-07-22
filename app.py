from flask import Flask, render_template, request, Response, redirect, url_for, Blueprint
import random
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from models import db, User, quiz_quizsets, Quiz, QuizSet, Result
from login import post_login, get_login, logout
from register import get_users, post_users, get_users_id, post_users_id
from quiz import make_quiz_get, make_quiz_post
from quizset import make_quizset_get, make_quizset_post
from answer import quizset_get, quizset_id_get, answer_get, answer_post, result_get
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

app.register_blueprint(quizset_get)
app.register_blueprint(quizset_id_get)
app.register_blueprint(answer_get)
app.register_blueprint(answer_post)
app.register_blueprint(result_get)


app.register_blueprint(make_quiz_get)
app.register_blueprint(make_quiz_post)

app.register_blueprint(make_quizset_get)
app.register_blueprint(make_quizset_post)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/',methods=['GET'])
def top_get():
    return render_template('top.html')

@app.route('/home',methods=['GET'])
@login_required
def home_get():
    quizsets = QuizSet.query.filter_by(author_id=current_user.id)
    return render_template('home.html', quizsets=quizsets)

@app.route("/view",methods=['GET'])
def view_get():
    return render_template('view_answer.html')

@app.route("/owner_view",methods=['GET'])
def owner_view_get():
    return render_template('view_other_answer.html')

db.init_app(app)

@app.before_request
def init():
    db.create_all()
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
