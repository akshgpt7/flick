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
    else:
        joints_json = []
        for j in joints:
            joints_json.append(
                {
                    'joint_id': j[0], 'name': j[1], 'location': j[2],
                    'description': j[3]
                 }
            )

    return jsonify(joints_json)


@bp.route('/joints/ratings')
def ratings():
    db = get_db()
    ratings = db.execute(
        'SELECT joint_id, AVG(rating) FROM ratings GROUP BY joint_id'
    ).fetchall()

    ratings_json = []
    for r in ratings:
        ratings_json.append({'joint_id': r[0], 'rating': r[1]})

    return jsonify(ratings_json)


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
    else:
        joint_json = {'joint_id': joint[0], 'name': joint[1],
                      'location': joint[2], 'description': joint[3],
                      'rating': joint[4]
                      }

    return jsonify(joint_json)


@bp.route('/joints/<int:joint_id>/menu')
def menu(joint_id):
    db = get_db()
    pizzas = db.execute(
        'SELECT m.pizza_id, name, toppings, vegetarian, p.small, p.medium, p.large'
        ' FROM pizzas m JOIN prices p ON m.pizza_id = p.pizza_id'
        ' WHERE m.joint_id = ?',
        (joint_id,)
    ).fetchall()

    if not pizzas:
        abort(404, "No pizzas found for this joint.")
    else:
        pizzas_json = []
        for p in pizzas:
            prices = []
            prices.append(
                {'S': p[4], 'M': p[5], 'L': p[6]}
            )
            pizzas_json.append(
                {
                    'pizza_id': p[0], 'name': p[1], 'toppings': p[2],
                    'vegetarian': bool(p[3]), 'prices': prices
                }
            )

    return jsonify(pizzas_json)


@bp.route('/joints/<int:joint_id>/rate', methods=['POST'])
def rate(joint_id):
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
        db.execute(
            'INSERT INTO ratings'
            ' VALUES (?, ?)',
            (joint_id, rating)
        )
        db.commit()

    return redirect(url_for('joints.joint', joint_id=joint_id))

