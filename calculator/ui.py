"""Modern clean UI for the calculator application using Tkinter."""

import tkinter as tk
from tkinter import ttk
from typing import Callable
from calculator.engine import CalculatorEngine, CalculationError
from calculator.history import HistoryManager

# Modern Color Palette
BG_COLOR = "#1e1e2e"
PANEL_COLOR = "#181825"
BUTTON_BASE = "#313244"
BUTTON_HOVER = "#45475a"
BUTTON_ACCENT = "#89b4fa"
BUTTON_ACCENT_HOVER = "#b4befe"
BUTTON_DANGER = "#f38ba8"
TEXT_PRIMARY = "#cdd6f4"
TEXT_MUTED = "#a6adc8"
TEXT_DARK = "#11111b"


class CalculatorUI(tk.Tk):
    """Main Tkinter graphical interface for the calculator."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Calculator")
        self.geometry("380x600")
        self.minsize(360, 560)
        self.configure(bg=BG_COLOR)

        self.engine = CalculatorEngine()
        self.history = HistoryManager()

        self._current_expr = ""
        self._reset_next = False
        self._history_visible = False

        self._setup_styles()
        self._build_widgets()
        self._bind_keys()

    def _setup_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=BG_COLOR)

    def _build_widgets(self) -> None:
        # Top Display Area
        display_frame = tk.Frame(self, bg=PANEL_COLOR, bd=0, padx=16, pady=16)
        display_frame.pack(fill=tk.X, padx=12, pady=(12, 6))

        self.sub_display = tk.Label(
            display_frame,
            text="",
            font=("Helvetica", 11),
            fg=TEXT_MUTED,
            bg=PANEL_COLOR,
            anchor="e",
        )
        self.sub_display.pack(fill=tk.X)

        self.main_display = tk.Label(
            display_frame,
            text="0",
            font=("Helvetica", 26, "bold"),
            fg=TEXT_PRIMARY,
            bg=PANEL_COLOR,
            anchor="e",
        )
        self.main_display.pack(fill=tk.X, pady=(4, 0))

        # Toolbar (History toggle & Memory status)
        toolbar = tk.Frame(self, bg=BG_COLOR)
        toolbar.pack(fill=tk.X, padx=12, pady=(2, 6))

        self.hist_btn = tk.Button(
            toolbar,
            text="History ▾",
            font=("Helvetica", 9),
            bg=BUTTON_BASE,
            fg=TEXT_PRIMARY,
            activebackground=BUTTON_HOVER,
            activeforeground=TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=0,
            command=self._toggle_history,
        )
        self.hist_btn.pack(side=tk.LEFT, padx=2)

        for label, fn in [("MC", self._mem_clear), ("MR", self._mem_recall), ("M+", self._mem_add)]:
            btn = tk.Button(
                toolbar,
                text=label,
                font=("Helvetica", 9),
                bg=BUTTON_BASE,
                fg=TEXT_PRIMARY,
                activebackground=BUTTON_HOVER,
                activeforeground=TEXT_PRIMARY,
                relief=tk.FLAT,
                bd=0,
                padx=8,
                command=fn,
            )
            btn.pack(side=tk.RIGHT, padx=2)

        # Center container for keypad and overlay history
        self.content_frame = tk.Frame(self, bg=BG_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        self._build_keypad()
        self._build_history_panel()

    def _build_history_panel(self) -> None:
        self.history_frame = tk.Frame(self.content_frame, bg=PANEL_COLOR)
        list_scroll = tk.Scrollbar(self.history_frame)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_list = tk.Listbox(
            self.history_frame,
            bg=PANEL_COLOR,
            fg=TEXT_PRIMARY,
            selectbackground=BUTTON_BASE,
            selectforeground=TEXT_PRIMARY,
            font=("Helvetica", 11),
            bd=0,
            highlightthickness=0,
            yscrollcommand=list_scroll.set,
        )
        self.history_list.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        list_scroll.config(command=self.history_list.yview)
        self.history_list.bind("<Double-1>", self._on_history_select)

        btn_bar = tk.Frame(self.history_frame, bg=PANEL_COLOR)
        btn_bar.pack(fill=tk.X, padx=8, pady=4)
        clear_btn = tk.Button(
            btn_bar,
            text="Clear History",
            font=("Helvetica", 9),
            bg=BUTTON_DANGER,
            fg=TEXT_DARK,
            bd=0,
            command=self._clear_history,
        )
        clear_btn.pack(fill=tk.X)

    def _build_keypad(self) -> None:
        self.keypad_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        self.keypad_frame.pack(fill=tk.BOTH, expand=True)

        layout = [
            [("C", self._clear, BUTTON_DANGER, TEXT_DARK), ("(", lambda: self._append("("), BUTTON_BASE, TEXT_PRIMARY), (")", lambda: self._append(")"), BUTTON_BASE, TEXT_PRIMARY), ("⌫", self._backspace, BUTTON_BASE, TEXT_PRIMARY)],
            [("sin", lambda: self._append("sin("), BUTTON_BASE, TEXT_PRIMARY), ("cos", lambda: self._append("cos("), BUTTON_BASE, TEXT_PRIMARY), ("sqrt", lambda: self._append("sqrt("), BUTTON_BASE, TEXT_PRIMARY), ("÷", lambda: self._append("÷"), BUTTON_ACCENT, TEXT_DARK)],
            [("7", lambda: self._append("7"), BUTTON_BASE, TEXT_PRIMARY), ("8", lambda: self._append("8"), BUTTON_BASE, TEXT_PRIMARY), ("9", lambda: self._append("9"), BUTTON_BASE, TEXT_PRIMARY), ("×", lambda: self._append("×"), BUTTON_ACCENT, TEXT_DARK)],
            [("4", lambda: self._append("4"), BUTTON_BASE, TEXT_PRIMARY), ("5", lambda: self._append("5"), BUTTON_BASE, TEXT_PRIMARY), ("6", lambda: self._append("6"), BUTTON_BASE, TEXT_PRIMARY), ("-", lambda: self._append("-"), BUTTON_ACCENT, TEXT_DARK)],
            [("1", lambda: self._append("1"), BUTTON_BASE, TEXT_PRIMARY), ("2", lambda: self._append("2"), BUTTON_BASE, TEXT_PRIMARY), ("3", lambda: self._append("3"), BUTTON_BASE, TEXT_PRIMARY), ("+", lambda: self._append("+"), BUTTON_ACCENT, TEXT_DARK)],
            [("0", lambda: self._append("0"), BUTTON_BASE, TEXT_PRIMARY), (".", lambda: self._append("."), BUTTON_BASE, TEXT_PRIMARY), ("π", lambda: self._append("π"), BUTTON_BASE, TEXT_PRIMARY), ("=", self._calculate, BUTTON_ACCENT_HOVER, TEXT_DARK)],
        ]

        for r, row in enumerate(layout):
            self.keypad_frame.rowconfigure(r, weight=1)
            for c, (text, cmd, bg_col, fg_col) in enumerate(row):
                self.keypad_frame.columnconfigure(c, weight=1)
                btn = tk.Button(
                    self.keypad_frame,
                    text=text,
                    font=("Helvetica", 13, "bold"),
                    bg=bg_col,
                    fg=fg_col,
                    activebackground=BUTTON_HOVER,
                    activeforeground=TEXT_PRIMARY,
                    relief=tk.FLAT,
                    bd=0,
                    command=cmd,
                )
                btn.grid(row=r, column=c, sticky="nsew", padx=3, pady=3)

    def _bind_keys(self) -> None:
        self.bind("<Return>", lambda _: self._calculate())
        self.bind("<KP_Enter>", lambda _: self._calculate())
        self.bind("<Escape>", lambda _: self._clear())
        self.bind("<BackSpace>", lambda _: self._backspace())
        for ch in "0123456789.+-*/()":
            self.bind(ch, lambda e, c=ch: self._append("×" if c == "*" else ("÷" if c == "/" else c)))

    def _append(self, char: str) -> None:
        if self._reset_next and char not in "+-×÷":
            self._current_expr = ""
        self._reset_next = False

        self._current_expr += char
        self.main_display.config(text=self._current_expr)

    def _clear(self) -> None:
        self._current_expr = ""
        self.main_display.config(text="0")
        self.sub_display.config(text="")

    def _backspace(self) -> None:
        if self._reset_next:
            self._clear()
            return
        self._current_expr = self._current_expr[:-1]
        self.main_display.config(text=self._current_expr if self._current_expr else "0")

    def _calculate(self) -> None:
        if not self._current_expr:
            return
        raw_expr = self._current_expr
        try:
            result = self.engine.evaluate(raw_expr)
            # Format result nicely (strip redundant trailing zeros for floats)
            if isinstance(result, float):
                formatted = f"{result:.8f}".rstrip("0").rstrip(".")
            else:
                formatted = str(result)

            self.sub_display.config(text=f"{raw_expr} =")
            self.main_display.config(text=formatted)
            self.history.add_entry(raw_expr, formatted)
            self._current_expr = formatted
            self._reset_next = True
            self._refresh_history_list()
        except CalculationError as err:
            self.sub_display.config(text=raw_expr)
            self.main_display.config(text="Error")
            self._reset_next = True

    def _toggle_history(self) -> None:
        if self._history_visible:
            self.history_frame.pack_forget()
            self.keypad_frame.pack(fill=tk.BOTH, expand=True)
            self.hist_btn.config(text="History ▾")
        else:
            self._refresh_history_list()
            self.keypad_frame.pack_forget()
            self.history_frame.pack(fill=tk.BOTH, expand=True)
            self.hist_btn.config(text="Keypad ▴")
        self._history_visible = not self._history_visible

    def _refresh_history_list(self) -> None:
        self.history_list.delete(0, tk.END)
        for item in self.history.get_entries():
            self.history_list.insert(tk.END, f"{item.expression} = {item.result}")

    def _on_history_select(self, event: Any) -> None:
        sel = self.history_list.curselection()
        if not sel:
            return
        selected_text = self.history_list.get(sel[0])
        if "=" in selected_text:
            _, res = selected_text.split("=", 1)
            self._current_expr = res.strip()
            self.main_display.config(text=self._current_expr)
            self._toggle_history()

    def _clear_history(self) -> None:
        self.history.clear()
        self._refresh_history_list()

    def _mem_clear(self) -> None:
        self.history.memory_clear()

    def _mem_recall(self) -> None:
        val = self.history.memory_recall()
        formatted = str(int(val)) if val.is_integer() else str(val)
        self._append(formatted)

    def _mem_add(self) -> None:
        try:
            val = float(self.main_display.cget("text"))
            self.history.memory_add(val)
        except ValueError:
            pass
