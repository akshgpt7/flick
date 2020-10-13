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

    ids = db.execute('SELECT joint_id from joints').fetchall()
    found = False
    for id in ids:
        if joint_id == id[0]:
            found = True
            break
    
    if found:
        joint = db.execute(
            'SELECT j.joint_id, name, location, description, AVG(r.rating) '
            ' FROM joints j JOIN ratings r ON j.joint_id = r.joint_id'
            ' WHERE j.joint_id = ?',
            (joint_id,)
        ).fetchone()

        joint_json = {'joint_id': joint[0], 'name': joint[1],
                    'location': joint[2], 'description': joint[3],
                    'rating': joint[4] 
                    }
    
        return jsonify(joint_json)

    else:
        abort(404, "Joint id {0} doesn't exist.".format(joint_id))


@bp.route('/joints/<int:joint_id>/menu')
def menu(joint_id):
    db = get_db()

    ids = db.execute('SELECT joint_id from joints').fetchall()
    found = False
    for id in ids:
        if joint_id == id[0]:
            found = True
            break

    if found:
        pizzas = db.execute(
            'SELECT pizza_id, name, toppings, vegetarian FROM pizzas WHERE joint_id = ?',
            (joint_id,)
        ).fetchall()

        pizzas_json = []
        for p in pizzas:
            pizzas_json.append(
                # TODO: add pizza price
                {
                    'pizza_id': p[0], 'name': p[1], 'toppings': p[2],
                    'vegetarian': bool(p[3])
                }
            )

        return jsonify(pizzas_json)

    else:
        abort(404, "Joint id {0} doesn't exist.".format(joint_id))


@bp.route('/joints/<int:joint_id>/rate', methods=['POST'])
def rate(joint_id):
    db = get_db()

    ids = db.execute('SELECT joint_id from joints').fetchall()
    found = False
    for id in ids:
        if joint_id == id[0]:
            found = True
            break

    if found:    
        json = request.get_json(force=True)
        rating = json['rating']
        joint_id = json['joint_id']

        error = None

        db.execute(
            'INSERT INTO ratings'
            ' VALUES (?, ?)',
            (joint_id, rating)
        )
        db.commit()

    else:
        abort(404, "Joint id {0} doesn't exist.".format(joint_id))


