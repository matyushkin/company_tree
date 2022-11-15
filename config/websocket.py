import json
from datetime import date, datetime
from decimal import Decimal

from asgiref.sync import sync_to_async
from django.core import serializers

from company_tree.users.models import Employee


def json_serial(obj):
    """JSON serializer for datetime objects"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return str(obj)
    print(obj)
    raise TypeError("Type %s not serializable" % type(obj))


def model_to_json(data):
    dict_data = serializers.serialize("python", data)
    actual_data = [d["fields"] for d in dict_data]
    json_data = json.dumps(actual_data, default=json_serial)
    return json_data


@sync_to_async
def get_employees_of_department(department_id):
    d = int(department_id)
    data = Employee.objects.filter(departments__id=d)
    return model_to_json(data)


async def websocket_application(scope, receive, send):
    while True:
        event = await receive()

        if event["type"] == "websocket.connect":
            await send({"type": "websocket.accept"})

        if event["type"] == "websocket.disconnect":
            break

        if event["type"] == "websocket.receive":
            department_id = event["text"]
            data = await get_employees_of_department(department_id)
            await send({"type": "websocket.send", "text": data})
