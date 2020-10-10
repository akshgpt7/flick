from flask import (
    Blueprint, jsonify
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

@bp.route('/joints/<int:id>')
def get_joint(joint_id):
    db = get_db()
    joint = db.execute(
        'SELECT joint_id, name, location, description FROM joints WHERE joint_id = ?',
        (joint_id,)
    ).fetchone()

    if joint is None:
        abort(404, "Joint id {0} doesn't exist.".format(joint_id))

    return jsonify(joint)
