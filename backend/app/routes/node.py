"""
Node routes - API endpoints for story node operations.
"""

from flask import Blueprint, jsonify, request

node_bp = Blueprint('node', __name__)


@node_bp.route('/', methods=['GET'])
def get_nodes():
    """Get all story nodes."""
    return jsonify({
        'status': 'success',
        'data': [],
        'message': 'Nodes endpoint'
    }), 200


@node_bp.route('/<int:node_id>', methods=['GET'])
def get_node(node_id):
    """Get a specific story node."""
    return jsonify({
        'status': 'success',
        'node_id': node_id,
        'message': f'Retrieved node {node_id}'
    }), 200


@node_bp.route('/', methods=['POST'])
def create_node():
    """Create a new story node."""
    data = request.get_json()
    return jsonify({
        'status': 'success',
        'data': data,
        'message': 'Node created'
    }), 201


@node_bp.route('/<int:node_id>', methods=['PUT'])
def update_node(node_id):
    """Update a story node."""
    data = request.get_json()
    return jsonify({
        'status': 'success',
        'node_id': node_id,
        'data': data,
        'message': f'Node {node_id} updated'
    }), 200


@node_bp.route('/<int:node_id>/choices', methods=['GET'])
def get_node_choices(node_id):
    """Get all choices for a specific node."""
    return jsonify({
        'status': 'success',
        'node_id': node_id,
        'choices': [],
        'message': f'Retrieved choices for node {node_id}'
    }), 200
