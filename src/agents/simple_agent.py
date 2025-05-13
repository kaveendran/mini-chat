"""Simple agent implementation for chatbot enhancement."""
from typing import Dict, List, Optional, Any
from app.llm.model import LLMHandler
from config import settings

class SimpleAgent:
    """A simple agent that can perform basic tasks."""
    
    def __init__(self, llm_handler: LLMHandler):
        """Initialize the agent with an LLM handler.
        
        Args:
            llm_handler: Language model handler for generating responses
        """
        self.llm_handler = llm_handler
        # Access settings from config module
        self.settings = settings.settings
        self.enabled = self.settings["agent"]["enabled"]
        self.available_tools = self.settings["agent"]["tools"] or []
    
    def process_message(self, message: str, context: str = "") -> Dict[str, Any]:
        """Process a message and determine if agent actions are needed.
        
        Args:
            message: User message
            context: Additional context
            
        Returns:
            Dictionary with response and any action results
        """
        if not self.enabled:
            return {"response": None, "actions_taken": []}
        
        # Check if the message needs agent actions
        needs_action, actions = self._determine_actions(message)
        
        results = {"response": None, "actions_taken": []}
        
        if needs_action:
            # Execute actions
            for action in actions:
                action_result = self._execute_action(action, message)
                results["actions_taken"].append({
                    "action": action,
                    "result": action_result
                })
            
            # Generate a response that includes action results
            action_context = self._format_action_results(results["actions_taken"])
            full_context = f"{context}\n\n{action_context}" if context else action_context
            response = self.llm_handler.generate_response(message, full_context)
            results["response"] = response
        
        return results
    
    def _determine_actions(self, message: str) -> tuple[bool, List[str]]:
        """Determine if actions are needed based on the message.
        
        Args:
            message: User message
            
        Returns:
            Tuple of (needs_action, actions)
        """
        # For a simple implementation, check for keywords
        actions = []
        
        for tool in self.available_tools:
            # Simple keyword matching for demonstration
            if tool.lower() in message.lower():
                actions.append(tool)
        
        return len(actions) > 0, actions
    
    def _execute_action(self, action: str, message: str) -> str:
        """Execute an action based on the message.
        
        Args:
            action: Action to execute
            message: User message
            
        Returns:
            Result of the action
        """
        # This would be a more complex implementation in a real system
        # Here we just return a placeholder
        return f"Executed action {action} based on message"
    
    def _format_action_results(self, action_results: List[Dict[str, Any]]) -> str:
        """Format action results as context for the LLM.
        
        Args:
            action_results: List of action results
            
        Returns:
            Formatted context string
        """
        if not action_results:
            return ""
        
        context = "Agent actions performed:\n"
        for i, result in enumerate(action_results):
            context += f"{i+1}. Action '{result['action']}': {result['result']}\n"
        
        return context 