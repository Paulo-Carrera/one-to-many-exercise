"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "P@ulo445"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return redirect('/users')


@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users = users)


@app.route('/users/new', methods = ['GET'])
def new_user():
    return render_template('new_user.html')


@app.route('/users/new', methods = ['POST'])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None 

    new_user = User(first_name = first_name , last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user_id).all()
    return render_template('user_detail.html', user = user, posts = posts)


@app.route('/users/<int:user_id>/edit', methods = ['GET'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user = user)


@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url'] or None

    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new', methods = ['GET'])
def new_post(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('new_post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods = ['POST'])
def create_post(user_id):
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title = title, content = content, user = user)
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('show_user', user_id = user_id))


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post = post)


@app.route('/posts/<int:post_id>/edit', methods = ['GET'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post = post)

@app.route('/posts/<int:post_id>/edit', methods = ['POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()

    return redirect(url_for('show_post', post_id = post_id))


@app.route('/posts/<int:post_id>/delete', methods = ['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('show_user', user_id = post.user_id))



if __name__ == '__main__':
    app.run(debug=True)



