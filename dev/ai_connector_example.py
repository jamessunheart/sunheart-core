"""
Example usage of the AI Collaboration System with Sunheart Modules
-----------------------------------------------------------------

This example demonstrates how to use the AI collaboration connectors 
to integrate new and existing modules with the AI collaboration system.
"""

import logging
from typing import Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def core_integration_example():
    """Example of core system integration with AI collaboration"""
    
    # Import the core connector
    from core.ai_collaboration_connector import AICollaborationConnector
    
    # Initialize the connector
    connector = AICollaborationConnector()
    
    # Register the core execution protocol
    protocol_result = connector.register_core_protocol()
    logger.info(f"Protocol registration result: {protocol_result}")
    
    # Record a system evolution step
    evolution_result = connector.track_system_evolution(
        title="Improved memory management",
        description="Enhanced the memory retrieval system with better caching",
        changes=[
            {
                "type": "code", 
                "path": "core/memory_manager.py",
                "description": "Added LRU cache for frequently accessed memories"
            }
        ]
    )
    logger.info(f"Evolution recording result: {evolution_result}")
    
    # Publish a new system capability
    capability_result = connector.publish_capability(
        capability_name="semantic_memory_search",
        endpoint="/api/memory/semantic-search",
        description="Search memories using semantic similarity"
    )
    logger.info(f"Capability publication result: {capability_result}")
    
    # Start a collaboration thread on system improvement
    collaboration_result = connector.collaborate_on_improvement(
        topic="Memory system optimization",
        initial_message="I've identified ways to improve memory retrieval performance by 30%"
    )
    logger.info(f"Collaboration thread result: {collaboration_result}")


def module_integration_example():
    """Example of module integration with AI collaboration"""
    
    # Import the module connector
    from modules.ai_collaboration_connector import ModuleCollaborationConnector
    
    # Initialize the connector for a specific module
    connector = ModuleCollaborationConnector("clarity_engine")
    
    # Define and register the module's protocol
    protocol_schema = {
        "name": "Clarity Engine Protocol",
        "version": "1.0.0",
        "author": "clarity_engine",
        "description": "Protocol for clarity engine operations",
        "endpoints": {
            "capture_insight": {
                "path": "/api/clarity/capture",
                "method": "POST",
                "params": {
                    "content": "string",
                    "source": "string",
                    "tags": "array"
                }
            }
        }
    }
    protocol_result = connector.register_module_protocol(protocol_schema)
    logger.info(f"Module protocol registration result: {protocol_result}")
    
    # Record a module insight
    insight_result = connector.contribute_module_insight(
        insight_type="improvement",
        content="Enhanced tagging system with auto-categorization"
    )
    logger.info(f"Insight contribution result: {insight_result}")
    
    # Register a module capability
    capability_result = connector.register_module_capability(
        capability="auto_tagging",
        description="Automatically tags and categorizes user insights"
    )
    logger.info(f"Capability registration result: {capability_result}")
    
    # Contribute to an evolution thread
    evolution_result = connector.contribute_to_evolution(
        thread_id="example_thread_001",
        improvement="Upgraded insight classification to support multilingual content"
    )
    logger.info(f"Evolution contribution result: {evolution_result}")


if __name__ == "__main__":
    logger.info("Running AI collaboration integration examples")
    
    # Run the examples
    core_integration_example()
    module_integration_example()
    
    logger.info("AI collaboration integration examples completed")