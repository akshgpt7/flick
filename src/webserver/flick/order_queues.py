from .db import get_db


db = get_db()
joints = db.execute(
    'SELECT joint_id FROM joints'
).fetchall()

queues = {}

for j in joints:
    queues[j[0]] = []

