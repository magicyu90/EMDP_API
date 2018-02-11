from flask import Flask
from src.resources.devicestat import DeviceStatResourceFields
from src.resources.route import emdp_blueprint1
from flask import Flask, Blueprint
from flask_restful import Api
from flask_restful_swagger import swagger


if __name__ == '__main__':
    DeviceStatResourceFields()
    app = Flask(__name__)
    app.register_blueprint(emdp_blueprint1, url_prefix='/api')
    app.run(host='0.0.0.0', port=5001, debug=True)
