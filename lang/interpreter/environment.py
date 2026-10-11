"""
Environment for variable scoping and storage.
"""

from typing import Any, Optional, Dict


class Environment:
    """
    Environment for storing variables with lexical scoping.
    
    Each environment has a reference to its parent (enclosing scope),
    allowing for nested scopes and variable shadowing.
    """
    
    def __init__(self, parent: Optional['Environment'] = None):
        """
        Initialize an environment.
        
        Args:
            parent: Parent (enclosing) environment, if any
        """
        self.variables: Dict[str, Any] = {}
        self.parent = parent
    
    def define(self, name: str, value: Any) -> None:
        """
        Define a new variable in the current scope.
        
        Args:
            name: Variable name
            value: Variable value
        """
        self.variables[name] = value
    
    def get(self, name: str) -> Any:
        """
        Get a variable's value, searching parent scopes if needed.
        
        Args:
            name: Variable name
            
        Returns:
            The variable's value
            
        Raises:
            NameError if variable is not found
        """
        if name in self.variables:
            return self.variables[name]
        
        if self.parent:
            return self.parent.get(name)
        
        raise NameError(f"Undefined variable: {name}")
    
    def set(self, name: str, value: Any) -> None:
        """
        Set a variable's value, searching parent scopes if needed.
        
        Args:
            name: Variable name
            value: New value
            
        Raises:
            NameError if variable is not found
        """
        if name in self.variables:
            self.variables[name] = value
            return
        
        if self.parent:
            self.parent.set(name, value)
            return
        
        raise NameError(f"Undefined variable: {name}")
    
    def has(self, name: str) -> bool:
        """
        Check if a variable exists in current or parent scopes.
        
        Args:
            name: Variable name
            
        Returns:
            True if variable exists
        """
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.has(name)
        return False
    
    def all_variables(self) -> Dict[str, Any]:
        """
        Get all variables (including from parent scopes).
        
        Returns:
            Dictionary of all variables
        """
        result = {}
        if self.parent:
            result.update(self.parent.all_variables())
        result.update(self.variables)
        return result
