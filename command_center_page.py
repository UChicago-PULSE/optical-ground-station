from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                             QPushButton, QLabel, QPlainTextEdit, QSizePolicy)
from PyQt6.QtGui import QFont, QColor, QPalette, QBrush, QTextCharFormat, QTextCursor
from PyQt6.QtCore import Qt

# --- Add imports for execution and output capture ---
import io
import contextlib
import traceback
# --- End imports ---

class CommandCenterPage(QWidget):
    """Widget for sending commands and viewing responses."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # --- Script Editor Section ---
        editor_label = QLabel("Python Command Script Editor:") # Updated label
        layout.addWidget(editor_label)

        self.script_editor = QPlainTextEdit()
        font = QFont("Courier New", 11)
        self.script_editor.setFont(font)
        self.script_editor.setPlaceholderText("Enter Python commands here...")
        self.script_editor.setFixedHeight(200)
        layout.addWidget(self.script_editor)
        # --- End Script Editor Section ---

        # --- Send Button ---
        self.send_button = QPushButton("Execute Python Script") # Updated button text
        self.send_button.clicked.connect(self.send_command)
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.send_button)
        button_layout.addStretch(1)
        layout.addLayout(button_layout)
        # --- End Send Button ---

        # --- Terminal Emulator Section ---
        terminal_label = QLabel("Output / Response Terminal:")
        layout.addWidget(terminal_label)

        self.terminal_output = QPlainTextEdit()
        self.terminal_output.setReadOnly(True)
        terminal_font = QFont("Courier New", 10)
        self.terminal_output.setFont(terminal_font)
        palette = self.terminal_output.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Text, QColor(200, 200, 200))
        self.terminal_output.setPalette(palette)
        self.terminal_output.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.terminal_output)
        # --- End Terminal Emulator Section ---

    def send_command(self):
        """Handles executing the Python script from the editor."""
        script_text = self.script_editor.toPlainText().strip()
        if not script_text:
            self.append_terminal_text(">> No script entered.", QColor("yellow"))
            return

        # Display the script being executed
        # self.append_terminal_text(f">> Executing:\n---\n{script_text}\n---", QColor("cyan"))
        self.append_terminal_text(f">> Executing Python script...", QColor("cyan"))

        # --- Execute Python code and capture output ---
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        try:
            # Redirect stdout and stderr
            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                # Execute the script in a dictionary scope (safer than default globals/locals)
                exec_globals = {}
                exec(script_text, exec_globals)

            # Get captured output
            stdout_result = stdout_capture.getvalue()
            stderr_result = stderr_capture.getvalue()

            # Display stdout if any
            if stdout_result:
                self.append_terminal_text(f"<< Stdout:\n{stdout_result.strip()}", QColor(200, 200, 200)) # Default color

            # Display stderr if any
            if stderr_result:
                self.append_terminal_text(f"<< Stderr:\n{stderr_result.strip()}", QColor("orange")) # Orange for stderr

            if not stdout_result and not stderr_result:
                 self.append_terminal_text("<< Script executed successfully (no output).", QColor("lightgreen"))


        except Exception as e:
            # Capture and display traceback for exceptions during exec()
            error_traceback = traceback.format_exc()
            self.append_terminal_text(f"<< Error executing script:\n{error_traceback.strip()}", QColor("red"))
        finally:
            # Close the StringIO objects
            stdout_capture.close()
            stderr_capture.close()
        # --- End Execution ---

        # Optionally clear the editor after sending
        # self.script_editor.clear()

    def append_terminal_text(self, text, color=None):
        """Appends text to the terminal display with optional color."""
        cursor = self.terminal_output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.terminal_output.setTextCursor(cursor)

        # Get the default char format to preserve font etc.
        default_format = self.terminal_output.currentCharFormat()
        # Ensure default text color is set correctly if no color override
        default_palette_color = self.terminal_output.palette().color(QPalette.ColorRole.Text)
        default_format.setForeground(QBrush(default_palette_color))

        if color:
            # Create a new format with the desired color
            text_format = QTextCharFormat(default_format)
            text_format.setForeground(QBrush(color))
            self.terminal_output.setCurrentCharFormat(text_format)
            self.terminal_output.insertPlainText(text + "\n")
            # Reset to default format for subsequent text
            self.terminal_output.setCurrentCharFormat(default_format)
        else:
            # Apply default format explicitly
            self.terminal_output.setCurrentCharFormat(default_format)
            self.terminal_output.insertPlainText(text + "\n")

        # Ensure the new text is visible
        self.terminal_output.ensureCursorVisible()

# Example of how to integrate (in main_window.py) - No changes needed here
# from command_center_page import CommandCenterPage
# ...
# self.command_center_page = CommandCenterPage()
# self.pages.addWidget(self.command_center_page)