"""
API REST of the UPSSITECH slot.
entrypoint:
    https://multi-sensor-network-api.ew.r.appspot.com/
endpoints :
    - .../weathers :
        get/post data about the weather in Toulouse (virtual sensor)
    - .../temperatures :
        get/post data about temperatures in UPSSITECH  (field sensor)
    - .../presences :
        get/post data of the presence detector in UPSSITECH (field sensor)
    - .../devices :
        get/post data about devices that have been connected to the UPSSITECH network (virtual sensor)
    - .../aggregates :
        get/post the configuration(s) of the aggregate(s)
"""

import datetime
import json

from flask import Flask
from flask_restful import Api, Resource, reqparse
from google.cloud import firestore

# init the api with flask
app = Flask(__name__)
api = Api(app)

# connection to the Firestore database through the google cloud firestore API
database = firestore.Client(project="multi-sensor-network-api")


class Weathers(Resource):
    """
    Defines a type of resource for the API : weather
    """

    def get(self):
        """Executed when there is a GET request to /weathers

        Returns:
            dict, int: the dict contains the last 10 data sent by the virtual weather sensor
            and the integer corresponds to the HTTP Status Code
        """
        weathers_ref = database.collection(u"weathers")
        query = weathers_ref.order_by(
            u"timestamp", direction=firestore.Query.DESCENDING
        ).limit(10)
        results = query.stream()
        i = 0
        data = {}
        for doc in results:
            data[i] = doc.to_dict()
            data[i]["timestamp"] = data[i]["timestamp"].strftime("%d %m %Y %H %M %S")
            i += 1
        return data, 200

    def post(self):
        """Executed when there is a POST request to /weathers

        args required in the request:
            - timestamp : timestamp (%d %m %Y %H %M %S) of the request
            - temperature : temperature outside (Toulouse)
            - weather : weather description (Toulouse)

        Returns:
            dict, int: the dict contains the new data sent
            and the integer corresponds to the HTTP Status Code
        """
        parser = reqparse.RequestParser()
        parser.add_argument("timestamp", required=True)
        parser.add_argument("temperature", required=True)
        parser.add_argument("weather", required=True)
        args = parser.parse_args()

        data = {
            u"timestamp": datetime.datetime.strptime(
                args["timestamp"] + " +0100", "%d %m %Y %H %M %S %z"
            ),
            u"temperature": int(args["temperature"]),
            u"weather": args["weather"],
        }

        database.collection(u"weathers").add(data)

        # datetime is not JSON serializable
        data["timestamp"] = args["timestamp"]

        return data, 200


class Temperatures(Resource):
    """
    Defines a type of resource for the API : temperature
    """

    def get(self):
        """Executed when there is a GET request to /temperatures

        Returns:
            dict, int: the dict contains the last 10 data sent by the temperature sensor
            and the integer corresponds to the HTTP Status Code
        """
        temperatures_ref = database.collection(u"temperatures")
        query = temperatures_ref.order_by(
            u"timestamp", direction=firestore.Query.DESCENDING
        ).limit(10)
        results = query.stream()
        i = 0
        data = {}
        for doc in results:
            data[i] = doc.to_dict()
            data[i]["timestamp"] = data[i]["timestamp"].strftime("%d %m %Y %H %M %S")
            i += 1
        return data, 200

    def post(self):
        """Executed when there is a POST request to /temperatures

        args required in the request:
            - timestamp : timestamp (%d %m %Y %H %M %S) of the request
            - temperature : temperature inside (UPSSITECH)

        Returns:
            dict, int: the dict contains the new data sent
            and the integer corresponds to the HTTP Status Code
        """
        parser = reqparse.RequestParser()
        parser.add_argument("timestamp", required=True)
        parser.add_argument("temperature", required=True)
        args = parser.parse_args()

        data = {
            u"timestamp": datetime.datetime.strptime(
                args["timestamp"] + " +0100", "%d %m %Y %H %M %S %z"
            ),
            u"temperature": float(args["temperature"]),
        }

        database.collection(u"temperatures").add(data)

        # datetime is not JSON serializable
        data["timestamp"] = args["timestamp"]

        return data, 200


class Devices(Resource):
    """
    Defines a type of resource for the API : device
    """

    def get(self):
        """Executed when there is a GET request to /devices

        Returns:
            dict, int: the dict contains the last 10 data sent by the virtual device sensor
            and the integer corresponds to the HTTP Status Code
        """
        devices_ref = database.collection(u"devices")
        query = devices_ref.order_by(
            u"timestamp", direction=firestore.Query.DESCENDING
        ).limit(10)
        results = query.stream()
        i = 0
        data = {}
        for doc in results:
            data[i] = doc.to_dict()
            data[i]["timestamp"] = data[i]["timestamp"].strftime("%d %m %Y %H %M %S")
            i += 1
        return data, 200

    def post(self):
        """Executed when there is a POST request to /devices

        args required in the request:
            - timestamp : timestamp (%d %m %Y %H %M %S) of the request
            - device : model of the device that joined the network

        Returns:
            dict, int: the dict contains the new data sent
            and the integer corresponds to the HTTP Status Code
        """
        parser = reqparse.RequestParser()
        parser.add_argument("timestamp", required=True)
        parser.add_argument("device", required=True)
        args = parser.parse_args()

        data = {
            u"timestamp": datetime.datetime.strptime(
                args["timestamp"] + " +0100", "%d %m %Y %H %M %S %z"
            ),
            u"device": args["device"],
        }

        database.collection(u"devices").add(data)

        # datetime is not JSON serializable
        data["timestamp"] = args["timestamp"]

        return data, 200


class Presences(Resource):
    """
    Defines a type of resource for the API : presence
    """

    def get(self):
        """Executed when there is a GET request to /presences

        Returns:
            dict, int: the dict contains the last 10 data sent by the presence sensor
            and the integer corresponds to the HTTP Status Code
        """
        presences_ref = database.collection(u"presences")
        query = presences_ref.order_by(
            u"timestamp", direction=firestore.Query.DESCENDING
        ).limit(10)
        results = query.stream()
        i = 0
        data = {}
        for doc in results:
            data[i] = doc.to_dict()
            data[i]["timestamp"] = data[i]["timestamp"].strftime("%d %m %Y %H %M %S")
            i += 1
        return data, 200

    def post(self):
        """Executed when there is a POST request to /presences

        args required in the request:
            - timestamp : timestamp (%d %m %Y %H %M %S) of the request
                Corresponding to the timestamp of the presence detection

        Returns:
            dict, int: the dict contains the new data sent
            and the integer corresponds to the HTTP Status Code
        """
        parser = reqparse.RequestParser()
        parser.add_argument("timestamp", required=True)
        args = parser.parse_args()

        data = {
            u"timestamp": datetime.datetime.strptime(
                args["timestamp"] + " +0100", "%d %m %Y %H %M %S %z"
            )
        }

        database.collection(u"presences").add(data)

        # datetime is not JSON serializable
        data["timestamp"] = args["timestamp"]

        return data, 200


class Aggregates(Resource):
    """
    Defines a type of resource for the API : aggregate
    """

    def get(self):
        """Executed when there is a GET request to /weathers

        Returns:
            dict, int: the dict contains the config of the aggregates
            and the integer corresponds to the HTTP Status Code
        """
        docs = database.collection(u"aggregates").stream()
        i = 0
        data = {}
        for doc in docs:
            data[i] = doc.to_dict()
            i += 1
        return data, 200

    def post(self):
        """Executed when there is a POST request to /aggregates

        args required in the request:
            - name_aggregate : name of an aggregate
            - config : dict discribing the config of an aggregate

        Returns:
            dict, int: the dict contains the new data sent
            and the integer corresponds to the HTTP Status Code
        """
        parser = reqparse.RequestParser()
        parser.add_argument("name_aggregate", required=True)
        parser.add_argument("config", required=True)
        args = parser.parse_args()

        name_aggregate = args["name_aggregate"]

        config = args["config"].replace("'", '"')
        config = json.loads(config)

        data = {"config": config}

        database.collection(u"aggregates").document(name_aggregate).set(data)

        return data, 200


# adding resources to the api, defining endpoints
api.add_resource(Weathers, "/weathers")
api.add_resource(Temperatures, "/temperatures")
api.add_resource(Devices, "/devices")
api.add_resource(Presences, "/presences")
api.add_resource(Aggregates, "/aggregates")

if __name__ == "__main__":
    app.run()
