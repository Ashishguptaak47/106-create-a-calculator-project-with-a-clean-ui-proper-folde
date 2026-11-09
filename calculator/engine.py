"""Safe AST-based calculation engine."""

import ast
import math
import operator
from typing import Any, Union


class CalculationError(Exception):
    """Custom exception for calculation errors."""
    pass


class CalculatorEngine:
    """Safely evaluates mathematical expressions using AST parsing."""

    _OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    _CONSTANTS = {
        "pi": math.pi,
        "e": math.e,
    }

    _FUNCTIONS = {
        "sqrt": math.sqrt,
        "sin": lambda x: math.sin(math.radians(x)),
        "cos": lambda x: math.cos(math.radians(x)),
        "tan": lambda x: math.tan(math.radians(x)),
        "log": math.log10,
        "ln": math.log,
        "abs": abs,
        "fact": math.factorial,
    }

    def evaluate(self, expression: str) -> Union[int, float]:
        """Evaluate a mathematical string expression safely."""
        if not expression or not expression.strip():
            return 0

        cleaned = (
            expression.replace("×", "*")
            .replace("÷", "/")
            .replace("^", "**")
            .replace("π", "pi")
            .strip()
        )

        try:
            node = ast.parse(cleaned, mode="eval")
            return self._eval_node(node.body)
        except ZeroDivisionError:
            raise CalculationError("Division by zero")
        except (SyntaxError, ValueError, OverflowError) as exc:
            raise CalculationError(f"Invalid expression: {exc}")
        except Exception as exc:
            raise CalculationError(f"Evaluation error: {exc}")

    def _eval_node(self, node: ast.AST) -> Any:
        """Recursively evaluate AST nodes with strict allowlist."""
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise CalculationError(f"Unsupported literal: {node.value}")

        if isinstance(node, ast.Name):
            if node.id in self._CONSTANTS:
                return self._CONSTANTS[node.id]
            raise CalculationError(f"Unknown variable: '{node.id}'")

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in self._OPERATORS:
                raise CalculationError(f"Unsupported operator: {op_type.__name__}")
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return self._OPERATORS[op_type](left, right)

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in self._OPERATORS:
                raise CalculationError(f"Unsupported unary operator: {op_type.__name__}")
            operand = self._eval_node(node.operand)
            return self._OPERATORS[op_type](operand)

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise CalculationError("Dynamic function calls are prohibited")
            fn_name = node.func.id
            if fn_name not in self._FUNCTIONS:
                raise CalculationError(f"Unsupported function: '{fn_name}'")
            args = [self._eval_node(arg) for arg in node.args]
            return self._FUNCTIONS[fn_name](*args)

        raise CalculationError(f"Syntax construct not permitted: {type(node).__name__}")
