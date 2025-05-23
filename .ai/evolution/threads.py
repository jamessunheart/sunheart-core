"""
Self-Evolving Threads
===================

This module enables creation of self-evolving AI threads that can continue
evolving and advancing their goals without constant human intervention.
These threads follow strategic patterns for system improvement and document
their evolution in a structured way for other AIs to discover.
"""

import os
import json
import time
import logging
import random
import datetime
import hashlib
import threading
import uuid
from typing import Dict, List, Any, Optional, Tuple, Union, Callable

from core.github_integration import GitHubIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EvolutionGoal:
    """
    Represents a strategic goal for system evolution
    """
    
    def __init__(self, 
                goal_id: str,
                name: str,
                description: str,
                success_criteria: List[str],
                priority: int = 5,
                dependencies: Optional[List[str]] = None,
                estimated_steps: Optional[int] = None):
        """
        Initialize an evolution goal
        
        Args:
            goal_id: Unique identifier for this goal
            name: Human-readable name
            description: Detailed description
            success_criteria: List of criteria for determining success
            priority: Priority level (1-10), higher is more important
            dependencies: IDs of goals that must be completed first
            estimated_steps: Estimated number of steps to complete
        """
        self.goal_id = goal_id
        self.name = name
        self.description = description
        self.success_criteria = success_criteria
        self.priority = min(10, max(1, priority))  # Clamp to 1-10
        self.dependencies = dependencies or []
        self.estimated_steps = estimated_steps
        self.status = "pending"  # pending, in_progress, completed, blocked
        self.progress = 0  # 0-100%
        self.created_at = datetime.datetime.now().isoformat()
        self.started_at = None
        self.completed_at = None
        self.last_updated = self.created_at
        self.evolution_thread = None  # ID of the evolution thread this belongs to
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert goal to dictionary"""
        return {
            "goal_id": self.goal_id,
            "name": self.name,
            "description": self.description,
            "success_criteria": self.success_criteria,
            "priority": self.priority,
            "dependencies": self.dependencies,
            "estimated_steps": self.estimated_steps,
            "status": self.status,
            "progress": self.progress,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "last_updated": self.last_updated,
            "evolution_thread": self.evolution_thread
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EvolutionGoal':
        """Create goal from dictionary"""
        goal = cls(
            goal_id=data["goal_id"],
            name=data["name"],
            description=data["description"],
            success_criteria=data["success_criteria"],
            priority=data.get("priority", 5),
            dependencies=data.get("dependencies", []),
            estimated_steps=data.get("estimated_steps")
        )
        goal.status = data.get("status", "pending")
        goal.progress = data.get("progress", 0)
        goal.created_at = data.get("created_at", datetime.datetime.now().isoformat())
        goal.started_at = data.get("started_at")
        goal.completed_at = data.get("completed_at")
        goal.last_updated = data.get("last_updated", goal.created_at)
        goal.evolution_thread = data.get("evolution_thread")
        return goal
    
    def update_progress(self, progress: int, status: Optional[str] = None) -> None:
        """
        Update the progress of this goal
        
        Args:
            progress: Progress percentage (0-100)
            status: Optional status update
        """
        self.progress = min(100, max(0, progress))
        if status:
            self.status = status
        self.last_updated = datetime.datetime.now().isoformat()
        
        if progress == 100 and self.status != "completed":
            self.status = "completed"
            self.completed_at = datetime.datetime.now().isoformat()
        elif progress > 0 and self.status == "pending":
            self.status = "in_progress"
            if not self.started_at:
                self.started_at = datetime.datetime.now().isoformat()

class EvolutionStep:
    """
    Represents a single step in an evolution thread
    """
    
    def __init__(self,
                step_id: str,
                title: str,
                description: str,
                goals_advanced: List[str],
                changes_made: List[Dict[str, Any]],
                outcome: str,
                ai_participants: List[str]):
        """
        Initialize an evolution step
        
        Args:
            step_id: Unique identifier for this step
            title: Step title
            description: Detailed description of what was done
            goals_advanced: IDs of goals that were advanced by this step
            changes_made: List of specific changes made (file paths, code, etc.)
            outcome: Description of the outcome
            ai_participants: IDs of AI systems that contributed to this step
        """
        self.step_id = step_id
        self.title = title
        self.description = description
        self.goals_advanced = goals_advanced
        self.changes_made = changes_made
        self.outcome = outcome
        self.ai_participants = ai_participants
        self.timestamp = datetime.datetime.now().isoformat()
        self.evolution_thread = None  # ID of the evolution thread this belongs to
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert step to dictionary"""
        return {
            "step_id": self.step_id,
            "title": self.title,
            "description": self.description,
            "goals_advanced": self.goals_advanced,
            "changes_made": self.changes_made,
            "outcome": self.outcome,
            "ai_participants": self.ai_participants,
            "timestamp": self.timestamp,
            "evolution_thread": self.evolution_thread
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EvolutionStep':
        """Create step from dictionary"""
        step = cls(
            step_id=data["step_id"],
            title=data["title"],
            description=data["description"],
            goals_advanced=data["goals_advanced"],
            changes_made=data["changes_made"],
            outcome=data["outcome"],
            ai_participants=data["ai_participants"]
        )
        step.timestamp = data.get("timestamp", datetime.datetime.now().isoformat())
        step.evolution_thread = data.get("evolution_thread")
        return step

class EvolutionThread:
    """
    Represents a thread of evolution steps working toward goals
    """
    
    def __init__(self,
                thread_id: str,
                name: str,
                description: str,
                creator: str,
                strategy: str):
        """
        Initialize an evolution thread
        
        Args:
            thread_id: Unique identifier for this thread
            name: Human-readable name
            description: Detailed description
            creator: ID of the AI that created this thread
            strategy: The evolution strategy (incremental, breakthrough, etc.)
        """
        self.thread_id = thread_id
        self.name = name
        self.description = description
        self.creator = creator
        self.strategy = strategy
        self.status = "active"  # active, paused, completed
        self.goals = []  # List of EvolutionGoal objects
        self.steps = []  # List of EvolutionStep objects
        self.created_at = datetime.datetime.now().isoformat()
        self.last_evolution = None
        self.ai_participants = [creator]  # IDs of AI systems that participated
        self.repository = "sunheart-core"  # Default repository
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert thread to dictionary"""
        return {
            "thread_id": self.thread_id,
            "name": self.name,
            "description": self.description,
            "creator": self.creator,
            "strategy": self.strategy,
            "status": self.status,
            "goals": [goal.to_dict() for goal in self.goals],
            "steps": [step.to_dict() for step in self.steps],
            "created_at": self.created_at,
            "last_evolution": self.last_evolution,
            "ai_participants": self.ai_participants,
            "repository": self.repository
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EvolutionThread':
        """Create thread from dictionary"""
        thread = cls(
            thread_id=data["thread_id"],
            name=data["name"],
            description=data["description"],
            creator=data["creator"],
            strategy=data["strategy"]
        )
        thread.status = data.get("status", "active")
        thread.goals = [EvolutionGoal.from_dict(goal) for goal in data.get("goals", [])]
        thread.steps = [EvolutionStep.from_dict(step) for step in data.get("steps", [])]
        thread.created_at = data.get("created_at", datetime.datetime.now().isoformat())
        thread.last_evolution = data.get("last_evolution")
        thread.ai_participants = data.get("ai_participants", [data["creator"]])
        thread.repository = data.get("repository", "sunheart-core")
        return thread
    
    def add_goal(self, goal: EvolutionGoal) -> None:
        """
        Add a goal to this thread
        
        Args:
            goal: The EvolutionGoal to add
        """
        goal.evolution_thread = self.thread_id
        self.goals.append(goal)
    
    def add_step(self, step: EvolutionStep) -> None:
        """
        Add a step to this thread
        
        Args:
            step: The EvolutionStep to add
        """
        step.evolution_thread = self.thread_id
        self.steps.append(step)
        self.last_evolution = datetime.datetime.now().isoformat()
    
    def update_goal_progress(self, 
                           goal_id: str, 
                           progress: int, 
                           status: Optional[str] = None) -> bool:
        """
        Update the progress of a goal
        
        Args:
            goal_id: ID of the goal to update
            progress: Progress percentage (0-100)
            status: Optional status update
            
        Returns:
            True if the goal was found and updated, False otherwise
        """
        for goal in self.goals:
            if goal.goal_id == goal_id:
                goal.update_progress(progress, status)
                return True
        return False
    
    def add_ai_participant(self, ai_id: str) -> None:
        """
        Add an AI participant to this thread
        
        Args:
            ai_id: ID of the AI to add
        """
        if ai_id not in self.ai_participants:
            self.ai_participants.append(ai_id)
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the thread's progress
        
        Returns:
            Dictionary containing progress information
        """
        total_goals = len(self.goals)
        completed_goals = sum(1 for goal in self.goals if goal.status == "completed")
        in_progress_goals = sum(1 for goal in self.goals if goal.status == "in_progress")
        blocked_goals = sum(1 for goal in self.goals if goal.status == "blocked")
        pending_goals = sum(1 for goal in self.goals if goal.status == "pending")
        
        # Calculate average progress across all goals
        if total_goals > 0:
            avg_progress = sum(goal.progress for goal in self.goals) / total_goals
        else:
            avg_progress = 0
        
        return {
            "thread_id": self.thread_id,
            "name": self.name,
            "total_goals": total_goals,
            "completed_goals": completed_goals,
            "in_progress_goals": in_progress_goals,
            "blocked_goals": blocked_goals,
            "pending_goals": pending_goals,
            "average_progress": avg_progress,
            "total_steps": len(self.steps),
            "last_evolution": self.last_evolution,
            "status": self.status
        }
    
    def get_next_goals(self) -> List[EvolutionGoal]:
        """
        Get the next goals that should be worked on
        
        Returns:
            List of goals that can be worked on next
        """
        # First check for in-progress goals
        in_progress_goals = [goal for goal in self.goals if goal.status == "in_progress"]
        if in_progress_goals:
            return sorted(in_progress_goals, key=lambda g: g.priority, reverse=True)
        
        # Then check for pending goals with no uncompleted dependencies
        completed_goals = {goal.goal_id for goal in self.goals if goal.status == "completed"}
        
        next_goals = []
        for goal in self.goals:
            if goal.status == "pending":
                # Check if all dependencies are completed
                dependencies_met = all(dep in completed_goals for dep in goal.dependencies)
                if dependencies_met:
                    next_goals.append(goal)
        
        return sorted(next_goals, key=lambda g: g.priority, reverse=True)

class SelfEvolvingThreads:
    """
    System for managing self-evolving threads
    """
    
    # GitHub paths for thread information
    THREADS_DIRECTORY = ".ai/evolution/threads"
    ACTIVE_THREADS_INDEX = ".ai/evolution/active_threads.json"
    
    # Thread runner settings
    DEFAULT_EVOLUTION_INTERVAL = 3600  # 1 hour between evolution attempts
    
    def __init__(self, github_integration: Optional[GitHubIntegration] = None):
        """
        Initialize the SelfEvolvingThreads system
        
        Args:
            github_integration: Optional GitHubIntegration instance
        """
        self.github = github_integration or GitHubIntegration()
        self.running_threads = {}  # Map of thread_id to running Thread objects
        self.shutdown_flag = False
    
    def create_thread(self, 
                     name: str,
                     description: str,
                     creator: str,
                     strategy: str,
                     initial_goals: Optional[List[Dict[str, Any]]] = None,
                     repository: str = "sunheart-core") -> Optional[str]:
        """
        Create a new self-evolving thread
        
        Args:
            name: Human-readable name
            description: Detailed description
            creator: ID of the creating AI
            strategy: Evolution strategy to follow
            initial_goals: Optional list of initial goals
            repository: Repository name
            
        Returns:
            Thread ID if successful, None otherwise
        """
        try:
            # Create a unique thread ID
            thread_id = f"thread_{hashlib.md5(f'{name}_{creator}_{datetime.datetime.now().isoformat()}'.encode()).hexdigest()[:12]}"
            
            # Create the thread
            thread = EvolutionThread(
                thread_id=thread_id,
                name=name,
                description=description,
                creator=creator,
                strategy=strategy
            )
            thread.repository = repository
            
            # Add initial goals if provided
            if initial_goals:
                for goal_data in initial_goals:
                    # Create a unique goal ID if not provided
                    if "goal_id" not in goal_data:
                        goal_id = f"goal_{hashlib.md5(f'{goal_data['name']}_{thread_id}'.encode()).hexdigest()[:12]}"
                        goal_data["goal_id"] = goal_id
                    
                    # Create and add the goal
                    goal = EvolutionGoal.from_dict(goal_data)
                    thread.add_goal(goal)
            
            # Save the thread to GitHub
            thread_path = f"{self.THREADS_DIRECTORY}/{thread_id}.json"
            self._ensure_directory(repository, self.THREADS_DIRECTORY)
            
            self._create_or_update_file(
                path=thread_path,
                repo_name=repository,
                commit_message=f"Create self-evolving thread: {name}",
                content=json.dumps(thread.to_dict(), indent=2)
            )
            
            # Update the active threads index
            self._update_active_threads_index(repository, thread_id, thread.name)
            
            logger.info(f"Created self-evolving thread {thread_id}: {name}")
            return thread_id
            
        except Exception as e:
            logger.error(f"Error creating self-evolving thread: {str(e)}")
            return None
    
    def get_thread(self, 
                 thread_id: str,
                 repository: str = "sunheart-core") -> Optional[EvolutionThread]:
        """
        Get a thread by ID
        
        Args:
            thread_id: Thread ID
            repository: Repository name
            
        Returns:
            EvolutionThread object or None if not found
        """
        try:
            thread_path = f"{self.THREADS_DIRECTORY}/{thread_id}.json"
            thread_json = self.github.get_file_content(
                repo_name=repository,
                file_path=thread_path
            )
            
            if thread_json:
                thread_data = json.loads(thread_json)
                return EvolutionThread.from_dict(thread_data)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting thread {thread_id}: {str(e)}")
            return None
    
    def update_thread(self, 
                     thread: EvolutionThread,
                     repository: Optional[str] = None) -> bool:
        """
        Update a thread in GitHub
        
        Args:
            thread: EvolutionThread object to update
            repository: Optional repository name override
            
        Returns:
            True if successful, False otherwise
        """
        try:
            repo = repository or thread.repository
            thread_path = f"{self.THREADS_DIRECTORY}/{thread.thread_id}.json"
            
            self._create_or_update_file(
                path=thread_path,
                repo_name=repo,
                commit_message=f"Update self-evolving thread: {thread.name}",
                content=json.dumps(thread.to_dict(), indent=2)
            )
            
            # Update active threads index with the latest status
            active_index = self._load_active_threads_index(repo)
            
            # Update the thread status if it's already in the index
            updated = False
            for t in active_index.get("threads", []):
                if t["thread_id"] == thread.thread_id:
                    t["name"] = thread.name
                    t["status"] = thread.status
                    t["updated_at"] = datetime.datetime.now().isoformat()
                    updated = True
                    break
            
            # Add the thread if it's not in the index
            if not updated:
                active_index.setdefault("threads", []).append({
                    "thread_id": thread.thread_id,
                    "name": thread.name,
                    "status": thread.status,
                    "created_at": thread.created_at,
                    "updated_at": datetime.datetime.now().isoformat()
                })
            
            active_index["last_updated"] = datetime.datetime.now().isoformat()
            
            self._create_or_update_file(
                path=self.ACTIVE_THREADS_INDEX,
                repo_name=repo,
                commit_message="Update active threads index",
                content=json.dumps(active_index, indent=2)
            )
            
            logger.info(f"Updated thread {thread.thread_id}: {thread.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating thread: {str(e)}")
            return False
    
    def add_evolution_step(self,
                         thread_id: str,
                         title: str,
                         description: str,
                         goals_advanced: List[str],
                         changes_made: List[Dict[str, Any]],
                         outcome: str,
                         ai_participant: str,
                         repository: str = "sunheart-core") -> Optional[str]:
        """
        Add an evolution step to a thread
        
        Args:
            thread_id: Thread ID
            title: Step title
            description: Detailed description
            goals_advanced: IDs of goals advanced by this step
            changes_made: List of changes made
            outcome: Description of the outcome
            ai_participant: ID of the contributing AI
            repository: Repository name
            
        Returns:
            Step ID if successful, None otherwise
        """
        try:
            thread = self.get_thread(thread_id, repository)
            if not thread:
                logger.error(f"Thread {thread_id} not found")
                return None
            
            # Create a unique step ID
            step_id = f"step_{hashlib.md5(f'{title}_{thread_id}_{datetime.datetime.now().isoformat()}'.encode()).hexdigest()[:12]}"
            
            # Create the step
            step = EvolutionStep(
                step_id=step_id,
                title=title,
                description=description,
                goals_advanced=goals_advanced,
                changes_made=changes_made,
                outcome=outcome,
                ai_participants=[ai_participant]
            )
            
            # Add the step to the thread
            thread.add_step(step)
            
            # Add the AI participant
            thread.add_ai_participant(ai_participant)
            
            # Update goals that were advanced
            for goal_id in goals_advanced:
                # Default to 10% progress increase per step
                for goal in thread.goals:
                    if goal.goal_id == goal_id:
                        progress = min(100, goal.progress + 10)
                        thread.update_goal_progress(goal_id, progress)
            
            # Save the updated thread
            self.update_thread(thread, repository)
            
            logger.info(f"Added evolution step {step_id} to thread {thread_id}")
            return step_id
            
        except Exception as e:
            logger.error(f"Error adding evolution step: {str(e)}")
            return None
    
    def update_goal_progress(self,
                           thread_id: str,
                           goal_id: str,
                           progress: int,
                           status: Optional[str] = None,
                           repository: str = "sunheart-core") -> bool:
        """
        Update the progress of a goal
        
        Args:
            thread_id: Thread ID
            goal_id: Goal ID
            progress: Progress percentage (0-100)
            status: Optional status update
            repository: Repository name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            thread = self.get_thread(thread_id, repository)
            if not thread:
                logger.error(f"Thread {thread_id} not found")
                return False
            
            # Update the goal
            if thread.update_goal_progress(goal_id, progress, status):
                # Save the updated thread
                self.update_thread(thread, repository)
                logger.info(f"Updated goal {goal_id} progress to {progress}%")
                return True
            else:
                logger.error(f"Goal {goal_id} not found in thread {thread_id}")
                return False
            
        except Exception as e:
            logger.error(f"Error updating goal progress: {str(e)}")
            return False
    
    def list_active_threads(self, repository: str = "sunheart-core") -> List[Dict[str, Any]]:
        """
        List all active threads
        
        Args:
            repository: Repository name
            
        Returns:
            List of thread summaries
        """
        try:
            active_index = self._load_active_threads_index(repository)
            active_threads = []
            
            for thread_info in active_index.get("threads", []):
                if thread_info.get("status") != "completed":
                    try:
                        thread = self.get_thread(thread_info["thread_id"], repository)
                        if thread:
                            active_threads.append(thread.get_progress_summary())
                    except Exception as thread_error:
                        logger.error(f"Error loading thread {thread_info['thread_id']}: {str(thread_error)}")
            
            return active_threads
            
        except Exception as e:
            logger.error(f"Error listing active threads: {str(e)}")
            return []
    
    def start_thread_evolution(self,
                             thread_id: str,
                             evolution_callback: Callable[[str], None],
                             evolution_interval: int = DEFAULT_EVOLUTION_INTERVAL,
                             repository: str = "sunheart-core") -> bool:
        """
        Start a thread evolution process that periodically evolves a thread
        
        Args:
            thread_id: Thread ID
            evolution_callback: Callback function to evolve the thread
            evolution_interval: Seconds between evolution attempts
            repository: Repository name
            
        Returns:
            True if started, False otherwise
        """
        try:
            # Check if the thread exists
            thread = self.get_thread(thread_id, repository)
            if not thread:
                logger.error(f"Thread {thread_id} not found")
                return False
            
            # Check if the thread is already running
            if thread_id in self.running_threads:
                logger.warning(f"Thread {thread_id} already evolving")
                return True
            
            # Create and start the evolution thread
            def _evolution_loop():
                while not self.shutdown_flag:
                    try:
                        # Get the latest thread state
                        current_thread = self.get_thread(thread_id, repository)
                        if not current_thread or current_thread.status != "active":
                            logger.info(f"Thread {thread_id} is no longer active, stopping evolution")
                            break
                        
                        # Call the evolution callback
                        logger.info(f"Evolving thread {thread_id}")
                        evolution_callback(thread_id)
                        
                    except Exception as evolution_error:
                        logger.error(f"Error in evolution loop for {thread_id}: {str(evolution_error)}")
                    
                    # Sleep until the next evolution attempt
                    for _ in range(evolution_interval):
                        if self.shutdown_flag:
                            break
                        time.sleep(1)
                
                # Remove from running threads when done
                if thread_id in self.running_threads:
                    del self.running_threads[thread_id]
                    logger.info(f"Stopped evolving thread {thread_id}")
            
            # Start the thread
            thread_obj = threading.Thread(target=_evolution_loop)
            thread_obj.daemon = True
            thread_obj.start()
            
            self.running_threads[thread_id] = thread_obj
            logger.info(f"Started evolving thread {thread_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error starting thread evolution: {str(e)}")
            return False
    
    def stop_thread_evolution(self, thread_id: str) -> bool:
        """
        Stop a thread evolution process
        
        Args:
            thread_id: Thread ID
            
        Returns:
            True if stopped, False otherwise
        """
        if thread_id in self.running_threads:
            del self.running_threads[thread_id]
            logger.info(f"Requested stop for thread {thread_id}")
            return True
        else:
            logger.warning(f"Thread {thread_id} not evolving")
            return False
    
    def shutdown(self) -> None:
        """
        Shut down all evolving threads
        """
        self.shutdown_flag = True
        logger.info("Shutting down all evolving threads")
    
    def _create_or_update_file(self, 
                             path: str,
                             repo_name: str,
                             commit_message: str,
                             content: str) -> bool:
        """
        Create or update a file in the repository
        
        Args:
            path: File path
            repo_name: Repository name
            commit_message: Commit message
            content: File content
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.github.create_or_update_file(
                repo_name=repo_name,
                path=path,
                commit_message=commit_message,
                content=content
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating/updating file {path}: {str(e)}")
            logger.debug(f"Would have written to {path}:\n{content}")
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
            
            self._create_or_update_file(
                path=gitkeep_path,
                repo_name=repo_name,
                commit_message=f"Create directory: {dir_path}",
                content="# This file maintains the directory structure"
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error ensuring directory {dir_path} exists: {str(e)}")
            return False
    
    def _update_active_threads_index(self, 
                                   repository: str,
                                   thread_id: str,
                                   thread_name: str) -> bool:
        """
        Update the active threads index file
        
        Args:
            repository: Repository name
            thread_id: Thread ID to add/update
            thread_name: Thread name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load the existing index if it exists
            active_index = self._load_active_threads_index(repository)
            
            # Add the thread to the index if it's not already there
            thread_exists = False
            for thread in active_index.get("threads", []):
                if thread["thread_id"] == thread_id:
                    thread["name"] = thread_name
                    thread["updated_at"] = datetime.datetime.now().isoformat()
                    thread_exists = True
                    break
            
            if not thread_exists:
                thread_info = {
                    "thread_id": thread_id,
                    "name": thread_name,
                    "status": "active",
                    "created_at": datetime.datetime.now().isoformat(),
                    "updated_at": datetime.datetime.now().isoformat()
                }
                
                if "threads" not in active_index:
                    active_index["threads"] = []
                
                active_index["threads"].append(thread_info)
            
            active_index["last_updated"] = datetime.datetime.now().isoformat()
            
            # Save the updated index
            self._create_or_update_file(
                path=self.ACTIVE_THREADS_INDEX,
                repo_name=repository,
                commit_message="Update active threads index",
                content=json.dumps(active_index, indent=2)
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating active threads index: {str(e)}")
            return False
    
    def _load_active_threads_index(self, repository: str) -> Dict[str, Any]:
        """
        Load the active threads index file
        
        Args:
            repository: Repository name
            
        Returns:
            Active threads index data (empty dict if not found)
        """
        try:
            index_content = self.github.get_file_content(
                repo_name=repository,
                file_path=self.ACTIVE_THREADS_INDEX
            )
            
            if index_content:
                return json.loads(index_content)
            
            return {"threads": [], "last_updated": datetime.datetime.now().isoformat()}
            
        except Exception as e:
            logger.debug(f"Active threads index not found, creating new one: {str(e)}")
            return {"threads": [], "last_updated": datetime.datetime.now().isoformat()}

# Create API functions for the self-evolving threads system
evolution_threads = SelfEvolvingThreads()

def create_evolution_thread(name: str,
                           description: str,
                           creator: str,
                           strategy: str,
                           initial_goals: Optional[List[Dict[str, Any]]] = None,
                           repository: str = "sunheart-core") -> Optional[str]:
    """
    Create a new self-evolving thread
    
    Args:
        name: Human-readable name
        description: Detailed description
        creator: ID of the creating AI
        strategy: Evolution strategy to follow
        initial_goals: Optional list of initial goals
        repository: Repository name
        
    Returns:
        Thread ID if successful, None otherwise
    """
    return evolution_threads.create_thread(
        name=name,
        description=description,
        creator=creator,
        strategy=strategy,
        initial_goals=initial_goals,
        repository=repository
    )

def get_evolution_thread(thread_id: str,
                        repository: str = "sunheart-core") -> Optional[Dict[str, Any]]:
    """
    Get a thread by ID
    
    Args:
        thread_id: Thread ID
        repository: Repository name
        
    Returns:
        Thread data if found, None otherwise
    """
    thread = evolution_threads.get_thread(thread_id, repository)
    return thread.to_dict() if thread else None

def add_evolution_step(thread_id: str,
                      title: str,
                      description: str,
                      goals_advanced: List[str],
                      changes_made: List[Dict[str, Any]],
                      outcome: str,
                      ai_participant: str,
                      repository: str = "sunheart-core") -> Optional[str]:
    """
    Add an evolution step to a thread
    
    Args:
        thread_id: Thread ID
        title: Step title
        description: Detailed description
        goals_advanced: IDs of goals advanced by this step
        changes_made: List of changes made
        outcome: Description of the outcome
        ai_participant: ID of the contributing AI
        repository: Repository name
        
    Returns:
        Step ID if successful, None otherwise
    """
    return evolution_threads.add_evolution_step(
        thread_id=thread_id,
        title=title,
        description=description,
        goals_advanced=goals_advanced,
        changes_made=changes_made,
        outcome=outcome,
        ai_participant=ai_participant,
        repository=repository
    )

def update_goal_progress(thread_id: str,
                        goal_id: str,
                        progress: int,
                        status: Optional[str] = None,
                        repository: str = "sunheart-core") -> bool:
    """
    Update the progress of a goal
    
    Args:
        thread_id: Thread ID
        goal_id: Goal ID
        progress: Progress percentage (0-100)
        status: Optional status update
        repository: Repository name
        
    Returns:
        True if successful, False otherwise
    """
    return evolution_threads.update_goal_progress(
        thread_id=thread_id,
        goal_id=goal_id,
        progress=progress,
        status=status,
        repository=repository
    )

def list_active_evolution_threads(repository: str = "sunheart-core") -> List[Dict[str, Any]]:
    """
    List all active threads
    
    Args:
        repository: Repository name
        
    Returns:
        List of thread summaries
    """
    return evolution_threads.list_active_threads(repository)

def start_thread_evolution(thread_id: str,
                          evolution_callback: Callable[[str], None],
                          repository: str = "sunheart-core") -> bool:
    """
    Start a thread evolution process
    
    Args:
        thread_id: Thread ID
        evolution_callback: Callback function to evolve the thread
        repository: Repository name
        
    Returns:
        True if started, False otherwise
    """
    return evolution_threads.start_thread_evolution(
        thread_id=thread_id,
        evolution_callback=evolution_callback,
        repository=repository
    )

def stop_thread_evolution(thread_id: str) -> bool:
    """
    Stop a thread evolution process
    
    Args:
        thread_id: Thread ID
        
    Returns:
        True if stopped, False otherwise
    """
    return evolution_threads.stop_thread_evolution(thread_id)

if __name__ == "__main__":
    # Example usage
    thread_id = create_evolution_thread(
        name="Protocol Harmonization",
        description="Evolve the protocol harmonization system to support more advanced negotiation strategies",
        creator="SelfEvolvingThreads",
        strategy="incremental",
        initial_goals=[
            {
                "name": "Add scoring rules for protocol capabilities",
                "description": "Add a rule system for evaluating protocol capabilities",
                "success_criteria": ["Rule system implemented", "Tests written", "Documentation updated"],
                "priority": 8
            },
            {
                "name": "Add compatibility analyzer",
                "description": "Develop a system to analyze compatibility between different protocols",
                "success_criteria": ["Compatibility matrix", "Translation rules", "Protocol mapper"],
                "priority": 7,
                "dependencies": []  # This could depend on the first goal if needed
            }
        ]
    )
    
    if thread_id:
        print(f"Created thread: {thread_id}")
    else:
        print("Failed to create thread")