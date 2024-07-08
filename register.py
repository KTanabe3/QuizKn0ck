from flask import Blueprint, render_template, request, redirect, url_for, Response
from flask_login import current_user, login_required
from models import db, User

get_users = Blueprint('get_users', __name__)
post_users = Blueprint('post_users', __name__)
get_users_id = Blueprint('get_users_id', __name__)
post_users_id = Blueprint('post_users_id', __name__)


@get_users.route("/users",methods=['GET'])
def users_get():
    users = User.query.all()
    return render_template('users_get.html', users=users)

@post_users.route("/users",methods=['POST'])
def users_post():
    user = User(
        name=request.form["user_name"],
        mail=request.form["mail"]
    )
    user.set_password(request.form["password"])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('top_get'))

@get_users_id.route("/users/<id>",methods=['GET'])
@login_required
def users_id_get(id):
    if str(current_user.id) != str(id):
        return Response(response="他人の個別ページは開けません", status=403)
    user = User.query.get(id)
    return render_template('users_id_get.html', user=user)

@post_users_id.route("/users/<id>/edit",methods=['POST'])
def users_id_post_edit(id):
    user = User.query.get(id)
    user.name = request.form["user_name"]
    db.session.merge(user)
    db.session.commit()
    return redirect(url_for('users_get'))