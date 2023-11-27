from typing import Callable, Any
from agents.lunatic_agent import LunaticAgent
import inspect

class EvaluationFunction:
    def __init__(self, evaluation_function:Callable[[LunaticAgent], bool], name="EvaluationFunction"):
        """Note this is a decorator, so the evaluation_function should be a function that takes in a LunaticAgent and returns a boolean"""
        self.evaluation_function = evaluation_function
        self.name = name

    def __call__(self, agent, *args, **kwargs) -> bool:
        return self.evaluation_function(agent, *args, **kwargs)

    @staticmethod 
    def _complete_func_to_string(func):
        funcString = inspect.getsourcelines(func)[0]
        if not funcString[0].startswith("def"): 
            # assuming foo = lambda: ...
            assert len(funcString) == 1, "BUG/TEST: Only one line should be returned from getsourcelines() when using lambda functions."
            _, funcString = funcString[0].split("=", 1)
            funcString = funcString.strip()
            return funcString
        #funcString = funcString.strip("['\\n']")
        funcString = "".join(funcString) 
        return funcString
    
    @staticmethod
    def _func_to_string(func):
        """If the function has a name return the name, otherwise only the lambda expression."""
        if func.__name__ == "<lambda>": 
            funcString = inspect.getsourcelines(func)[0]
            assert len(funcString) == 1, "BUG/TEST: Only one line should be returned from getsourcelines() when using lambda functions."
            return funcString[0].strip("\n")
            # only the functional part:
            _, funcString = funcString[0].split(":", 1)
            funcString = funcString.strip()
            return funcString
        return func.__name__


    def __str__(self):
        return self.name

    @classmethod 
    def AND(cls, func1, func2):
        """Creates a new EvaluationFunction as an AND combination of two other EvaluationFunctions"""
        def combined_func(*args, **kwargs):
            return func1(*args, **kwargs) and func2(*args, **kwargs)
        return cls(combined_func, f"{func1.__class__.__name__}_and_{func2.__class__.__name__}")
    
    @classmethod
    def OR(cls, func1, func2):
        """Creates a new EvaluationFunction as an OR combination of two other EvaluationFunctions"""
        def combined_func(*args, **kwargs):
            return func1(*args, **kwargs) or func2(*args, **kwargs)
        return cls(combined_func, f"{func1.__class__.__name__}_or_{func2.__class__.__name__}")
    
    @classmethod
    def NOT(cls, func):
        """Creates a new EvaluationFunction as a NOT combination of another EvaluationFunction"""
        def combined_func(*args, **kwargs):
            return not func(*args, **kwargs)
        return cls(combined_func, f"not_{func.__class__.__name__}")
    
    def __add__(self, other):
        return self.AND(self, other)
    
    def __or__(self, other):
        """NOTE: This is the bitwise OR operator, not the logical OR operator."""
        return self.OR(self, other)
    
    def __invert__(self):
        return self.NOT(self)
    

class ActionFunction(EvaluationFunction):
    def __init__(self, action_function:Callable[[LunaticAgent], Any]):
        """Note this is a decorator, so the action_function should be a function that takes in a LunaticAgent and operates on it."""
        self.action_function = action_function

    @classmethod
    def NOT(cls, func):
        NotImplemented

    def __call__(self, agent, *args, **kwargs) -> Any:
        return self.action_function(agent, *args, **kwargs)
    
