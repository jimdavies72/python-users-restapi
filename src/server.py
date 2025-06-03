import os
from dotenv import load_dotenv
from flask import Flask
from users.user_routes import users_blueprint
from db.connection import connect_to_db

load_dotenv()

port = int(os.getenv("PORT") or 5001)

app = Flask(__name__)

# Connect to MongoDB and attach the db handle to the app
client = connect_to_db()
#app.db = client[os.getenv("MONGO_DB")]
app.config["db"] = client[os.getenv("MONGO_DB")]

# Register the blueprint
app.register_blueprint(users_blueprint, url_prefix='/users')

if __name__ == '__main__':
    print(f"Server running on port {port}")
    app.run(debug=True, port=port)