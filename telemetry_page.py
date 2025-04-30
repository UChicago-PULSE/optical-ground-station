from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy)
from PyQt6.QtCore import Qt

class TelemetryPage(QWidget):
    """Widget for displaying incoming telemetry data."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # --- Status Bar ---
        status_layout = QHBoxLayout()
        self.connection_status_label = QLabel("Status: System OFF", styleSheet="font-weight: bold; color: gray;")
        self.last_message_label = QLabel("Last Message: N/A")
        status_layout.addWidget(self.connection_status_label)
        status_layout.addStretch(1)
        status_layout.addWidget(self.last_message_label)
        layout.addLayout(status_layout)
        # --- End Status Bar ---

        # --- Telemetry Table ---
        self.telemetry_table = QTableWidget()
        self.telemetry_table.setColumnCount(3)
        self.telemetry_table.setHorizontalHeaderLabels(["Timestamp", "Parameter", "Value"])
        self.telemetry_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.telemetry_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.telemetry_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.telemetry_table.setRowCount(0) # Start empty
        layout.addWidget(self.telemetry_table)
        # --- End Telemetry Table ---

    def update_status(self, status_text, status_color, last_msg_text):
        """Updates the status labels."""
        self.connection_status_label.setText(status_text)
        self.connection_status_label.setStyleSheet(f"font-weight: bold; color: {status_color};")
        self.last_message_label.setText(last_msg_text)

    def add_telemetry_row(self, timestamp, parameter, value, max_rows):
        """Adds a new row to the telemetry table."""
        self.telemetry_table.insertRow(0)
        self.telemetry_table.setItem(0, 0, QTableWidgetItem(timestamp))
        self.telemetry_table.setItem(0, 1, QTableWidgetItem(parameter))
        self.telemetry_table.setItem(0, 2, QTableWidgetItem(value))
        if self.telemetry_table.rowCount() > max_rows:
            self.telemetry_table.removeRow(max_rows)

    def reset_status(self):
        """Resets status labels to the 'Off' state."""
        self.connection_status_label.setText("Status: System OFF")
        self.connection_status_label.setStyleSheet("font-weight: bold; color: gray;")
        self.last_message_label.setText("Last Message: N/A")