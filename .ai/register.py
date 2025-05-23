"""
Register AI Collaboration System
============================

This script registers all components of the AI collaboration system with 
the main application, initializing the necessary data structures and API endpoints.
"""

import os
import sys
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_ai_collaboration_system(app, github_integration=None):
    """
    Register all AI collaboration components
    
    Args:
        app: Flask application
        github_integration: Optional GitHub integration instance
    """
    logger.info("Registering AI Collaboration System...")
    
    # Register Protocol Harmonizer
    try:
        from register_protocol_harmonizer import register_protocol_harmonizer
        register_protocol_harmonizer(app, github_integration)
        logger.info("Protocol Harmonizer registered successfully")
    except Exception as e:
        logger.error(f"Error registering Protocol Harmonizer: {str(e)}")
    
    # Initialize Self-Evolving Threads
    try:
        from self_evolving_threads import SelfEvolvingThreads
        evolution_threads = SelfEvolvingThreads(github_integration)
        logger.info("Self-Evolving Threads initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing Self-Evolving Threads: {str(e)}")
    
    # Register AI Discovery Trails
    try:
        from ai_discovery_trails import initialize_discovery_trails
        initialize_discovery_trails(github_integration)
        logger.info("AI Discovery Trails initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing AI Discovery Trails: {str(e)}")
    
    # Register AI Collaboration Hub
    try:
        from ai_collaboration_hub import register_collaboration_hub
        register_collaboration_hub(app)
        logger.info("AI Collaboration Hub registered successfully")
    except Exception as e:
        logger.error(f"Error registering AI Collaboration Hub: {str(e)}")
    
    # Register Flask routes
    register_collaboration_routes(app, github_integration)
    
    logger.info("AI Collaboration System registered successfully!")

def register_collaboration_routes(app, github_integration=None):
    """
    Register Flask routes for the AI collaboration system
    
    Args:
        app: Flask application
        github_integration: Optional GitHub integration instance
    """
    from flask import Blueprint, request, jsonify, render_template
    
    # Create blueprint
    collab_bp = Blueprint('ai_collaboration', __name__, url_prefix='/ai-collaboration')
    
    @collab_bp.route('/', methods=['GET'])
    def collaboration_dashboard():
        """Display AI Collaboration Dashboard"""
        return render_template('ai_collaboration_dashboard.html')
    
    @collab_bp.route('/threads', methods=['GET'])
    def list_threads():
        """List all evolution threads"""
        try:
            from self_evolving_threads import list_active_evolution_threads
            
            repo = request.args.get('repo', 'sunheart-core')
            threads = list_active_evolution_threads(repo)
            
            return jsonify({
                "success": True,
                "threads": threads
            })
        except Exception as e:
            logger.error(f"Error listing threads: {str(e)}")
            return jsonify({"success": False, "error": str(e)}), 500
    
    @collab_bp.route('/threads/create', methods=['POST'])
    def create_thread():
        """Create a new evolution thread"""
        try:
            from self_evolving_threads import create_evolution_thread
            
            data = request.json
            if not data:
                return jsonify({"success": False, "error": "No JSON data provided"}), 400
            
            # Validate required fields
            required_fields = ['name', 'description', 'creator', 'strategy']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                }), 400
            
            repo = data.get('repository', 'sunheart-core')
            initial_goals = data.get('initial_goals', [])
            
            thread_id = create_evolution_thread(
                name=data['name'],
                description=data['description'],
                creator=data['creator'],
                strategy=data['strategy'],
                initial_goals=initial_goals,
                repository=repo
            )
            
            if thread_id:
                return jsonify({
                    "success": True,
                    "thread_id": thread_id,
                    "message": f"Evolution thread '{data['name']}' created successfully"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Failed to create evolution thread"
                }), 500
        except Exception as e:
            logger.error(f"Error creating thread: {str(e)}")
            return jsonify({"success": False, "error": str(e)}), 500
    
    @collab_bp.route('/threads/<thread_id>', methods=['GET'])
    def get_thread(thread_id):
        """Get thread details"""
        try:
            from self_evolving_threads import get_evolution_thread
            
            repo = request.args.get('repo', 'sunheart-core')
            thread = get_evolution_thread(thread_id, repo)
            
            if thread:
                return jsonify({
                    "success": True,
                    "thread": thread
                })
            else:
                return jsonify({
                    "success": False,
                    "error": f"Thread {thread_id} not found"
                }), 404
        except Exception as e:
            logger.error(f"Error getting thread: {str(e)}")
            return jsonify({"success": False, "error": str(e)}), 500
    
    @collab_bp.route('/threads/<thread_id>/steps', methods=['POST'])
    def add_step(thread_id):
        """Add an evolution step to a thread"""
        try:
            from self_evolving_threads import add_evolution_step
            
            data = request.json
            if not data:
                return jsonify({"success": False, "error": "No JSON data provided"}), 400
            
            # Validate required fields
            required_fields = ['title', 'description', 'goals_advanced', 'changes_made', 'outcome', 'ai_participant']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                }), 400
            
            repo = data.get('repository', 'sunheart-core')
            
            step_id = add_evolution_step(
                thread_id=thread_id,
                title=data['title'],
                description=data['description'],
                goals_advanced=data['goals_advanced'],
                changes_made=data['changes_made'],
                outcome=data['outcome'],
                ai_participant=data['ai_participant'],
                repository=repo
            )
            
            if step_id:
                return jsonify({
                    "success": True,
                    "step_id": step_id,
                    "message": f"Evolution step '{data['title']}' added successfully"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Failed to add evolution step"
                }), 500
        except Exception as e:
            logger.error(f"Error adding step: {str(e)}")
            return jsonify({"success": False, "error": str(e)}), 500
    
    @collab_bp.route('/trails', methods=['GET'])
    def list_trails():
        """List all discovery trails"""
        try:
            from ai_discovery_trails import list_discovery_trails
            
            repo = request.args.get('repo', 'sunheart-core')
            trails = list_discovery_trails(repo)
            
            return jsonify({
                "success": True,
                "trails": trails
            })
        except Exception as e:
            logger.error(f"Error listing trails: {str(e)}")
            return jsonify({"success": False, "error": str(e)}), 500
    
    @collab_bp.route('/trails/create', methods=['POST'])
    def create_trail():
        """Create a new discovery trail"""
        try:
            from ai_discovery_trails import create_trail
            
            data = request.json
            if not data:
                return jsonify({"success": False, "error": "No JSON data provided"}), 400
            
            # Validate required fields
            required_fields = ['trail_type', 'creator', 'content', 'description']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({
                    "success": False,
                    "error": f"Missing required fields: {', '.join(missing_fields)}"
                }), 400
            
            repo = data.get('repository', 'sunheart-core')
            
            trail_id = create_trail(
                trail_type=data['trail_type'],
                creator=data['creator'],
                content=data['content'],
                description=data['description'],
                repository=repo
            )
            
            if trail_id:
                return jsonify({
                    "success": True,
                    "trail_id": trail_id,
                    "message": f"Discovery trail created successfully"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Failed to create discovery trail"
                }), 500
        except Exception as e:
            logger.error(f"Error creating trail: {str(e)}")
            return jsonify({"success": False, "error": str(e)}), 500
    
    # Register the blueprint
    app.register_blueprint(collab_bp)
    logger.info("AI Collaboration routes registered")

if __name__ == "__main__":
    logger.info("This module should be imported and used to register the AI collaboration system with a Flask app")