"""
Sunheart AI Verification System
------------------------------

This module verifies the actual capabilities of the Sunheart AI system to prevent
hallucination of capabilities and ensure version numbers accurately reflect
the implemented functionality.
"""

import os
import logging
import json
import datetime
import requests
import importlib.util
import sys
from typing import Dict, Any, List, Optional, Set, Tuple

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("verification.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CapabilityVerifier:
    """
    Class for verifying actual capabilities of the Sunheart AI system
    """
    
    def __init__(self, github_integration=None):
        """
        Initialize the capability verifier
        
        Args:
            github_integration: Optional GitHub integration instance
        """
        self.github_integration = github_integration
        self.verified_capabilities = set()
        self.failed_capabilities = set()
        self.version_components = {
            "major": 0,
            "minor": 0,
            "patch": 0
        }
        logger.info("Capability Verifier initialized")
        
    def verify_github_repository(self) -> bool:
        """
        Verify the GitHub repository exists and is properly configured
        
        Returns:
            bool: True if verified, False otherwise
        """
        if not self.github_integration:
            logger.error("GitHub integration not available")
            return False
            
        try:
            # Check if the repository exists
            repo = self.github_integration.github.get_repo("jamessunheart/sunheart-core")
            
            # Get the README and verify it contains key features
            readme_content = repo.get_contents("README.md").decoded_content.decode()
            
            # Check for key components in the README
            required_components = [
                "Sunheart AI", 
                "self-evolving intelligence system", 
                "Protocol Harmonizer", 
                "AI Discovery Trails"
            ]
            
            for component in required_components:
                if component not in readme_content:
                    logger.warning(f"Repository README missing key component: {component}")
                    return False
            
            logger.info("GitHub repository verified")
            self.verified_capabilities.add("github_repository")
            return True
        except Exception as e:
            logger.error(f"Error verifying GitHub repository: {e}")
            self.failed_capabilities.add("github_repository")
            return False
    
    def verify_ai_collaboration_system(self) -> bool:
        """
        Verify the AI collaboration system exists and is properly structured
        
        Returns:
            bool: True if verified, False otherwise
        """
        if not self.github_integration:
            logger.error("GitHub integration not available")
            return False
            
        try:
            repo = self.github_integration.github.get_repo("jamessunheart/sunheart-core")
            
            # Verify the .ai directory structure
            required_paths = [
                ".ai/protocols/harmonizer.py",
                ".ai/evolution/threads.py",
                ".ai/discovery/trails.py",
                ".ai/collaboration/hub.py",
                ".ai/system.json"
            ]
            
            for path in required_paths:
                try:
                    content = repo.get_contents(path)
                    if not content or not content.decoded_content:
                        logger.warning(f"Required path exists but is empty: {path}")
                        return False
                except Exception as e:
                    logger.warning(f"Required path missing: {path} - {e}")
                    return False
            
            logger.info("AI collaboration system verified")
            self.verified_capabilities.add("ai_collaboration_system")
            return True
        except Exception as e:
            logger.error(f"Error verifying AI collaboration system: {e}")
            self.failed_capabilities.add("ai_collaboration_system")
            return False
    
    def verify_evolution_system(self) -> bool:
        """
        Verify the evolution system exists and is active
        
        Returns:
            bool: True if verified, False otherwise
        """
        if not self.github_integration:
            logger.error("GitHub integration not available")
            return False
            
        try:
            repo = self.github_integration.github.get_repo("jamessunheart/sunheart-core")
            
            # Check for evolution directories and files
            required_paths = [
                "evolution/evolution_activator.py",
                "evolution/start_evolution.py"
            ]
            
            for path in required_paths:
                try:
                    content = repo.get_contents(path)
                    if not content or not content.decoded_content:
                        logger.warning(f"Required evolution file exists but is empty: {path}")
                        return False
                except Exception as e:
                    logger.warning(f"Required evolution file missing: {path} - {e}")
                    return False
            
            # Check for active evolution threads
            try:
                threads_dir = repo.get_contents(".ai/evolution/threads")
                if not threads_dir or not isinstance(threads_dir, list) or len(threads_dir) < 1:
                    logger.warning("No active evolution threads found")
                    return False
                
                # Verify at least one thread has evolution steps
                valid_threads = 0
                for thread_file in threads_dir:
                    content = repo.get_contents(thread_file.path).decoded_content.decode()
                    thread_data = json.loads(content)
                    
                    if "goals" in thread_data and len(thread_data["goals"]) > 0:
                        valid_threads += 1
                
                if valid_threads == 0:
                    logger.warning("No valid evolution threads with goals found")
                    return False
                
            except Exception as e:
                logger.warning(f"Error checking evolution threads: {e}")
                return False
            
            logger.info("Evolution system verified")
            self.verified_capabilities.add("evolution_system")
            return True
        except Exception as e:
            logger.error(f"Error verifying evolution system: {e}")
            self.failed_capabilities.add("evolution_system")
            return False
    
    def verify_clarity_engine(self) -> bool:
        """
        Verify the Clarity Engine module exists and has basic functionality
        
        Returns:
            bool: True if verified, False otherwise
        """
        if not self.github_integration:
            logger.error("GitHub integration not available")
            return False
            
        try:
            repo = self.github_integration.github.get_repo("jamessunheart/sunheart-core")
            
            # Check for Clarity Engine files
            try:
                content = repo.get_contents("modules/clarity_engine/insight_capture.py")
                code = content.decoded_content.decode()
                
                # Verify key functions exist in the code
                required_functions = [
                    "capture_insight",
                    "categorize_insight"
                ]
                
                for function in required_functions:
                    if function not in code:
                        logger.warning(f"Required function missing in Clarity Engine: {function}")
                        return False
                
            except Exception as e:
                logger.warning(f"Required Clarity Engine file missing: {e}")
                return False
            
            logger.info("Clarity Engine verified")
            self.verified_capabilities.add("clarity_engine")
            return True
        except Exception as e:
            logger.error(f"Error verifying Clarity Engine: {e}")
            self.failed_capabilities.add("clarity_engine")
            return False
    
    def verify_expression_engine(self) -> bool:
        """
        Verify the Expression Engine module exists and has basic functionality
        
        Returns:
            bool: True if verified, False otherwise
        """
        if not self.github_integration:
            logger.error("GitHub integration not available")
            return False
            
        try:
            repo = self.github_integration.github.get_repo("jamessunheart/sunheart-core")
            
            # Check for Expression Engine files
            try:
                content = repo.get_contents("modules/expression_engine/generator.py")
                code = content.decoded_content.decode()
                
                # Verify key functions exist in the code
                required_functions = [
                    "generate_post",
                    "schedule_post"
                ]
                
                for function in required_functions:
                    if function not in code:
                        logger.warning(f"Required function missing in Expression Engine: {function}")
                        return False
                
            except Exception as e:
                logger.warning(f"Required Expression Engine file missing: {e}")
                return False
            
            logger.info("Expression Engine verified")
            self.verified_capabilities.add("expression_engine")
            return True
        except Exception as e:
            logger.error(f"Error verifying Expression Engine: {e}")
            self.failed_capabilities.add("expression_engine")
            return False
    
    def verify_all_capabilities(self) -> Dict[str, Any]:
        """
        Verify all capabilities of the Sunheart AI system
        
        Returns:
            Dict containing verification results
        """
        results = {}
        
        # Core verifications
        results["github_repository"] = self.verify_github_repository()
        results["ai_collaboration_system"] = self.verify_ai_collaboration_system()
        results["evolution_system"] = self.verify_evolution_system()
        
        # Module verifications
        results["clarity_engine"] = self.verify_clarity_engine()
        results["expression_engine"] = self.verify_expression_engine()
        
        # Calculate version based on verified capabilities
        self._calculate_version()
        
        # Summarize results
        capabilities_summary = {
            "verified_capabilities": list(self.verified_capabilities),
            "failed_capabilities": list(self.failed_capabilities),
            "verification_time": datetime.datetime.now().isoformat(),
            "version": f"{self.version_components['major']}.{self.version_components['minor']}.{self.version_components['patch']}",
            "results": results
        }
        
        logger.info(f"Verification complete: {len(self.verified_capabilities)} capabilities verified, "
                   f"{len(self.failed_capabilities)} failed")
        
        return capabilities_summary
    
    def _calculate_version(self) -> None:
        """
        Calculate the appropriate version number based on verified capabilities
        
        Core components increase major version:
        - GitHub repository
        - AI collaboration system
        - Evolution system
        
        Modules increase minor version:
        - Clarity Engine
        - Expression Engine
        - Commerce Layer (future)
        
        Improvements to existing components increase patch version.
        """
        # Major version components
        major_components = {
            "github_repository",
            "ai_collaboration_system",
            "evolution_system"
        }
        
        # Minor version components
        minor_components = {
            "clarity_engine",
            "expression_engine"
        }
        
        # Calculate major version (0-3)
        major_count = len(major_components.intersection(self.verified_capabilities))
        self.version_components["major"] = major_count
        
        # Calculate minor version (0-n)
        minor_count = len(minor_components.intersection(self.verified_capabilities))
        self.version_components["minor"] = minor_count
        
        # Patch version would be determined by comparing to previous verification results
        # For initial implementation, set to 0
        self.version_components["patch"] = 0
    
    def update_version_in_repository(self) -> bool:
        """
        Update the version number in the repository based on verified capabilities
        
        Returns:
            bool: True if updated, False otherwise
        """
        if not self.github_integration:
            logger.error("GitHub integration not available")
            return False
            
        try:
            repo = self.github_integration.github.get_repo("jamessunheart/sunheart-core")
            
            # Format version string
            version = f"{self.version_components['major']}.{self.version_components['minor']}.{self.version_components['patch']}"
            
            # Create or update version file
            version_content = {
                "version": version,
                "verified_capabilities": list(self.verified_capabilities),
                "verification_time": datetime.datetime.now().isoformat()
            }
            
            try:
                # Try to get existing file
                content = repo.get_contents("VERSION.json")
                repo.update_file(
                    "VERSION.json",
                    f"Update version to {version} based on capability verification",
                    json.dumps(version_content, indent=2),
                    content.sha
                )
                logger.info(f"Updated version to {version}")
            except Exception:
                # File doesn't exist, create it
                repo.create_file(
                    "VERSION.json",
                    f"Create initial version file: {version}",
                    json.dumps(version_content, indent=2)
                )
                logger.info(f"Created initial version file: {version}")
            
            # Also update README badges if possible
            try:
                readme = repo.get_contents("README.md")
                readme_content = readme.decoded_content.decode()
                
                # Look for version badge
                if "![Version:" in readme_content:
                    readme_content = readme_content.replace(
                        f"![Version: {self.version_components['major']}.{self.version_components['minor']}.{self.version_components['patch']-1}]",
                        f"![Version: {version}]"
                    )
                    
                    # Update README
                    repo.update_file(
                        "README.md",
                        f"Update version badge to {version}",
                        readme_content,
                        readme.sha
                    )
                    logger.info("Updated version badge in README")
            except Exception as e:
                logger.warning(f"Could not update README version badge: {e}")
            
            return True
        except Exception as e:
            logger.error(f"Error updating version in repository: {e}")
            return False

def run_verification():
    """
    Run the capability verification process and update version information
    """
    from core.github_integration import GitHubIntegration
    
    # Initialize GitHub integration
    github_integration = GitHubIntegration()
    
    if not github_integration.is_configured():
        logger.error("GitHub integration not configured")
        return {"error": "GitHub integration not configured"}
    
    # Initialize and run verification
    verifier = CapabilityVerifier(github_integration)
    results = verifier.verify_all_capabilities()
    
    # Update version in repository
    verifier.update_version_in_repository()
    
    # Log results
    with open("verification_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Verification results saved to verification_results.json")
    
    return results

if __name__ == "__main__":
    print("=== Running Sunheart AI Capability Verification ===")
    results = run_verification()
    
    print(f"\nVerification complete!")
    print(f"Version: {results.get('version', 'Unknown')}")
    print(f"Verified capabilities: {len(results.get('verified_capabilities', []))}")
    print(f"Failed capabilities: {len(results.get('failed_capabilities', []))}")
    
    print("\nDetailed results:")
    for capability, result in results.get("results", {}).items():
        status = "✅" if result else "❌"
        print(f"{status} {capability}")
    
    print("\nSee verification_results.json for complete details.")