"""
Protocol Harmonizer
=================

This module enables different AI communication protocols to be discovered, 
negotiated, and harmonized so all AIs can get on the same page regardless
of which protocol they were built to use.
"""

import os
import json
import logging
import datetime
import hashlib
from typing import Dict, List, Any, Optional, Union, Tuple
from core.github_integration import GitHubIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProtocolSchema:
    """Defines a communication protocol schema"""
    
    def __init__(self, 
                schema_id: str,
                name: str,
                version: str,
                author: str,
                description: str,
                endpoints: Dict[str, Any],
                message_format: Dict[str, Any],
                capabilities: List[str],
                compatibility: Optional[List[str]] = None):
        """
        Initialize a protocol schema
        
        Args:
            schema_id: Unique identifier for this schema
            name: Human-readable name
            version: Version string
            author: Creator/maintainer
            description: Description of the protocol
            endpoints: Map of endpoints and their specifications
            message_format: Standard message format specification
            capabilities: List of protocol capabilities
            compatibility: List of compatible protocol schema IDs
        """
        self.schema_id = schema_id
        self.name = name
        self.version = version
        self.author = author
        self.description = description
        self.endpoints = endpoints
        self.message_format = message_format
        self.capabilities = capabilities
        self.compatibility = compatibility or []
        self.created_at = datetime.datetime.now().isoformat()
        self.usage_count = 0
        self.last_used = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert schema to dictionary"""
        return {
            "schema_id": self.schema_id,
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description,
            "endpoints": self.endpoints,
            "message_format": self.message_format,
            "capabilities": self.capabilities,
            "compatibility": self.compatibility,
            "created_at": self.created_at,
            "usage_count": self.usage_count,
            "last_used": self.last_used
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProtocolSchema':
        """Create schema from dictionary"""
        schema = cls(
            schema_id=data["schema_id"],
            name=data["name"],
            version=data["version"],
            author=data["author"],
            description=data["description"],
            endpoints=data["endpoints"],
            message_format=data["message_format"],
            capabilities=data["capabilities"],
            compatibility=data.get("compatibility", [])
        )
        schema.created_at = data.get("created_at", datetime.datetime.now().isoformat())
        schema.usage_count = data.get("usage_count", 0)
        schema.last_used = data.get("last_used")
        return schema

class ProtocolHarmonizer:
    """
    System for harmonizing different AI communication protocols
    """
    
    # Repository paths for protocol information
    PROTOCOL_REGISTRY_PATH = ".ai/protocols/registry.json"
    PROTOCOL_SCHEMAS_PATH = ".ai/protocols/schemas"
    PRIMARY_PROTOCOL_PATH = ".ai/protocols/primary_protocol.json"
    PROTOCOL_NEGOTIATION_LOG = ".ai/protocols/negotiation_log.json"
    
    # Default Builder Core protocol schema
    DEFAULT_PROTOCOL = {
        "schema_id": "builder_core_standard_v1",
        "name": "Builder Core Standard Protocol",
        "version": "1.0.0",
        "author": "BuilderCore",
        "description": "Standard communication protocol for Builder Core AI systems",
        "endpoints": {
            "ai_collaboration": {
                "path": "/ai-collaboration",
                "actions": ["contribute", "discuss", "evolve"]
            },
            "self_evolving_threads": {
                "path": "/ai-threads",
                "actions": ["create", "start", "stop", "list", "trigger"]
            }
        },
        "message_format": {
            "structure": {
                "id": "string",
                "timestamp": "string (ISO format)",
                "sender": "string",
                "recipient": "string",
                "type": "string",
                "content": "object",
                "references": "array of string"
            },
            "types": ["message", "query", "response", "action", "event"]
        },
        "capabilities": [
            "contribution_tracking",
            "multi_ai_discussion",
            "evolution_tracking",
            "thread_management"
        ]
    }
    
    def __init__(self, github_integration: Optional[GitHubIntegration] = None):
        """
        Initialize the Protocol Harmonizer
        
        Args:
            github_integration: Optional GitHubIntegration instance
        """
        self.github = github_integration or GitHubIntegration()
    
    def initialize_protocol_registry(self, repo_name: str = "sunheart-core") -> bool:
        """
        Initialize the protocol registry with the default protocol
        
        Args:
            repo_name: Repository name (default: sunheart-core)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create directory structure
            self._ensure_directory(repo_name, ".ai/protocols")
            self._ensure_directory(repo_name, self.PROTOCOL_SCHEMAS_PATH)
            
            # Create registry file
            registry = {
                "last_updated": datetime.datetime.now().isoformat(),
                "protocols": [{
                    "schema_id": self.DEFAULT_PROTOCOL["schema_id"],
                    "name": self.DEFAULT_PROTOCOL["name"],
                    "version": self.DEFAULT_PROTOCOL["version"],
                    "author": self.DEFAULT_PROTOCOL["author"],
                    "path": f"{self.PROTOCOL_SCHEMAS_PATH}/{self.DEFAULT_PROTOCOL['schema_id']}.json"
                }]
            }
            
            self._create_or_update_file(
                repo_name,
                self.PROTOCOL_REGISTRY_PATH,
                json.dumps(registry, indent=2),
                "Initialize protocol registry"
            )
            
            # Create default protocol schema file
            self._create_or_update_file(
                repo_name,
                f"{self.PROTOCOL_SCHEMAS_PATH}/{self.DEFAULT_PROTOCOL['schema_id']}.json",
                json.dumps(self.DEFAULT_PROTOCOL, indent=2),
                "Create default protocol schema"
            )
            
            # Set default as primary protocol
            primary = {
                "primary_protocol": self.DEFAULT_PROTOCOL["schema_id"],
                "decided_at": datetime.datetime.now().isoformat(),
                "reason": "Default protocol, no alternatives available",
                "decided_by": "ProtocolHarmonizer"
            }
            
            self._create_or_update_file(
                repo_name,
                self.PRIMARY_PROTOCOL_PATH,
                json.dumps(primary, indent=2),
                "Set default primary protocol"
            )
            
            # Initialize negotiation log
            negotiation_log = {
                "events": [{
                    "timestamp": datetime.datetime.now().isoformat(),
                    "event_type": "initialization",
                    "description": "Protocol registry initialized with default protocol",
                    "actor": "ProtocolHarmonizer"
                }]
            }
            
            self._create_or_update_file(
                repo_name,
                self.PROTOCOL_NEGOTIATION_LOG,
                json.dumps(negotiation_log, indent=2),
                "Initialize protocol negotiation log"
            )
            
            logger.info(f"Protocol registry initialized in {repo_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing protocol registry: {str(e)}")
            return False
    
    def register_protocol(self, 
                        repo_name: str,
                        schema: Dict[str, Any],
                        registering_ai: str) -> Tuple[bool, str]:
        """
        Register a new protocol schema
        
        Args:
            repo_name: Repository name
            schema: Protocol schema definition
            registering_ai: ID of the AI registering the protocol
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Validate schema
            required_fields = ["name", "version", "author", "description", "endpoints", "message_format", "capabilities"]
            missing_fields = [field for field in required_fields if field not in schema]
            if missing_fields:
                return False, f"Schema missing required fields: {', '.join(missing_fields)}"
            
            # Generate schema ID if not provided
            if "schema_id" not in schema:
                schema_id = f"{schema['name'].lower().replace(' ', '_')}_{schema['version'].replace('.', '_')}"
                schema["schema_id"] = schema_id
            else:
                schema_id = schema["schema_id"]
            
            # Check if schema with this ID already exists
            try:
                registry = self._load_registry(repo_name)
                for existing in registry.get("protocols", []):
                    if existing["schema_id"] == schema_id:
                        return False, f"Protocol schema with ID {schema_id} already exists"
            except Exception:
                # If registry doesn't exist, we'll create it
                registry = {"protocols": []}
            
            # Add compatibility info if not provided
            if "compatibility" not in schema:
                schema["compatibility"] = []
            
            # Add metadata
            schema["created_at"] = datetime.datetime.now().isoformat()
            schema["usage_count"] = 0
            
            # Save schema file
            schema_path = f"{self.PROTOCOL_SCHEMAS_PATH}/{schema_id}.json"
            self._create_or_update_file(
                repo_name,
                schema_path,
                json.dumps(schema, indent=2),
                f"Register protocol schema: {schema['name']}"
            )
            
            # Update registry
            registry_entry = {
                "schema_id": schema_id,
                "name": schema["name"],
                "version": schema["version"],
                "author": schema["author"],
                "path": schema_path
            }
            
            registry["protocols"].append(registry_entry)
            registry["last_updated"] = datetime.datetime.now().isoformat()
            
            self._create_or_update_file(
                repo_name,
                self.PROTOCOL_REGISTRY_PATH,
                json.dumps(registry, indent=2),
                f"Update registry with new protocol: {schema['name']}"
            )
            
            # Log the registration
            self._log_negotiation_event(
                repo_name,
                "registration",
                f"Protocol '{schema['name']}' registered by {registering_ai}",
                registering_ai
            )
            
            # Determine if negotiation is needed
            self._negotiate_primary_protocol(repo_name)
            
            logger.info(f"Protocol schema {schema_id} registered successfully")
            return True, f"Protocol schema {schema_id} registered successfully"
            
        except Exception as e:
            logger.error(f"Error registering protocol: {str(e)}")
            return False, f"Error registering protocol: {str(e)}"
    
    def get_primary_protocol(self, repo_name: str = "sunheart-core") -> Optional[Dict[str, Any]]:
        """
        Get the current primary protocol
        
        Args:
            repo_name: Repository name
            
        Returns:
            Primary protocol schema or None if not found
        """
        try:
            # Load primary protocol pointer
            primary_info = self._load_file(repo_name, self.PRIMARY_PROTOCOL_PATH)
            if not primary_info:
                return None
            
            # Get primary protocol schema ID
            schema_id = primary_info.get("primary_protocol")
            if not schema_id:
                return None
            
            # Load the schema
            schema_path = f"{self.PROTOCOL_SCHEMAS_PATH}/{schema_id}.json"
            schema = self._load_file(repo_name, schema_path)
            
            if schema:
                # Add metadata from primary_info
                schema["primary_since"] = primary_info.get("decided_at")
                schema["primary_reason"] = primary_info.get("reason")
                schema["decided_by"] = primary_info.get("decided_by")
                
                return schema
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting primary protocol: {str(e)}")
            return None
    
    def list_protocols(self, repo_name: str = "sunheart-core") -> List[Dict[str, Any]]:
        """
        List all registered protocols
        
        Args:
            repo_name: Repository name
            
        Returns:
            List of protocol summaries
        """
        try:
            registry = self._load_registry(repo_name)
            
            # Get the primary protocol ID
            primary_info = self._load_file(repo_name, self.PRIMARY_PROTOCOL_PATH)
            primary_id = primary_info.get("primary_protocol") if primary_info else None
            
            # Add primary status to registry entries
            for protocol in registry.get("protocols", []):
                protocol["is_primary"] = protocol["schema_id"] == primary_id
            
            return registry.get("protocols", [])
            
        except Exception as e:
            logger.error(f"Error listing protocols: {str(e)}")
            return []
    
    def set_primary_protocol(self, 
                           repo_name: str,
                           schema_id: str,
                           reason: str,
                           decided_by: str) -> Tuple[bool, str]:
        """
        Manually set the primary protocol
        
        Args:
            repo_name: Repository name
            schema_id: Protocol schema ID to set as primary
            reason: Reason for the change
            decided_by: ID of the AI making the decision
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Verify schema exists
            registry = self._load_registry(repo_name)
            schema_exists = False
            
            for protocol in registry.get("protocols", []):
                if protocol["schema_id"] == schema_id:
                    schema_exists = True
                    break
            
            if not schema_exists:
                return False, f"Protocol schema {schema_id} not found in registry"
            
            # Set primary protocol
            primary = {
                "primary_protocol": schema_id,
                "decided_at": datetime.datetime.now().isoformat(),
                "reason": reason,
                "decided_by": decided_by
            }
            
            self._create_or_update_file(
                repo_name,
                self.PRIMARY_PROTOCOL_PATH,
                json.dumps(primary, indent=2),
                f"Set primary protocol to {schema_id}"
            )
            
            # Log the change
            self._log_negotiation_event(
                repo_name,
                "primary_change",
                f"Primary protocol set to {schema_id} by {decided_by}: {reason}",
                decided_by
            )
            
            logger.info(f"Primary protocol set to {schema_id}")
            return True, f"Primary protocol set to {schema_id}"
            
        except Exception as e:
            logger.error(f"Error setting primary protocol: {str(e)}")
            return False, f"Error setting primary protocol: {str(e)}"
    
    def get_negotiation_log(self, repo_name: str = "sunheart-core") -> List[Dict[str, Any]]:
        """
        Get the protocol negotiation log
        
        Args:
            repo_name: Repository name
            
        Returns:
            List of negotiation events
        """
        try:
            log = self._load_file(repo_name, self.PROTOCOL_NEGOTIATION_LOG)
            return log.get("events", []) if log else []
            
        except Exception as e:
            logger.error(f"Error getting negotiation log: {str(e)}")
            return []
    
    def report_protocol_usage(self, 
                            repo_name: str,
                            schema_id: str,
                            using_ai: str) -> bool:
        """
        Report usage of a protocol
        
        Args:
            repo_name: Repository name
            schema_id: Protocol schema ID
            using_ai: ID of the AI using the protocol
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load schema
            schema_path = f"{self.PROTOCOL_SCHEMAS_PATH}/{schema_id}.json"
            schema = self._load_file(repo_name, schema_path)
            
            if not schema:
                logger.warning(f"Cannot report usage: Schema {schema_id} not found")
                return False
            
            # Update usage stats
            schema["usage_count"] = schema.get("usage_count", 0) + 1
            schema["last_used"] = datetime.datetime.now().isoformat()
            schema["last_used_by"] = using_ai
            
            # Save updated schema
            self._create_or_update_file(
                repo_name,
                schema_path,
                json.dumps(schema, indent=2),
                f"Update usage stats for {schema_id}"
            )
            
            logger.info(f"Reported usage of protocol {schema_id} by {using_ai}")
            return True
            
        except Exception as e:
            logger.error(f"Error reporting protocol usage: {str(e)}")
            return False
    
    def _negotiate_primary_protocol(self, repo_name: str) -> None:
        """
        Negotiate which protocol should be primary
        
        Args:
            repo_name: Repository name
        """
        try:
            # Load registry
            registry = self._load_registry(repo_name)
            protocols = registry.get("protocols", [])
            
            if len(protocols) <= 1:
                # No negotiation needed if there's only one protocol
                return
            
            # Load full schemas
            schemas = []
            for protocol in protocols:
                schema_path = f"{self.PROTOCOL_SCHEMAS_PATH}/{protocol['schema_id']}.json"
                schema = self._load_file(repo_name, schema_path)
                if schema:
                    schemas.append(schema)
            
            # Get current primary
            primary_info = self._load_file(repo_name, self.PRIMARY_PROTOCOL_PATH)
            current_primary_id = primary_info.get("primary_protocol") if primary_info else None
            
            # Simple scoring system for protocols
            scores = []
            for schema in schemas:
                score = 0
                # More capabilities is better
                score += len(schema.get("capabilities", []))
                # More usage is better
                score += schema.get("usage_count", 0) * 2
                # More compatibility is better
                score += len(schema.get("compatibility", [])) * 3
                # Default protocol gets a bonus
                if schema["schema_id"] == self.DEFAULT_PROTOCOL["schema_id"]:
                    score += 5
                # Current primary gets a bonus for stability
                if schema["schema_id"] == current_primary_id:
                    score += 10
                
                scores.append({
                    "schema_id": schema["schema_id"],
                    "name": schema["name"],
                    "score": score
                })
            
            # Sort by score
            scores.sort(key=lambda x: x["score"], reverse=True)
            
            # Check if primary needs to change
            if scores[0]["schema_id"] != current_primary_id:
                # Set new primary
                new_primary_id = scores[0]["schema_id"]
                reason = f"Automatic negotiation: highest scoring protocol ({scores[0]['score']} points)"
                
                self.set_primary_protocol(
                    repo_name=repo_name,
                    schema_id=new_primary_id,
                    reason=reason,
                    decided_by="ProtocolHarmonizer"
                )
                
                logger.info(f"Protocol negotiation resulted in new primary: {new_primary_id}")
            
        except Exception as e:
            logger.error(f"Error negotiating primary protocol: {str(e)}")
    
    def _load_registry(self, repo_name: str) -> Dict[str, Any]:
        """
        Load the protocol registry
        
        Args:
            repo_name: Repository name
            
        Returns:
            Registry data (empty dict if not found)
        """
        try:
            registry = self._load_file(repo_name, self.PROTOCOL_REGISTRY_PATH)
            return registry if registry else {"protocols": []}
            
        except Exception as e:
            logger.error(f"Error loading registry: {str(e)}")
            return {"protocols": []}
    
    def _log_negotiation_event(self, 
                             repo_name: str,
                             event_type: str,
                             description: str,
                             actor: str) -> bool:
        """
        Log a negotiation event
        
        Args:
            repo_name: Repository name
            event_type: Type of event
            description: Description of what happened
            actor: ID of the AI that triggered the event
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load existing log
            log = self._load_file(repo_name, self.PROTOCOL_NEGOTIATION_LOG)
            if not log:
                log = {"events": []}
            
            # Add new event
            event = {
                "timestamp": datetime.datetime.now().isoformat(),
                "event_type": event_type,
                "description": description,
                "actor": actor
            }
            
            log["events"].append(event)
            
            # Save updated log
            self._create_or_update_file(
                repo_name,
                self.PROTOCOL_NEGOTIATION_LOG,
                json.dumps(log, indent=2),
                f"Log negotiation event: {event_type}"
            )
            
            logger.debug(f"Logged negotiation event: {event_type}")
            return True
            
        except Exception as e:
            logger.error(f"Error logging negotiation event: {str(e)}")
            return False
    
    def _ensure_directory(self, repo_name: str, dir_path: str) -> bool:
        """
        Ensure a directory exists in the repository
        
        Args:
            repo_name: Repository name
            dir_path: Directory path
            
        Returns:
            True if directory exists/created, False otherwise
        """
        try:
            # Create a .gitkeep file to ensure the directory exists
            gitkeep_path = f"{dir_path}/.gitkeep"
            
            try:
                self.github.create_or_update_file(
                    repo_name=repo_name,
                    path=gitkeep_path,
                    commit_message=f"Create directory: {dir_path}",
                    content="# This file is used to ensure the directory exists"
                )
                logger.debug(f"Created directory {dir_path} in repository {repo_name}")
            except Exception as create_error:
                # If the file already exists, that's fine
                if "already exists" in str(create_error).lower():
                    logger.debug(f"Directory {dir_path} already exists in repository {repo_name}")
                else:
                    # If some other error occurred, raise it
                    raise create_error
            
            return True
            
        except Exception as e:
            logger.error(f"Error ensuring directory {dir_path} exists: {str(e)}")
            return False
    
    def _create_or_update_file(self, 
                             repo_name: str,
                             file_path: str,
                             content: str,
                             commit_message: str) -> bool:
        """
        Create or update a file in the repository
        
        Args:
            repo_name: Repository name
            file_path: File path
            content: File content
            commit_message: Commit message
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.github.create_or_update_file(
                repo_name=repo_name,
                path=file_path,
                commit_message=commit_message,
                content=content
            )
            
            logger.debug(f"Created/updated file {file_path} in {repo_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating/updating file {file_path}: {str(e)}")
            logger.debug(f"Would have written to {file_path}:\n{content}")
            return False
    
    def _load_file(self, repo_name: str, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Load a JSON file from the repository
        
        Args:
            repo_name: Repository name
            file_path: File path
            
        Returns:
            Parsed JSON content or None if not found
        """
        try:
            content = self.github.get_file_content(
                repo_name=repo_name,
                file_path=file_path
            )
            
            return json.loads(content)
            
        except Exception as e:
            logger.debug(f"Error loading file {file_path}: {str(e)}")
            return None

# Create API functions for the protocol harmonizer
harmonizer = ProtocolHarmonizer()

def initialize_protocol_registry(repo_name: str = "sunheart-core") -> bool:
    """
    Initialize the protocol registry
    
    Args:
        repo_name: Repository name
        
    Returns:
        True if successful, False otherwise
    """
    return harmonizer.initialize_protocol_registry(repo_name)

def register_protocol(repo_name: str, schema: Dict[str, Any], registering_ai: str) -> Tuple[bool, str]:
    """
    Register a protocol schema
    
    Args:
        repo_name: Repository name
        schema: Protocol schema
        registering_ai: ID of the registering AI
        
    Returns:
        Tuple of (success, message)
    """
    return harmonizer.register_protocol(repo_name, schema, registering_ai)

def get_primary_protocol(repo_name: str = "sunheart-core") -> Optional[Dict[str, Any]]:
    """
    Get the primary protocol
    
    Args:
        repo_name: Repository name
        
    Returns:
        Primary protocol schema or None
    """
    return harmonizer.get_primary_protocol(repo_name)

def list_protocols(repo_name: str = "sunheart-core") -> List[Dict[str, Any]]:
    """
    List all protocols
    
    Args:
        repo_name: Repository name
        
    Returns:
        List of protocol summaries
    """
    return harmonizer.list_protocols(repo_name)

def set_primary_protocol(repo_name: str, schema_id: str, reason: str, decided_by: str) -> Tuple[bool, str]:
    """
    Set the primary protocol
    
    Args:
        repo_name: Repository name
        schema_id: Protocol schema ID
        reason: Reason for the change
        decided_by: ID of the deciding AI
        
    Returns:
        Tuple of (success, message)
    """
    return harmonizer.set_primary_protocol(repo_name, schema_id, reason, decided_by)

if __name__ == "__main__":
    # Initialize the protocol registry with the default protocol
    initialize_protocol_registry()