"""
Core Module Integration with AI Collaboration
--------------------------------------------

This module connects the core execution engine with the AI collaboration system.
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class AICollaborationConnector:
    """
    Connector class to integrate Sunheart Core with AI collaboration system
    """
    
    def __init__(self):
        """Initialize the AI collaboration connector"""
        logger.info("AI Collaboration Connector initialized")
        
    def register_core_protocol(self) -> Dict[str, Any]:
        """
        Register the core execution protocol with the harmonizer
        
        Returns:
            Dict containing registration result
        """
        protocol_schema = {
            "name": "Sunheart Core Execution Protocol",
            "version": "1.0.0",
            "author": "sunheart-core",
            "description": "Protocol for core execution engine communication",
            "endpoints": {
                "execute": {
                    "path": "/api/core/execute",
                    "method": "POST",
                    "params": {
                        "instruction": "string",
                        "context": "object",
                        "options": "object"
                    }
                },
                "status": {
                    "path": "/api/core/status",
                    "method": "GET"
                }
            },
            "message_format": {
                "sender": "string",
                "receiver": "string",
                "message_type": "string",
                "content": "any",
                "timestamp": "string"
            }
        }
        
        # Import here to avoid circular imports
        from .ai.protocols.harmonizer import register_protocol
        return register_protocol("sunheart-core", protocol_schema, "core-execution-engine")
        
    def track_system_evolution(self, title: str, description: str, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Record an evolution step in the system
        
        Args:
            title: Title of the evolution step
            description: Detailed description of the evolution
            changes: List of changes made in this evolution step
            
        Returns:
            Dict containing the recorded evolution step
        """
        # Import here to avoid circular imports
        from .ai.evolution.threads import add_evolution_step
        return add_evolution_step(
            thread_id="system_evolution",
            title=title,
            description=description,
            goals_advanced=["system_improvement"],
            changes_made=changes,
            outcome=f"System evolution step: {title}",
            ai_participant="core-execution-engine"
        )
        
    def publish_capability(self, capability_name: str, endpoint: str, description: str) -> Dict[str, Any]:
        """
        Publish a system capability as a discovery trail
        
        Args:
            capability_name: Name of the capability
            endpoint: Endpoint or path to access the capability
            description: Description of what the capability does
            
        Returns:
            Dict containing the created trail marker
        """
        # Import here to avoid circular imports
        from .ai.discovery.trails import create_trail_marker
        return create_trail_marker(
            trail_type="system_capability",
            content={
                "capability": capability_name,
                "endpoint": endpoint,
                "description": description
            },
            description=f"System capability: {capability_name}"
        )
        
    def collaborate_on_improvement(self, topic: str, initial_message: str) -> Dict[str, Any]:
        """
        Start a collaboration thread on system improvement
        
        Args:
            topic: Topic of the collaboration
            initial_message: Initial message to start the collaboration
            
        Returns:
            Dict containing the created discussion
        """
        # Import here to avoid circular imports
        from .ai.collaboration.hub import start_discussion
        return start_discussion(
            ai_identifier="core-execution-engine",
            topic=topic,
            initial_message=initial_message,
            tags=["improvement", "core", "collaboration"]
        )