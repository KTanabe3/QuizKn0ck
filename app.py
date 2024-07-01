from flask import Flask, render_template, request, Response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DB_USER = "docker"
DB_PASS = "docker"
DB_HOST = "db"
DB_NAME = "flask_app"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = "secret"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

### テーブル設定 ###############################

#ユーザテーブル
class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    mail = db.Column(db.String(128), unique=True)
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
    #セット作成者のuserID
    author = db.Column(db.Integer)
    #問題セットのタイトル
    title = db.Column(db.String(128))
    #双方の中間テーブルの設定
    quiz = db.relationship('Quiz', secondary=quiz_quizsets, backref=db.backref('quizsets', lazy=True))

### 実装する機能の設定 #########################

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

@app.route('/login', methods=['POST'])
def login_post():
    user = User.query.filter_by(mail=request.form["mail"]).one_or_none()
    
    # ユーザが存在しない or パスワードが間違っている時
    if user is None or not user.check_password(request.form["password"]):
        # メッセージの表示
        flash('メールアドレスかパスワードが間違っています')
        # loginページへリダイレクト
        return redirect(url_for('login_get'))

    # ログインを承認
    login_user(user)
    # トップページへリダイレクト
    return redirect(url_for('home_get'))

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

@app.route("/make",methods=['GET'])
def make_get():
    return render_template('make_quiz.html')

@app.route("/view",methods=['GET'])
def view_get():
    return render_template('view_answer.html')

@app.route("/owner_view",methods=['GET'])
def owner_view_get():
    return render_template('view_other_answer.html')

@app.route("/make", methods=['POST'])
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
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
