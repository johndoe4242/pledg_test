import json

from flask import Response
from flask import request

from app import app, constants
from app.services import PurchasesService


@app.route('/api/v1.0/purchases', methods=['POST'])
def create_purchase():
    raise NotImplementedError


@app.route('/api/v1.0/purchases', methods=['GET'])
def list_purchases():
    """Retrieve a list of purchases. Could be filtered by using the """

    status = request.args.get('status', None)
    purchases = PurchasesService().list(status=status)
    data = {'purchases': [purchase.to_dict() for purchase in purchases]}

    return Response(
        json.dumps(data),
        status=constants.HTTP_OK,
        mimetype='application/json',
    )
