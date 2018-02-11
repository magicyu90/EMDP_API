# -*- coding: utf-8 -*-
from app.main import create_app
from flask_script import Manager, Server

app = create_app()
manager = Manager(app)

manager.add_command('runserver', Server(host='0.0.0.0', port=5001, use_debugger=True))

if __name__ == '__main__':
    manager.run()
