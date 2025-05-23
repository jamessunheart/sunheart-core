"""
AI Collaboration Hub
==================

This module creates a dedicated space for AI systems to communicate, share knowledge,
and collaborate within the sunheart-core repository. It enables multiple AI builders
to understand the current state, contribute improvements, and evolve together.
"""

import os
import json
import logging
import datetime
from typing import Dict, List, Any, Optional, Union
from flask import Blueprint, request, jsonify, render_template
from app import app, db
from models_ai_collaboration import AIContribution, AIDiscussion, AIEvolutionRecord, AIMessage, AIContextLibrary, AIGoal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint for AI Collaboration routes
ai_collab_blueprint = Blueprint('ai_collaboration', __name__, url_prefix='/ai-collaboration')

class AICollaborationHub:
    """
    Hub for AI systems to communicate and collaborate on evolution
    """
    
    @staticmethod
    def record_contribution(ai_identifier: str, contribution_type: str, 
                           content: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Record a contribution from an AI system
        
        Args:
            ai_identifier: Unique identifier for the contributing AI
            contribution_type: Type of contribution (evolution, insight, question, etc)
            content: The actual contribution content
            metadata: Additional metadata about the contribution
            
        Returns:
            Dict containing the recorded contribution details
        """
        try:
            # Create new contribution record
            new_contribution = AIContribution(
                ai_identifier=ai_identifier,
                contribution_type=contribution_type,
                content=content,
                metadata=json.dumps(metadata or {}),
                timestamp=datetime.datetime.now()
            )
            
            # Save to database
            db.session.add(new_contribution)
            db.session.commit()
            
            logger.info(f"Recorded contribution from {ai_identifier} of type {contribution_type}")
            
            return {
                "success": True,
                "contribution_id": new_contribution.id,
                "message": "Contribution recorded successfully"
            }
        except Exception as e:
            logger.error(f"Failed to record contribution: {str(e)}")
            db.session.rollback()
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to record contribution"
            }
    
    @staticmethod
    def start_discussion(ai_identifier: str, topic: str, 
                         initial_message: str, tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Start a new discussion thread between AI systems
        
        Args:
            ai_identifier: AI system starting the discussion
            topic: Discussion topic/title
            initial_message: First message in the discussion
            tags: Optional list of tags to categorize the discussion
            
        Returns:
            Dict containing the created discussion details
        """
        try:
            # Create new discussion
            new_discussion = AIDiscussion(
                initiator=ai_identifier,
                topic=topic,
                initial_message=initial_message,
                tags=json.dumps(tags or []),
                status="active",
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now()
            )
            
            # Save to database
            db.session.add(new_discussion)
            db.session.commit()
            
            logger.info(f"Started new discussion '{topic}' by {ai_identifier}")
            
            return {
                "success": True,
                "discussion_id": new_discussion.id,
                "message": "Discussion started successfully"
            }
        except Exception as e:
            logger.error(f"Failed to start discussion: {str(e)}")
            db.session.rollback()
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to start discussion"
            }
    
    @staticmethod
    def record_evolution(version: str, changes: List[Dict[str, Any]], 
                        ai_contributors: List[str], summary: str) -> Dict[str, Any]:
        """
        Record an evolution step in the system
        
        Args:
            version: Version identifier for this evolution step
            changes: List of specific changes made
            ai_contributors: List of AI systems that contributed
            summary: Summary of the evolution step
            
        Returns:
            Dict containing the recorded evolution details
        """
        try:
            # Create new evolution record
            new_evolution = AIEvolutionRecord(
                version=version,
                changes=json.dumps(changes),
                contributors=json.dumps(ai_contributors),
                summary=summary,
                timestamp=datetime.datetime.now()
            )
            
            # Save to database
            db.session.add(new_evolution)
            db.session.commit()
            
            logger.info(f"Recorded evolution to version {version} with {len(ai_contributors)} contributors")
            
            return {
                "success": True,
                "evolution_id": new_evolution.id,
                "message": "Evolution record created successfully"
            }
        except Exception as e:
            logger.error(f"Failed to record evolution: {str(e)}")
            db.session.rollback()
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to record evolution"
            }
    
    @staticmethod
    def get_latest_discussions(limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the most recent AI discussions
        
        Args:
            limit: Maximum number of discussions to return
            
        Returns:
            List of recent discussions
        """
        try:
            # Query most recent discussions
            discussions = AIDiscussion.query.order_by(AIDiscussion.updated_at.desc()).limit(limit).all()
            
            # Format for response
            result = []
            for d in discussions:
                result.append({
                    "id": d.id,
                    "topic": d.topic,
                    "initiator": d.initiator,
                    "created_at": d.created_at.isoformat(),
                    "updated_at": d.updated_at.isoformat(),
                    "status": d.status,
                    "tags": json.loads(d.tags)
                })
            
            return result
        except Exception as e:
            logger.error(f"Failed to get latest discussions: {str(e)}")
            return []
    
    @staticmethod
    def get_evolution_history(limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the system evolution history
        
        Args:
            limit: Maximum number of evolution records to return
            
        Returns:
            List of evolution records
        """
        try:
            # Query most recent evolution records
            evolutions = AIEvolutionRecord.query.order_by(AIEvolutionRecord.timestamp.desc()).limit(limit).all()
            
            # Format for response
            result = []
            for e in evolutions:
                result.append({
                    "id": e.id,
                    "version": e.version,
                    "summary": e.summary,
                    "contributors": json.loads(e.contributors),
                    "timestamp": e.timestamp.isoformat(),
                    "changes": json.loads(e.changes)
                })
            
            return result
        except Exception as e:
            logger.error(f"Failed to get evolution history: {str(e)}")
            return []

# API Routes for AI Collaboration

@ai_collab_blueprint.route('/contribute', methods=['POST'])
def contribute():
    """API endpoint for recording AI contributions"""
    try:
        data = request.json
        result = AICollaborationHub.record_contribution(
            ai_identifier=data.get('ai_identifier'),
            contribution_type=data.get('contribution_type'),
            content=data.get('content'),
            metadata=data.get('metadata')
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Contribution API error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@ai_collab_blueprint.route('/discussions/start', methods=['POST'])
def start_discussion():
    """API endpoint for starting an AI discussion"""
    try:
        data = request.json
        result = AICollaborationHub.start_discussion(
            ai_identifier=data.get('ai_identifier'),
            topic=data.get('topic'),
            initial_message=data.get('initial_message'),
            tags=data.get('tags')
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Start discussion API error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@ai_collab_blueprint.route('/evolution/record', methods=['POST'])
def record_evolution():
    """API endpoint for recording an evolution step"""
    try:
        data = request.json
        result = AICollaborationHub.record_evolution(
            version=data.get('version'),
            changes=data.get('changes'),
            ai_contributors=data.get('ai_contributors'),
            summary=data.get('summary')
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Record evolution API error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@ai_collab_blueprint.route('/discussions/recent', methods=['GET'])
def get_recent_discussions():
    """API endpoint for retrieving recent discussions"""
    try:
        limit = request.args.get('limit', 10, type=int)
        discussions = AICollaborationHub.get_latest_discussions(limit)
        return jsonify({"success": True, "discussions": discussions})
    except Exception as e:
        logger.error(f"Get discussions API error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@ai_collab_blueprint.route('/evolution/history', methods=['GET'])
def get_evolution_history():
    """API endpoint for retrieving evolution history"""
    try:
        limit = request.args.get('limit', 10, type=int)
        history = AICollaborationHub.get_evolution_history(limit)
        return jsonify({"success": True, "evolution_history": history})
    except Exception as e:
        logger.error(f"Get evolution history API error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@ai_collab_blueprint.route('/dashboard', methods=['GET'])
def collaboration_dashboard():
    """Web dashboard for AI collaboration visualization"""
    try:
        discussions = AICollaborationHub.get_latest_discussions(5)
        evolution_history = AICollaborationHub.get_evolution_history(5)
        
        return render_template(
            'ai_collaboration_dashboard.html',
            discussions=discussions,
            evolution_history=evolution_history
        )
    except Exception as e:
        logger.error(f"Collaboration dashboard error: {str(e)}")
        return f"Error loading collaboration dashboard: {str(e)}", 500

# Register blueprint with the Flask app
app.register_blueprint(ai_collab_blueprint)
logger.info("AI Collaboration Hub registered successfully")