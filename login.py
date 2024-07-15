from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from models import db, User

post_login = Blueprint('post_login', __name__)
get_login = Blueprint('get_login', __name__)
logout = Blueprint('logout', __name__)

@get_login.route('/login', methods=['GET'])
def login_get():
    # 現在のユーザーがログイン済みの場合
    if current_user.is_authenticated:
        # トップページに移動
        return redirect(url_for('home_get'))
    # loginページのテンプレートを返す
    return render_template('login.html')


@post_login.route("/login",methods=['POST'])
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

@logout.route('/logout')
def logout_get():
    # logout_user関数を呼び出し
    logout_user()
    # トップページにリダイレクト
    return redirect(url_for('home_get'))