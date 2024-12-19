from flask import Flask
from flask_cors import CORS 
from db import db, init_app 
from dotenv import load_dotenv
from flask_migrate import Migrate
from routes import register_routes 
from models import *  # Import all models 



# Create the Flask app
app = Flask(__name__)  

# Load environment variables
load_dotenv()  

# Initialize database
init_app(app)

migrate = Migrate(app, db)

# Enable CORS
CORS(app)
  
# Register Blueprints
register_routes(app)  

if __name__ == "__main__":
    app.run(debug=True)
