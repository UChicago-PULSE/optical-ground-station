from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QPushButton, QWidget,
                             QStackedWidget, QLabel, QHBoxLayout, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPalette
import numpy as np
from datetime import datetime
from collections import deque

# Import page widgets
from telemetry_page import TelemetryPage
from data_analysis_page import DataAnalysisPage

# --- Constants ---
MAX_DATA_POINTS = 100 # Max points to store and plot
MAX_TABLE_ROWS = 50 # Max rows for telemetry table
# --- End Constants ---

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PULSE-A Interface")
        self.setGeometry(100, 100, 1200, 800)

        # --- Data Storage ---
        self.timestamps = deque(maxlen=MAX_DATA_POINTS)
        self.sensor_a_data = deque(maxlen=MAX_DATA_POINTS)
        self.sensor_b_data = deque(maxlen=MAX_DATA_POINTS)
        # --- End Data Storage ---

        # Main container widget and layout
        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top Menu Row
        top_menu = QWidget()
        top_menu.setStyleSheet("background-color: lightgray;")
        top_menu.setFixedHeight(50)
        top_menu_layout = QHBoxLayout(top_menu)
        top_menu_layout.setContentsMargins(10, 5, 10, 5)

        label = QLabel("PULSE-A Ground Control")
        label.setStyleSheet("font-size: 20pt; font-weight: bold;")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        top_menu_layout.addWidget(label)
        top_menu_layout.addStretch(1)

        # On/Off Button
        power_symbol = "\u23FB"
        self.on_off_button = QPushButton(power_symbol)
        self.on_off_button.setCheckable(True)
        self.on_off_button.setChecked(False)
        self.on_off_button.setFixedWidth(50)
        self.on_off_button.setFixedHeight(35)
        font = self.on_off_button.font()
        font.setPointSize(16)
        self.on_off_button.setFont(font)
        self.on_off_button.setStyleSheet("""
            QPushButton { background-color: red; color: white; border: 1px solid darkred; border-radius: 17px; font-weight: bold; padding: 0px; }
            QPushButton:checked { background-color: lightgreen; border: 1px solid darkgreen; color: black; }
            QPushButton:hover { border: 2px solid black; }
        """)
        self.on_off_button.toggled.connect(self.handle_on_off_toggle)
        top_menu_layout.addWidget(self.on_off_button)
        main_layout.addWidget(top_menu)

        # Content Area Layout (Sidebar + Pages)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Sidebar
        sidebar_container = QWidget()
        sidebar_container.setStyleSheet("background-color: lightgray;")
        sidebar_container.setFixedWidth(170)
        sidebar_layout = QVBoxLayout(sidebar_container)
        sidebar_layout.setContentsMargins(10, 0, 10, 0)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.button_names = ["Incoming Telemetry", "Data Analysis", "Telescope Controls", "Command Center"]
        self.buttons = [ QPushButton(name) for name in self.button_names]
        for button in self.buttons:
            button.clicked.connect(self.change_page)
            sidebar_layout.addWidget(button)

        # Pages
        self.pages = QStackedWidget()
        # Instantiate page widgets
        self.telemetry_page = TelemetryPage()
        self.data_analysis_page = DataAnalysisPage(main_window=self) # Pass self
        # Add instances to stacked widget
        self.pages.addWidget(self.telemetry_page)
        self.pages.addWidget(self.data_analysis_page)
        # Add placeholder pages
        self.pages.addWidget(self.create_placeholder_page("Telescope Controls Page"))
        self.pages.addWidget(self.create_placeholder_page("Command Center Page"))

        content_layout.addWidget(sidebar_container)
        content_layout.addWidget(self.pages)
        main_layout.addLayout(content_layout)
        self.setCentralWidget(main_container)

        # Timer
        self.telemetry_timer = QTimer(self)
        self.telemetry_timer.timeout.connect(self.update_incoming_data)

    # --- Handler for the toggle button ---
    def handle_on_off_toggle(self, checked):
        if checked:
            print("System turned ON")
            self.telemetry_timer.start(1000) # Update interval
            # Clear old data on restart? Optional.
            # self.timestamps.clear()
            # self.sensor_a_data.clear()
            # self.sensor_b_data.clear()
            # self.data_analysis_page.update_plots() # Update plots if clearing data
            # self.data_analysis_page.update_table(MAX_TABLE_ROWS)
        else:
            print("System turned OFF")
            self.telemetry_timer.stop()
            # Reset status on the telemetry page
            self.telemetry_page.reset_status()

    # --- Generic placeholder page creation ---
    def create_placeholder_page(self, text):
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel(text, alignment=Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18px;")
        layout.addWidget(label)
        return page

    # --- Function to handle incoming data and update UI ---
    def update_incoming_data(self):
        # Simulate connection status and data fetching
        is_connected = np.random.rand() > 0.1
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        if is_connected:
            status_text = "Status: Connected"
            status_color = "green"
            last_msg = f"Last Message: {now_str}"

            # Simulate new data points for different sensors
            param = f"Sensor_{np.random.choice(['A', 'B', 'C', 'Temp'])}"
            value = np.random.rand() * 100
            value_str = f"{value:.3f}"

            # --- Update Telemetry Page ---
            self.telemetry_page.add_telemetry_row(now_str, param, value_str, MAX_TABLE_ROWS)
            # --- End Telemetry Page Update ---

            # --- Store Data for Analysis ---
            self.timestamps.append(now)
            sensor_a_val = np.nan
            sensor_b_val = np.nan
            if param == "Sensor_A":
                sensor_a_val = value
            elif param == "Sensor_B":
                sensor_b_val = value
            # Ensure deques stay aligned even if only one sensor updates
            self.sensor_a_data.append(sensor_a_val)
            self.sensor_b_data.append(sensor_b_val)
            # --- End Data Storage ---

            # --- Update Analysis Page ---
            self.data_analysis_page.update_plots()
            self.data_analysis_page.update_table(MAX_TABLE_ROWS) # Use constant
            # --- End Analysis Update ---

        else:
            status_text = "Status: Disconnected"
            status_color = "red"
            last_msg = self.telemetry_page.last_message_label.text() # Keep last message time

            # Optionally append NaNs when disconnected
            # self.timestamps.append(now)
            # self.sensor_a_data.append(np.nan)
            # self.sensor_b_data.append(np.nan)
            # self.data_analysis_page.update_plots()

        # Update status on telemetry page regardless of connection
        self.telemetry_page.update_status(status_text, status_color, last_msg)


    def change_page(self):
        sender = self.sender()
        try:
            # Find index based on button text matching the list
            index = self.button_names.index(sender.text())
            self.pages.setCurrentIndex(index)
        except ValueError:
            print(f"Error: Button '{sender.text()}' not found in expected names.")

# --- No PlotCanvas class here anymore ---

# --- No main execution block here anymore ---