from flask import (
    Blueprint, request, redirect, url_for, jsonify
)
from werkzeug.exceptions import abort
from .db import get_db
from .order_queues import queues

bp = Blueprint('order', __name__)


@bp.route('/order', methods=['GET', 'POST',])
def order():
    if request.method == 'POST':
        order_details = request.get_json(force=True)
        joint_id = order_details.get('joint_id')

        if joint_id in queues.keys():
            message = "Order placed successfully!"
        else:
            message = f"{joint_id} is not a valid joint id"
            abort(406, message)

        joint_order_queue = queues.get(joint_id)
        joint_order_queue.append(order_details['details'])

        return jsonify({'order_status': f'{message}'})

    else:
        return str(queues)

