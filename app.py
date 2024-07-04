from flask import Flask, render_template, request, Response, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from models import db, User, quiz_quizsets, Quiz, QuizSet
from app_post_login import post_login

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

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/home',methods=['GET'])
@login_required
def home_get():
    return render_template('home.html')

@app.route('/login', methods=['GET'])
def login_get():
    # 現在のユーザーがログイン済みの場合
    if current_user.is_authenticated:
        # トップページに移動
        return redirect(url_for('home_get'))
    # loginページのテンプレートを返す
    return render_template('login.html')

@app.route('/logout')
def logout():
  # logout_user関数を呼び出し
  logout_user()
  # トップページにリダイレクト
  return redirect(url_for('home_get'))

@app.route("/users",methods=['GET'])
def users_get():
    users = User.query.all()
    return render_template('users_get.html', users=users)

@app.route("/users",methods=['POST'])
def users_post():
    user = User(
        name=request.form["user_name"],
        mail=request.form["mail"]
    )
    user.set_password(request.form["password"])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('users_get'))

@app.route("/users/<id>",methods=['GET'])
@login_required
def users_id_get(id):
    if str(current_user.id) != str(id):
        return Response(response="他人の個別ページは開けません", status=403)
    user = User.query.get(id)
    return render_template('users_id_get.html', user=user)

@app.route("/users/<id>/edit",methods=['POST'])
def users_id_post_edit(id):
    user = User.query.get(id)
    user.name = request.form["user_name"]
    db.session.merge(user)
    db.session.commit()
    return redirect(url_for('users_get'))


@app.route("/quiz",methods=['GET'])
def quiz_get():
    quizzes = Quiz.query.all()
    return render_template('answer_quiz.html', quizzes=quizzes)

@app.route("/make/quizset",methods=['GET'])
def make_quizset_get():
    return render_template('make_quiz_set.html')

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
    quizset = Quizset(
        title=request.form["title"]
    )
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
