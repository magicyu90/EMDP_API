from flask import Flask, g
from flask_restful import reqparse, abort, Api, Resource
from api.resources.devicestat import DeviceStat,DeviceStatResourceFields
from flask_restful_swagger import swagger

app = Flask(__name__)
#app.register_blueprint(api_bp, url_prefix='/api')
#api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url='/api/spec')
api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url='/api/swagger')
api.add_resource(DeviceStat, '/api/devicestat')

if __name__ == '__main__':
    DeviceStatResourceFields()
    app.run(host='0.0.0.0', port=5001, debug=True)
