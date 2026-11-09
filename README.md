# Modern Desktop Calculator

A modern, clean, and extensible desktop calculator built in Python with `tkinter` and safe AST-based mathematical evaluation.

## Features

- **Clean Modern UI**: Dark-themed responsive interface inspired by modern design systems.
- **Safe Evaluation Engine**: Custom expression parser leveraging Python's `ast` (Abstract Syntax Tree) to prevent arbitrary code execution while supporting rich math operations.
- **Extended Functions**: Trigonometric functions (`sin`, `cos`, `tan`), logarithms (`log`, `ln`), square roots (`sqrt`), constants ($\\pi$, $e$), percentages, and power operations.
- **Calculation History**: Built-in history tracking to review and reload previous computations.
- **Keyboard Integration**: Full keyboard support (Enter to compute, Esc to clear, Backspace, digits, and operator keys).
- **Unit Tested**: Comprehensive test suite covering arithmetic, edge cases, error handling, and security.

## Folder Structure

```text
.
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── calculator/
│   ├── __init__.py
│   ├── engine.py       # Safe mathematical AST evaluator
│   ├── history.py      # History logging and memory state
│   └── ui.py           # Tkinter interface & event binding
└── tests/
    ├── __init__.py
    └── test_main.py    # Test suite for engine & history
```

## Installation & Running

Ensure you have Python 3.9+ installed. The GUI uses standard library `tkinter`.

```bash
# Run the calculator application
python main.py

# Run the test suite
pip install -r requirements.txt
pytest
```
