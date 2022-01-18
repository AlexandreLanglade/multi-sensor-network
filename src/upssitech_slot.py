"""
API REST of the UPSSITECH slot.
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

import pandas as pd
from flask import Flask
from flask_restful import Api, Resource, reqparse

# init the api with flask
app = Flask(__name__)
api = Api(app)

"""
Each class in this file define a resource for the API.
The design is similar for all.
"""


class Weather(Resource):
    def get(self):
        """This function is the one executed for a GET request.

        Returns:
            dict, int: the dict contains the datas or an error message
            and the integer corresponds to the HTTP Status Code
        """
        data = pd.read_json(
            "C:/Users/Devel/Desktop/multi-sensor-network/data/weathers.json"
        )
        data = data.to_dict()
        return data, 200

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

        new_data = pd.DataFrame(
            [{"weatherId": args["weatherId"], "weather": args["weather"]}]
        )
        data = pd.read_json(
            "C:/Users/Devel/Desktop/multi-sensor-network/data/weathers.json"
        )

        if args["weatherId"] in list(data["weatherId"]):
            return {"message": f"id:{args['weatherId']} already exists."}, 401

        data = data.append(new_data, ignore_index=True)
        data.to_json("C:/Users/Devel/Desktop/multi-sensor-network/data/weathers.json")

        return data.to_dict(), 200


class Temperatures(Resource):
    def get(self):
        data = pd.read_json(
            "C:/Users/Devel/Desktop/multi-sensor-network/data/temperatures.json"
        )
        data = data.to_dict()
        return data, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("temperatureId", required=True)
        parser.add_argument("value", required=True)
        args = parser.parse_args()

        new_data = pd.DataFrame(
            [{"temperatureId": args["temperatureId"], "value": int(args["value"])}]
        )
        data = pd.read_json(
            "C:/Users/Devel/Desktop/multi-sensor-network/data/temperatures.json"
        )

        if args["temperatureId"] in list(data["temperatureId"]):
            return {"message": f"id:{args['temperatureId']} already exists."}, 401

        data = data.append(new_data, ignore_index=True)
        data.to_json(
            "C:/Users/Devel/Desktop/multi-sensor-network/data/temperatures.json"
        )

        return data.to_dict(), 200


class Devices(Resource):
    def get(self):
        data = pd.read_json(
            "C:/Users/Devel/Desktop/multi-sensor-network/data/devices.json"
        )
        data = data.to_dict()
        return data, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("deviceId", required=True)
        parser.add_argument("model", required=True)
        args = parser.parse_args()

        new_data = pd.DataFrame(
            [{"deviceId": args["deviceId"], "model": args["model"]}]
        )
        data = pd.read_json(
            "C:/Users/Devel/Desktop/multi-sensor-network/data/devices.json"
        )

        if args["deviceId"] in list(data["deviceId"]):
            return {"message": f"id:{args['deviceId']} already exists."}, 401

        data = data.append(new_data, ignore_index=True)
        data.to_json("C:/Users/Devel/Desktop/multi-sensor-network/data/devices.json")

        return data.to_dict(), 200


class Presences(Resource):
    def get(self):
        data = pd.read_json(
            "C:/Users/Devel/Desktop/multi-sensor-network/data/presences.json",
            convert_dates=False,
        )
        data = data.to_dict()
        return data, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("presenceId", required=True)
        parser.add_argument("datetime", required=True)
        args = parser.parse_args()

        new_data = pd.DataFrame(
            [{"presenceId": args["presenceId"], "datetime": args["datetime"]}]
        )
        data = pd.read_json(
            "C:/Users/Devel/Desktop/multi-sensor-network/data/presences.json",
            convert_dates=False,
        )
        if args["presenceId"] in list(data["presenceId"]):
            return {"message": f"id:{args['presenceId']} already exists."}, 401

        data = data.append(new_data, ignore_index=True)
        data.to_json("C:/Users/Devel/Desktop/multi-sensor-network/data/presences.json")

        return data.to_dict(), 200


# adding resources to the api
api.add_resource(Weather, "/weather")
api.add_resource(Temperatures, "/temperatures")
api.add_resource(Devices, "/devices")
api.add_resource(Presences, "/presences")

if __name__ == "__main__":
    app.run()
