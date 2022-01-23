"""
API REST of the UPSSITECH slot.
entrypoint:
    https://multi-sensor-network-api.ew.r.appspot.com/
endpoints :
    - .../weathers :
        get/post datas about the weather in Toulouse (virtual sensor)
    - .../temperatures :
        get/post datas about temperatures in UPSSITECH  (field sensor)
    - .../presences :
        get/post datas of the presence detector in UPSSITECH (field sensor)
    - .../devices :
        get/post datas about devices connected UPSSITECH netwok (virtual sensor)
"""

from flask import Flask
from flask_restful import Api, Resource, reqparse
from google.cloud import firestore

# init the api with flask
app = Flask(__name__)
api = Api(app)

# connection to the Firestore database through the google cloud firestore API
database = firestore.Client(project="multi-sensor-network-api")
# links to the documents that contain sensors' datas
doc_temperatures = database.collection("datas").document("temperatures")
doc_devices = database.collection("datas").document("devices")
doc_presences = database.collection("datas").document("presences")
doc_weathers = database.collection("datas").document("weathers")


class Weathers(Resource):
    """
    Each class in this file define a resource for the API.
    The design is similar for all.
    """

    def get(self):
        """This function is the one executed for a GET request.

        Returns:
            dict, int: the dict contains the datas or an error message
            and the integer corresponds to the HTTP Status Code
        """
        return doc_weathers.get().to_dict(), 200

    def post(self):
        """This function is the one executed for a POST request.

        Returns:
            dict, int: the dict contains the datas updated or an error message
            and the integer corresponds to the HTTP Status Code
        """
        parser = reqparse.RequestParser()
        parser.add_argument("weatherId", required=True)
        parser.add_argument("weather", required=True)
        args = parser.parse_args()

        datas = doc_weathers.get().to_dict()

        if args["weatherId"] in datas:
            return {"message": f"id:{args['weatherId']} already exists."}, 401

        datas[args["weatherId"]] = args["weather"]
        doc_weathers.set(datas)

        return datas, 200


class Temperatures(Resource):
    def get(self):
        return doc_temperatures.get().to_dict(), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("temperatureId", required=True)
        parser.add_argument("temperature", required=True)
        args = parser.parse_args()

        datas = doc_temperatures.get().to_dict()

        if args["temperatureId"] in datas:
            return {"message": f"id:{args['temperatureId']} already exists."}, 401

        datas[args["temperatureId"]] = args["temperature"]
        doc_temperatures.set(datas)

        return datas, 200


class Devices(Resource):
    def get(self):
        return doc_devices.get().to_dict(), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("deviceId", required=True)
        parser.add_argument("device", required=True)
        args = parser.parse_args()

        datas = doc_devices.get().to_dict()

        if args["deviceId"] in datas:
            return {"message": f"id:{args['deviceId']} already exists."}, 401

        datas[args["deviceId"]] = args["device"]
        doc_devices.set(datas)

        return datas, 200


class Presences(Resource):
    def get(self):
        return doc_presences.get().to_dict(), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("presenceId", required=True)
        parser.add_argument("presence", required=True)
        args = parser.parse_args()

        datas = doc_presences.get().to_dict()

        if args["presenceId"] in datas:
            return {"message": f"id:{args['presenceId']} already exists."}, 401

        datas[args["presenceId"]] = args["presence"]
        doc_presences.set(datas)

        return datas, 200


# adding resources to the api
api.add_resource(Weathers, "/weathers")
api.add_resource(Temperatures, "/temperatures")
api.add_resource(Devices, "/devices")
api.add_resource(Presences, "/presences")

if __name__ == "__main__":
    app.run()
