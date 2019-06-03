from flask import (
    Blueprint, flash, g, redirect, render_template, 
    request, url_for, current_app, session, jsonify
)
from werkzeug.exceptions import abort

from hotel.db import get_db
from hotel.forms import DateRangeForm
import datetime

from hotel.okta import oidc, get_oidc, init_app

from oauth2client.client import OAuth2Credentials

bp = Blueprint('rooms', __name__)

# # def __init__(self):
# with app.app_context():
#     oidc = g.pop('oidc',None)
#     okta_client = g.pop('okta_client',None)

# @bp.app_context_processor #with_appcontext
# oidc = g.pop('oidc',None)

@bp.route('/')
def index():
    """Show all the listings - raw list."""
    db = get_db()
    dates = db.execute(
        'SELECT l.id, l.listing_url, c.date, c.available, c.price '
        'FROM calendar c, listings l '
        'WHERE  (c.price is not "") and (c.listing_id = l.id) ' 
        'LIMIT 100 '
    ).fetchall()
    return render_template('rooms/index.html', dates=dates)


@bp.before_request
def before_request():
    print ('rooms.before_request call reached')
    with current_app.app_context():
        print ('rooms.before_request in app_context',g)
        oidc = g.pop('oidc',None)
        okta_client = g.pop('okta_client',None)
        if oidc is not None and okta_client is not None:
            print ('rooms.before_request g.oidc and g.okta_client available')
            if oidc.user_loggedin:
                # OpenID Token as 
                g.user = okta_client.get_user(oidc.user_getfield("sub"))
                g.oidc_id_token = OAuth2Credentials.from_json(g.oidc.credentials_store[info.get('sub')]).token_response['id_token']
            else:
                g.user = None
        else:
            print('rooms.beforerequest No user logged in')
            g.user = None


#example oidc require_login functon
# def require_login(loginfunc)
#     """ oidc related work 
#     connects to okta 
#     set some variable for loginfunc to use
#     """

"""
@oidc.require_login
If the user is not already logged in, they will be sent to the
Provider to log in, after which they will be returned.
"""
@bp.route('/login', methods=['GET', 'POST'])
# @oidc.require_login
def login():
    """
    Force the user to login, then redirect them to the get_books.
    Currently this code DOES NOT work
    Problem:
        * oidc global object is not available to pass request to okta
    Resolution:
        * redirecting to /calendar
    """
    # print('rooms.login entered ', request.url)
    
    # with current_app.app_context:
    #     init_app(current_app)

    # print('rooms.login oidc object exists?', (oidc is not None) )
    # print('rooms.login oidc object ' , dir(oidc))

    # print('rooms.login user logged in?', oidc.user_loggedin )
    # return oidc.redirect_to_auth_server(None,request.values)
    # # oidc.redirect_to_auth_server(None,request.url)  # redirect_to_auth_server(request.url)
    # # info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])
    # # print ('rooms.login:: oidc info info is',info)
    # # id_token = OAuth2Credentials.from_json(oidc.credentials_store[info.get('sub')]).token_response['id_token']
    # # if 'logged_in' not in session:
    # #     session['logged_in'] = False
    return redirect(url_for("rooms.calendar"))
 
@bp.route('/custom_callback')
@oidc.custom_callback
def callback(data):
    return 'Hello. You submitted %s' % data

@bp.route("/logout")
# @oidc.require_login
def logout():
    """
    Log the user out of their account.
    """
    info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])
    id_token = OAuth2Credentials.from_json(oidc.credentials_store[info.get('sub')]).token_response['id_token']
    # logout_request = base_url + logout_url + str(id_token) + logout_redirect_url
    base_url = "http://localhost:5000/"
    logout_url =  url_for("rooms.logout")
    logout_redirect_url =  url_for("rooms.index")
    # logout_request = str(id_token) 
    logout_request = base_url + logout_url + str(id_token) + logout_redirect_url

    # flash('routes::logout : Congratulations, you have logged out!')
    oidc.logout()
    session.clear()
    # info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])
    # id_token = OAuth2Credentials.from_json(oidc.credentials_store[info.get('sub')]).token_response['id_token']
    # flash('routes::logout : User Token ID {}'.format(id_token))

    return redirect(logout_request) #     redirect(url_for(".index"))


@bp.route('/calendar', methods=('GET', 'POST'))
def calendar():
    current_app.dates = []
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        error = None

        if not start_date:
            error = 'start date is required.'
    
        if not end_date:
            error = 'end date is required.'


        if error is not None:
            flash(error)
        else:    
            flash("start date  is {start_date} and end date is {end_date}".format(start_date= start_date, end_date= end_date))
            """Show all the posts, most recent first."""
            db = get_db()
            current_app.dates = db.execute(
                        'SELECT l.id, l.listing_url, c.date, c.available, c.price '
                        'FROM calendar c, listings l '
                        'WHERE  (c.price is not "") and (c.listing_id = l.id) ' 
                        'and c.date between ? and ? '
                        'GROUP BY l.id '
                        'LIMIT 10 ',
                        (start_date,end_date)
                ).fetchall()
            return redirect(url_for('rooms.show_listings'))
    return render_template('rooms/calendar.html', dates=current_app.dates)

@bp.route('/show_listings', methods=('GET', 'POST'))
def show_listings():
    dates = current_app.dates
    return render_template('rooms/listings.html', dates=dates)    



# def get_post(id, check_author=True):
#     """Get a post and its author by id.
#     Checks that the id exists and optionally that the current user is
#     the author.
#     :param id: id of post to get
#     :param check_author: require the current user to be the author
#     :return: the post with author information
#     :raise 404: if a post with the given id doesn't exist
#     :raise 403: if the current user isn't the author
#     """
#     post = get_db().execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()

#     if post is None:
#         abort(404, "Post id {0} doesn't exist.".format(id))

#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)

#     return post


# @bp.route('/create', methods=('GET', 'POST'))
# @login_required
# def create():
#     """Create a new post for the current user."""
#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'INSERT INTO post (title, body, author_id)'
#                 ' VALUES (?, ?, ?)',
#                 (title, body, g.user['id'])
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/create.html')


# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# @login_required
# def update(id):
#     """Update a post if the current user is the author."""
#     post = get_post(id)

#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET title = ?, body = ? WHERE id = ?',
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/update.html', post=post)


# @bp.route('/<int:id>/delete', methods=('POST',))
# @login_required
# def delete(id):
#     """Delete a post.
#     Ensures that the post exists and that the logged in user is the
#     author of the post.
#     """
#     get_post(id)
#     db = get_db()
#     db.execute('DELETE FROM post WHERE id = ?', (id,))
#     db.commit()
#     return redirect(url_for('blog.index'))
