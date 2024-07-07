from flask import Flask
from app.db import init_db
from app.routes import routes

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
