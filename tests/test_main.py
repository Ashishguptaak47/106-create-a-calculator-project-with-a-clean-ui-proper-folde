"""Unit tests for calculator engine and history state."""

import math
import pytest
from calculator.engine import CalculatorEngine, CalculationError
from calculator.history import HistoryManager


@pytest.fixture
def engine() -> CalculatorEngine:
    return CalculatorEngine()


@pytest.fixture
def history() -> HistoryManager:
    return HistoryManager(max_items=5)


def test_basic_arithmetic(engine: CalculatorEngine) -> None:
    assert engine.evaluate("2 + 3") == 5
    assert engine.evaluate("10 - 4") == 6
    assert engine.evaluate("3 × 7") == 21
    assert engine.evaluate("20 ÷ 4") == 5.0
    assert engine.evaluate("2 ^ 3") == 8


def test_operator_precedence(engine: CalculatorEngine) -> None:
    assert engine.evaluate("2 + 3 * 4") == 14
    assert engine.evaluate("(2 + 3) * 4") == 20
    assert engine.evaluate("100 - 50 / 2") == 75.0


def test_constants_and_functions(engine: CalculatorEngine) -> None:
    assert math.isclose(engine.evaluate("pi"), math.pi)
    assert math.isclose(engine.evaluate("sqrt(16)"), 4.0)
    assert math.isclose(engine.evaluate("sin(90)"), 1.0)  # sin in degrees
    assert math.isclose(engine.evaluate("cos(0)"), 1.0)
    assert math.isclose(engine.evaluate("log(100)"), 2.0)


def test_division_by_zero(engine: CalculatorEngine) -> None:
    with pytest.raises(CalculationError, match="Division by zero"):
        engine.evaluate("10 / 0")


def test_syntax_and_security(engine: CalculatorEngine) -> None:
    with pytest.raises(CalculationError):
        engine.evaluate("__import__('os').system('ls')")

    with pytest.raises(CalculationError):
        engine.evaluate("open('/etc/passwd')")

    with pytest.raises(CalculationError):
        engine.evaluate("2 ++ ")


def test_history_manager(history: HistoryManager) -> None:
    history.add_entry("2+2", "4")
    history.add_entry("3+3", "6")

    entries = history.get_entries()
    assert len(entries) == 2
    assert entries[0].expression == "3+3"
    assert entries[0].result == "6"

    history.clear()
    assert len(history.get_entries()) == 0


def test_memory_functions(history: HistoryManager) -> None:
    assert history.memory_recall() == 0.0
    history.memory_add(15.5)
    assert history.memory_recall() == 15.5
    history.memory_sub(5.5)
    assert history.memory_recall() == 10.0
    history.memory_clear()
    assert history.memory_recall() == 0.0
