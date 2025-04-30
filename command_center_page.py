from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                             QPushButton, QLabel, QPlainTextEdit, QSizePolicy) # Added QSizePolicy
from PyQt6.QtGui import QFont, QColor, QPalette, QBrush, QTextCharFormat, QTextCursor # Added QPalette, QBrush, QTextCharFormat, QTextCursor
from PyQt6.QtCore import Qt

class CommandCenterPage(QWidget):
    """Widget for sending commands and viewing responses."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # --- Script Editor Section ---
        editor_label = QLabel("Command Script Editor:")
        layout.addWidget(editor_label)

        self.script_editor = QPlainTextEdit()
        # Use a monospaced font for code editing
        font = QFont("Courier New", 11) # Or another monospaced font like Monaco, Consolas
        self.script_editor.setFont(font)
        self.script_editor.setPlaceholderText("Enter Python commands here...")
        # Set a reasonable initial height
        self.script_editor.setFixedHeight(200)
        layout.addWidget(self.script_editor)
        # --- End Script Editor Section ---

        # --- Send Button ---
        self.send_button = QPushButton("Send Command")
        self.send_button.clicked.connect(self.send_command)
        # Align button to the right or center if desired
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
        # Basic terminal styling
        terminal_font = QFont("Courier New", 10)
        self.terminal_output.setFont(terminal_font)
        palette = self.terminal_output.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(0, 0, 0)) # Black background
        palette.setColor(QPalette.ColorRole.Text, QColor(200, 200, 200)) # Light gray text
        self.terminal_output.setPalette(palette)
        # Make terminal take remaining space
        self.terminal_output.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.terminal_output)
        # --- End Terminal Emulator Section ---

    def send_command(self):
        """Handles sending the command from the editor."""
        command_text = self.script_editor.toPlainText().strip()
        if not command_text:
            self.append_terminal_text(">> No command entered.", QColor("yellow"))
            return

        # Display the command being sent in the terminal
        self.append_terminal_text(f">> Sending: {command_text}", QColor("cyan"))

        # --- Placeholder for actual command execution ---
        # In a real application, you would send this command_text
        # to your backend/control system via sockets, serial, etc.
        # and receive a response asynchronously.
        print(f"Executing command:\n{command_text}") # Print to console for now

        # Simulate receiving a confirmation and response
        # Replace this with actual response handling
        confirmation = "Command received by backend."
        response = f"Executed: {command_text}\nResult: OK (Simulated)" # Example response
        self.append_terminal_text(f"<< {confirmation}", QColor("lightgreen"))
        self.append_terminal_text(f"<< {response}", QColor(200, 200, 200)) # Default text color
        # --- End Placeholder ---

        # Optionally clear the editor after sending
        # self.script_editor.clear()

    def append_terminal_text(self, text, color=None):
        """Appends text to the terminal display with optional color."""
        cursor = self.terminal_output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.terminal_output.setTextCursor(cursor)

        if color:
            # Get the default char format to preserve font etc.
            default_format = self.terminal_output.currentCharFormat()
            # Create a new format with the desired color
            text_format = QTextCharFormat(default_format)
            text_format.setForeground(QBrush(color))
            self.terminal_output.setCurrentCharFormat(text_format)
            self.terminal_output.insertPlainText(text + "\n")
            # Reset to default format for subsequent text
            self.terminal_output.setCurrentCharFormat(default_format)
        else:
            self.terminal_output.insertPlainText(text + "\n")

        # Ensure the new text is visible
        self.terminal_output.ensureCursorVisible()

# Example of how to integrate (in main_window.py)
# from command_center_page import CommandCenterPage
# ...
# self.command_center_page = CommandCenterPage()
# self.pages.addWidget(self.command_center_page)