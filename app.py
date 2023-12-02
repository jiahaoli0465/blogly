"""Blogly application."""
from flask import Flask, request, redirect, render_template

from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'
app.debug = True



connect_db(app)
with app.app_context():
    db.create_all()



@app.route('/')
def show_home():
    return render_template('home.html')

@app.route('/newuser')
def new_user():


    return render_template('newuser.html')

@app.route('/newuser/new', methods = ['POST'])
def make_user():
    new_user = User(
    first_name = request.form['firstName'],
    last_name = request.form['lastName'],
    image_url = request.form['imgurl'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users')
def show_users():

    users =  User.query.order_by(User.last_name, User.first_name).all()

    return render_template('users.html', users = users)

@app.route('/users/<int:uid>')
def show_profile(uid):

    user = User.query.get_or_404(uid)
    return render_template('profile.html', user = user)


@app.route('/users/<int:uid>/delete', methods=["POST"])
def delete(uid):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(uid)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:uid>/edit')
def show_edit(uid):

    user = User.query.get_or_404(uid)


    return render_template('edit.html', user = user)

@app.route('/users/<int:uid>/edit/post', methods=['POST'])
def edit(uid):
    user = User.query.get_or_404(uid)

    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    image_url = request.form.get('imgurl')

    # Update only if the input field has a value
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if image_url:
        user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect("/users")