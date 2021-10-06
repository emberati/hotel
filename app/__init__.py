from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
#login = LoginManager(app)

if __name__ == "__main__":
    app.run(debug=True)


from app import routes, models
