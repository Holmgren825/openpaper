from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from openpaper.auth import login_required

bp = Blueprint('stream', __name__, url_prefix='/stream')


# function to return all published papers under the read view.
@bp.route('/')
def index():
    return render_template('stream/index.html')


# Open a published paper to read it.
@bp.route('/read/<int:id>')
def read_paper(id):
    post = get_post(id, check_author=False)
    return(render_template('stream/read.html', post=post))

# Slightly different compared to the read view. For this view, a login is
# required and we only show unpublished papers.
@bp.route('/review')
@login_required
def review():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, abstract, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE published = 0'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('stream/review.html', posts=posts)


# Methods for view for actually reviewing a paper
@bp.route('/review/<int:id>', methods=('POST', 'GET'))
@login_required
def review_paper(id):
    post = get_post_review(id)

    if request.method == 'POST':
        comment = request.form['new comment']
        approved = request.form.get('approved') != None
        error = None
        if not comment:
            error = 'Comment is required.'
        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'INSERT INTO reviews (post_id, reviewer_id, comment, approved)'
                ' VALUES (?, ?, ?, ?)',
                (post['id'], g.user['id'], comment, approved)
            )
            db.commit()

            if approved:
                db.execute('UPDATE post SET approvals = approvals + 1 WHERE id = ?', 
                (post['id'],)
                )
                db.execute('UPDATE post SET published = CASE WHEN approvals > 3 THEN 1 ELSE 0 END WHERE id = ?',
                (post['id'],)
                )
                db.commit()
            return redirect(url_for('stream.review_paper', id=post['id']))
    comments = get_post_comments(id)

    return render_template('stream/review_post.html', post=post,
                           comments=comments)


# View for creating a post.
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        abstract = request.form['abstract']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        elif not abstract:
            error = 'Abstract is required.'
        elif not body:
            error = 'Body is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, abstract, body, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, abstract, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('stream.index'))

    return render_template('stream/create.html')


# Get the current post through its id.
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, abstract, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


# Get the current post through its id for review.
def get_post_review(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, abstract, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] == g.user['id']:
        abort(403)

    return post


# Fetch all comments for a certain post.
def get_post_comments(id):
    comments = get_db().execute(
        'SELECT post_id, comment, r.created, approved'
        ' FROM reviews r JOIN post p ON r.post_id = p.id'
        ' WHERE post_id = ?',
        (id,)
    ).fetchall()

    return comments


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
