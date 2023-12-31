"""Blogly application."""
from flask import Flask, request, redirect, render_template

from models import db, connect_db, User, Post, Tag

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
    users = User.query.all()
    posts = Post.query.order_by(Post.created_at.desc()).all()


    return render_template('home.html', users = users, posts = posts)

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

@app.route('/users/<int:uid>/post', methods = ['GET'])
def make_post(uid):
    user = User.query.get_or_404(uid)
    tags = Tag.query.all()

    return render_template('makepost.html', user = user, tags = tags)


@app.route('/users/<int:uid>/post/new', methods = ['POST'])
def create_post(uid):
    # user = User.query.get_or_404(uid)
    title = request.form.get('title')
    content = request.form.get('content')
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post = Post(
        title = title,
        content = content,
        user_id = uid,
        tags=tags
    )
    db.session.add(post)
    db.session.commit()
    

    return redirect(f'/users/{uid}')





@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a page with info on a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)




@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """edit current post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()


    return render_template('editPost.html', post = post, tags = tags)

@app.route('/posts/<int:post_id>/edit/post', methods = ['POST'])
def edit_post_apply(post_id):
    """edit current post"""
    post = Post.query.get_or_404(post_id)

    title = request.form.get('title')
    content = request.form.get('content')


    # Update only if the input field has a value
    if title:
        post.title = title
    if content:
        post.content = content

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods = ['POST'])
def delete_post(post_id):
    """delete current post"""

    post = Post.query.get_or_404(post_id)
    uid = post.user_id

    db.session.delete(post)
    db.session.commit()
    print(f'post id: {post_id} has been deleted')
    return redirect('/')

@app.route('/tags')
def show_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags = tags)

@app.route('/tags/<int:tid>')
def edit_tag(tid):
    tag = Tag.query.get_or_404(tid)
    return render_template('editTag.html', tag = tag)

@app.route('/tags/new')
def new_tag():

    return render_template('newTag.html')

@app.route('/tags/new/post', methods = ['POST'])
def create_new_tag():
    tagName = request.form.get('tagName')
    if tagName:
        tag = Tag(
            name = tagName
        )
    else:
        tag = Tag(
            name = 'N/A'
        )
    
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tid>/post', methods = ['POST'])
def appply_change_tag(tid):
    tag = Tag.query.get_or_404(tid)

    tagName = request.form.get('tagName')

    if tagName:
        tag.name = tagName

    db.session.add(tag)
    db.session.commit()
    return redirect('/')

@app.route('/tags/<int:tid>/delete', methods = ['POST'])
def delete_tag(tid):
    tag = Tag.query.get_or_404(tid)
    db.session.delete(tag)
    db.session.commit()
    print(f'tag id: {tag.id} has been deleted')

    return redirect('/')