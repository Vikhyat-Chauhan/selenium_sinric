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
        
        # Parse the arguments into an object
        args = parser.parse_args()
        os.system('sudo python3 ~/Documents/Github/selenium_sinric/restful/sinric.py')
        return {'message': 'Sinric script processed', 'data': args}, 201

api.add_resource(DeviceList, '/devices/')
api.add_resource(Device, '/device/<string:device_chipid>/')
api.add_resource(Sinric, '/sinric/')



