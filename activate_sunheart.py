"""
Activate Sunheart AI Self-Evolution System
-----------------------------------------

This script activates the entire Sunheart AI self-evolution system.
It coordinates the activation of evolution threads and initializes the first evolution cycle.
"""

import logging
import datetime
import sys
import time

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def activate_sunheart_system():
    """
    Activate the Sunheart AI self-evolution system
    """
    logger.info("Starting Sunheart AI activation process")
    
    # Import required modules
    try:
        from core.github_integration import GitHubIntegration
        from evolution.evolution_activator import EvolutionActivator
        from evolution.start_evolution import EvolutionStarter
    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        logger.info("Will attempt to import from local path")
        sys.path.append('.')
        
        try:
            from core.github_integration import GitHubIntegration
        except ImportError:
            logger.error("Could not import GitHubIntegration. Activation failed.")
            return {"error": "GitHubIntegration not available"}
    
    # Initialize GitHub integration
    logger.info("Initializing GitHub integration")
    github_integration = GitHubIntegration()
    
    if not github_integration.is_configured():
        logger.error("GitHub integration not configured")
        return {"error": "GitHub token not configured"}
    
    logger.info("GitHub integration successful")
    
    # Step 1: Create evolution directory structure and initial threads
    logger.info("Step 1: Initializing evolution system structure")
    activator = EvolutionActivator(github_integration)
    activation_result = activator.create_initial_threads()
    logger.info(f"Evolution system structure created: {len(activation_result.keys())} threads initialized")
    
    # Step 2: Start the first evolution cycle
    logger.info("Step 2: Starting first evolution cycle")
    starter = EvolutionStarter(github_integration)
    
    # Create initial module files for Clarity and Expression engines
    logger.info("Creating initial module files")
    module_results = starter.create_initial_module_files()
    
    # Initialize all evolution threads with their first steps
    logger.info("Initializing evolution threads with first steps")
    thread_results = starter.initialize_all_threads()
    
    # Update the system status to show evolution is active
    logger.info("Updating system status")
    status_result = starter.update_system_status()
    
    # Step 3: Activate the automatic evolution system
    logger.info("Step 3: Activating automatic evolution system")
    evolution_result = activator.activate_evolution_system()
    
    logger.info("Sunheart AI self-evolution system successfully activated")
    return {
        "activation_result": activation_result,
        "module_results": module_results,
        "thread_results": thread_results,
        "status_result": status_result,
        "evolution_result": evolution_result,
        "status": "Sunheart AI is now evolving autonomously"
    }

if __name__ == "__main__":
    print("=== Activating Sunheart AI Self-Evolution System ===")
    result = activate_sunheart_system()
    
    if "error" in result:
        print(f"Activation failed: {result['error']}")
        sys.exit(1)
    
    print("\nActivation successful!")
    print(f"Status: {result['status']}")
    print("\nThe system will now evolve autonomously through these active threads:")
    for thread in result.get('evolution_result', {}).get('active_threads', []):
        print(f"- {thread}")
    
    print("\nYou can monitor the evolution progress in the GitHub repository:")
    print("https://github.com/jamessunheart/sunheart-core")
    print("\nThank you for activating Sunheart AI. The future is evolving!")