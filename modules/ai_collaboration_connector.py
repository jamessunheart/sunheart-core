"""
Module Integration with AI Collaboration
---------------------------------------

This module connects Sunheart modules with the AI collaboration system.
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ModuleCollaborationConnector:
    """
    Connector class to integrate Sunheart Modules with AI collaboration system
    """
    
    def __init__(self, module_name: str):
        """
        Initialize the module collaboration connector
        
        Args:
            module_name: Name of the module using this connector
        """
        self.module_name = module_name
        logger.info(f"Module Collaboration Connector initialized for {module_name}")
        
    def register_module_protocol(self, protocol_schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register a module's protocol with the harmonizer
        
        Args:
            protocol_schema: The protocol schema to register
            
        Returns:
            Dict containing registration result
        """
        # Import here to avoid circular imports
        from .ai.protocols.harmonizer import register_protocol
        return register_protocol(f"module-{self.module_name}", protocol_schema, self.module_name)
        
    def contribute_module_insight(self, insight_type: str, content: str) -> Dict[str, Any]:
        """
        Record a module contribution or insight
        
        Args:
            insight_type: Type of insight (e.g., 'feature', 'improvement', 'bug')
            content: The insight content
            
        Returns:
            Dict containing the recorded contribution
        """
        # Import here to avoid circular imports
        from .ai.collaboration.hub import record_contribution
        return record_contribution(
            ai_identifier=self.module_name, 
            contribution_type=insight_type, 
            content=content,
            metadata={"module": self.module_name}
        )
        
    def register_module_capability(self, capability: str, description: str) -> Dict[str, Any]:
        """
        Register a module capability as a discovery trail
        
        Args:
            capability: Name of the capability
            description: Description of what the capability does
            
        Returns:
            Dict containing the created trail marker
        """
        # Import here to avoid circular imports
        from .ai.discovery.trails import create_trail_marker
        return create_trail_marker(
            trail_type="module_capability",
            content={
                "module": self.module_name,
                "capability": capability,
                "description": description
            },
            description=f"Module capability: {self.module_name}:{capability}"
        )
        
    def contribute_to_evolution(self, thread_id: str, improvement: str) -> Dict[str, Any]:
        """
        Contribute to an existing evolution thread
        
        Args:
            thread_id: ID of the thread to contribute to
            improvement: Description of the improvement made
            
        Returns:
            Dict containing the evolution step details
        """
        # Import here to avoid circular imports
        from .ai.evolution.threads import add_evolution_step
        return add_evolution_step(
            thread_id=thread_id,
            title=f"{self.module_name} improvement",
            description=improvement,
            goals_advanced=[],
            changes_made=[
                {
                    "type": "module",
                    "module": self.module_name,
                    "description": improvement
                }
            ],
            outcome=f"Module {self.module_name} improved: {improvement}",
            ai_participant=self.module_name
        )