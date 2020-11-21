from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('stream', __name__, url_prefix='/stream')


# function to return all published papers under the read view.
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE published = 1'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('stream/index.html', posts=posts)


# Slightly different compared to the read view. For this view, a login is
# required and we only show unpublished papers.
@bp.route('/review')
@login_required
def review():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE published = 0'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('stream/review.html', posts=posts)


# View for creating a post.
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('stream.index'))

    return render_template('stream/create.html')


# Get the current post through its id.
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


# update post.
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('stream.index'))

    return render_template('stream/update.html', post=post)


# Remove post.
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('stream.index'))


# Old approve route. Probably changed soon.
@bp.route('/<int:id>/approve', methods=('POST',))
@login_required
def approve(id):
    get_post(id, check_author=False)
    db = get_db()
    db.execute('UPDATE post SET approvals = approvals + 1 WHERE id = ?', (id,))
    db.execute('UPDATE post SET published = CASE WHEN approvals > 3 THEN 1 ELSE 0 END WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('stream.index'))
