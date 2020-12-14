import markdown
import os
import shelve
# Import the framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("devices.db")
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)


class DeviceList(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        devices = []

        for key in keys:
            devices.append(shelf[key])

        return {'message': 'Success', 'data': devices}, 200

    def post(self):
        parser = reqparse.RequestParser()
        print(reqparse)
        print("Getting post req")
        parser.add_argument('device_type', required=True)
        parser.add_argument('device_name', required=False)
        parser.add_argument('device_codename', required=True)
        parser.add_argument('device_chipid', required=True)
        parser.add_argument('device_location', required=False)
        parser.add_argument('device_relaycount', required=True)
        parser.add_argument('device_fancount', required=True)
        parser.add_argument('device_imageurl', required=True)
        parser.add_argument('user_code', required=True)
        
        # Parse the arguments into an object
        args = parser.parse_args()
        #print(args)
        shelf = get_db()
        shelf[args['device_chipid']] = args

        return {'message': 'Device registered', 'data': args}, 201


class Device(Resource):
    def get(self, device_chipid):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (device_chipid in shelf):
            return {'message': 'Device not found', 'data': {}}, 404

        return {'message': 'Device found', 'data': shelf[device_chipid]}, 200

    def delete(self, device_chipid):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (device_chipid in shelf):
            return {'message': 'Device not found', 'data': {}}, 404

        del shelf[device_chipid]
        return '', 204

class Sinric(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        print("Getting post req")
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('chipid', required=True)
        parser.add_argument('codename',required=True)
        parser.add_argument('switch1', required=True)
        parser.add_argument('switch2', required=False)
        parser.add_argument('switch3', required=False)
        parser.add_argument('switch4', required=False)
        parser.add_argument('switch5', required=False)
        # Parse the arguments into an object
        args = parser.parse_args()

        if(args["switch5"] is not None):
            args["switch5"] = args["switch5"].replace(" ", "_")
            args["switch4"] = args["switch4"].replace(" ", "_")
            args["switch3"] = args["switch3"].replace(" ", "_")
            args["switch2"] = args["switch2"].replace(" ", "_")
            args["switch1"] = args["switch1"].replace(" ", "_")
            os.system('sudo python3 ~/Documents/Github/selenium_sinric/restful/sinric_script.py '+args['email']+' '+args['password']+' '+args["chipid"]+' '+args["codename"]+' '+args["switch1"]+' '+args["switch2"]+' '+args["switch3"]+' '+args["switch4"]+' '+args["switch5"])
        elif(args["switch4"] is not None):
            args["switch4"] = args["switch4"].replace(" ", "_")
            args["switch3"] = args["switch3"].replace(" ", "_")
            args["switch2"] = args["switch2"].replace(" ", "_")
            args["switch1"] = args["switch1"].replace(" ", "_")
            os.system('sudo python3 ~/Documents/Github/selenium_sinric/restful/sinric_script.py '+args['email']+' '+args['password']+' '+args["chipid"]+' '+args["codename"]+' '+args["switch1"]+' '+args["switch2"]+' '+args["switch3"]+' '+args["switch4"])
        elif(args["switch3"] is not None):
            args["switch3"] = args["switch3"].replace(" ", "_")
            args["switch2"] = args["switch2"].replace(" ", "_")
            args["switch1"] = args["switch1"].replace(" ", "_")
            os.system('sudo python3 ~/Documents/Github/selenium_sinric/restful/sinric_script.py '+args['email']+' '+args['password']+' '+args["chipid"]+' '+args["codename"]+' '+args["switch1"]+' '+args["switch2"]+' '+args["switch3"])
        elif(args["switch2"] is not None):
            args["switch2"] =  args["switch2"].replace(" ", "_")
            args["switch1"] = args["switch1"].replace(" ", "_")
            os.system('sudo python3 ~/Documents/Github/selenium_sinric/restful/sinric_script.py '+args['email']+' '+args['password']+' '+args["chipid"]+' '+args["codename"]+' '+args["switch1"]+' '+args["switch2"])
        else:
            args["switch1"] = args["switch1"].replace(" ", "_")
            os.system('sudo python3 ~/Documents/Github/selenium_sinric/restful/sinric_script.py '+args['email']+' '+args['password']+' '+args["chipid"]+' '+args["codename"]+' '+args["switch1"])        
        return {'message': 'Sinric script processed', 'data': args}, 201

    def delete(self):
        print(reqparse)
        parser = reqparse.RequestParser()
        print("Getting del req")
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('chipid', required=True)
        parser.add_argument('codename',required=True)
        # Parse the arguments into an object
        args = parser.parse_args()

        os.system('sudo python3 ~/Documents/Github/selenium_sinric/restful/sinric_script.py '+args['email']+' '+args['password']+' '+args["chipid"]+' '+args["codename"])
        return {'message': 'Sinric script processed', 'data': args}, 201

api.add_resource(DeviceList, '/devices/')
api.add_resource(Device, '/device/<string:device_chipid>/')
api.add_resource(Sinric, '/sinric/')



