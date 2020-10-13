from flask import (
    Blueprint, request, redirect, url_for, jsonify
)
from werkzeug.exceptions import abort
from .db import get_db
from .order_queues import queues
import json

bp = Blueprint('order', __name__)


@bp.route('/order', methods=['GET', 'POST',])
def order():
    if request.method == 'POST':

        # Retrieves JSON request and removes extra bracket
        order_request = json.loads(request.get_json(force=True))[0]
        order_details = json.dumps(order_request)

        joint_id = order_details['joint_id']
        pizza_id = order_details['order_details']['item_id']
        size = order_details['order_details']['size']

        db = get_db()
        details = db.execute(
            'SELECT name, toppings, ?'
            ' FROM pizzas i JOIN prices p ON i.pizza_id = r.pizza_id'
            ' WHERE i.pizza_id = ?',
            (size, pizza_id,)
        ).fetchone()

        details.append(db.execute(
            'SELECT name FROM joints'
            ' WHERE joint_id = ?',
            (joint_id,)
        ).fetchone())

        if joint_id in queues.keys():
            message = "Order placed successfully!"
        else:
            message = f"{joint_id} is not a valid joint id"
            abort(406, message)

        joint_order_queue = queues.get(joint_id)
        joint_order_queue.append(order_details)

        response_json = []

        if details is not None:
            response_json = {'pizza_name': order_details[0], 'toppings': order_details[1],
                            'price': order_details[2], 'joint_name': order_details[3],
                            'order_status': f'{message}'
                        }

        return jsonify(response_json)

        # return jsonify({'order_status': f'{message}'})

    else:
        return str(queues)

