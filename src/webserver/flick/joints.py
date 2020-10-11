from flask import (
    Blueprint, request, jsonify
)
from werkzeug.exceptions import abort
from .db import get_db

bp = Blueprint('joints', __name__)

@bp.route('/joints')
def get_joints():
    db = get_db()
    joints = db.execute(
        'SELECT joint_id, name, location, description FROM joints'
    ).fetchall()

    if not joints:
        abort(404, "No joints found.")

    return jsonify(joints)

@bp.route('/joints/<int:joint_id>')
def get_joint(joint_id):
    db = get_db()
    joint = db.execute(
        'SELECT joint_id, name, location, description FROM joints WHERE joint_id = ?',
        (joint_id,)
    ).fetchone()

    if joint is None:
        abort(404, "Joint id {0} doesn't exist.".format(joint_id))

    return jsonify(joint)

@bp.route('/joints/<int:joint_id>/menu')
def get_menu(joint_id):
    db = get_db()
    pizzas = db.execute(
        'SELECT pizza_id, name, toppings, vegetarian FROM pizzas WHERE joint_id = ?',
        (joint_id,)
    ).fetchall()

    if not pizzas:
        abort(404, "No pizzas found for this joint.")

    return jsonify(pizzas)

@bp.route('/joints/<int:joint_id>/rate', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':

        rating = 5;
        error = None

        if not (rating >= 0 and rating <= 5):
            error = 'Rating is invalid'
            abort(404, "No pizzas found for this joint.")
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')
