"""
Main entry point for the Stories of Stories backend API.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///stories.db'
)
app.config['JSON_SORT_KEYS'] = False

# Register blueprints (routes)
from routes.node import node_bp
from routes.choice import choice_bp
from routes.user import user_bp

app.register_blueprint(node_bp, url_prefix='/api/nodes')
app.register_blueprint(choice_bp, url_prefix='/api/choices')
app.register_blueprint(user_bp, url_prefix='/api/users')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'Stories of Stories API is running'
    }), 200


@app.route('/', methods=['GET'])
def root():
    """Root endpoint."""
    return jsonify({
        'name': 'Stories of Stories API',
        'version': '0.1.0',
        'description': 'Interactive storytelling platform'
    }), 200


if __name__ == '__main__':
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )
