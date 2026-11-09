"""Entry point for launching the modern Calculator application."""

import sys
from calculator.ui import CalculatorUI


def main() -> int:
    """Start the application mainloop."""
    app = CalculatorUI()
    app.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
