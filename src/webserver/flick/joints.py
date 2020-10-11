from flask import (
    Blueprint, request, redirect, url_for, jsonify
)
from werkzeug.exceptions import abort
from .db import get_db

bp = Blueprint('joints', __name__)

@bp.route('/joints')
def joints():
    db = get_db()
    joints = db.execute(
        'SELECT joint_id, name, location, description FROM joints'
    ).fetchall()

    if not joints:
        abort(404, "No joints found.")

    return jsonify(joints)

@bp.route('/joints/<int:joint_id>')
def joint(joint_id):
    db = get_db()
    joint = db.execute(
        'SELECT j.joint_id, name, location, description, AVG(r.rating) '
        ' FROM joints j JOIN ratings r ON j.joint_id = r.joint_id'
        ' WHERE j.joint_id = ?',
        (joint_id,)
    ).fetchone()

    if joint is None:
        abort(404, "Joint id {0} doesn't exist.".format(joint_id))

    return jsonify(joint)

@bp.route('/joints/<int:joint_id>/menu')
def menu(joint_id):
    db = get_db()
    pizzas = db.execute(
        'SELECT pizza_id, name, toppings, vegetarian FROM pizzas WHERE joint_id = ?',
        (joint_id,)
    ).fetchall()

    if not pizzas:
        abort(404, "No pizzas found for this joint.")

    return jsonify(pizzas)

@bp.route('/joints/<int:joint_id>/rate', methods=['GET','POST',])
def rate(joint_id):
    if request.method == 'POST':

        # TODO: Change rating to user input from CLI
        rating = 5
        error = None

        # Checks that input is valid
        if not (0 <= rating <= 5):
            error = "Invalid rating."

        if error is not None:
            # TODO: Display the error to the user
            return error
        else:
            db = get_db()
            db.execute(
                'INSERT INTO ratings'
                ' VALUES (?, ?)',
                (joint_id, rating)
            )
            db.commit()

    return redirect(url_for('joints.joint', joint_id=joint_id))
