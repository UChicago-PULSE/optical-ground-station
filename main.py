from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QPushButton,
                             QWidget, QStackedWidget, QLabel, QHBoxLayout,
                             QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem,
                             QHeaderView) # Added QHeaderView
from PyQt6.QtCore import Qt, QTimer # Import QTimer
from PyQt6.QtGui import QPalette # Import QPalette to get colors
import matplotlib.pyplot as plt
# --- Use the general Qt Agg backend ---
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime # Import datetime
from collections import deque # Import deque for efficient data storage

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
        self.buttons = [ QPushButton(name) for name in ["Incoming Telemetry", "Data Analysis", "Telescope Controls", "Command Center"]]
        for button in self.buttons:
            button.clicked.connect(self.change_page)
            sidebar_layout.addWidget(button)

        # Pages
        self.pages = QStackedWidget()
        self.pages.addWidget(self.create_telemetry_page())
        self.pages.addWidget(self.create_data_analysis_page())
        self.pages.addWidget(self.create_page("Telescope Controls Page"))
        self.pages.addWidget(self.create_page("Command Center Page"))

        content_layout.addWidget(sidebar_container)
        content_layout.addWidget(self.pages)
        main_layout.addLayout(content_layout)
        self.setCentralWidget(main_container)

        # Timer
        self.telemetry_timer = QTimer(self)
        self.telemetry_timer.timeout.connect(self.update_incoming_data) # Changed target function

    # --- Handler for the toggle button ---
    def handle_on_off_toggle(self, checked):
        if checked:
            print("System turned ON")
            self.telemetry_timer.start(1000) # Update interval
            # Clear old data on restart? Optional.
            # self.timestamps.clear()
            # self.sensor_a_data.clear()
            # self.sensor_b_data.clear()
        else:
            print("System turned OFF")
            self.telemetry_timer.stop()
            self.connection_status_label.setText("Status: System OFF")
            self.connection_status_label.setStyleSheet("font-weight: bold; color: gray;")
            self.last_message_label.setText("Last Message: N/A")

    # --- Generic page creation ---
    def create_page(self, text):
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel(text, alignment=Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18px;")
        layout.addWidget(label)
        return page

    # --- Create Incoming Telemetry page ---
    def create_telemetry_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        status_layout = QHBoxLayout()
        self.connection_status_label = QLabel("Status: System OFF", styleSheet="font-weight: bold; color: gray;")
        self.last_message_label = QLabel("Last Message: N/A")
        status_layout.addWidget(self.connection_status_label)
        status_layout.addStretch(1)
        status_layout.addWidget(self.last_message_label)
        layout.addLayout(status_layout)

        self.telemetry_table = QTableWidget()
        self.telemetry_table.setColumnCount(3)
        self.telemetry_table.setHorizontalHeaderLabels(["Timestamp", "Parameter", "Value"])
        self.telemetry_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.telemetry_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.telemetry_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.telemetry_table.setRowCount(0) # Start empty
        layout.addWidget(self.telemetry_table)
        return page

    # --- Create Data Analysis page ---
    def create_data_analysis_page(self):
        page = QWidget()
        main_page_layout = QVBoxLayout(page)
        main_page_layout.setContentsMargins(10, 10, 10, 10)
        main_page_layout.setSpacing(15)

        plot_row_layout = QHBoxLayout()
        plot_row_layout.setSpacing(10)
        bg_color = self.palette().color(QPalette.ColorRole.Window).name()

        # Store references to plot canvases, pass MainWindow instance
        self.plot_canvas1 = PlotCanvas(self, width=5, height=3.5, plot_title="Sensor A", bg_color=bg_color, data_source='a', main_window=self) # Pass self as main_window
        self.plot_canvas2 = PlotCanvas(self, width=5, height=3.5, plot_title="Sensor B", bg_color=bg_color, data_source='b', main_window=self) # Pass self as main_window
        plot_row_layout.addWidget(self.plot_canvas1)
        plot_row_layout.addWidget(self.plot_canvas2)

        # --- Create Table Widget (Now linked to data) ---
        self.analysis_table = QTableWidget() # Renamed to avoid confusion
        self.analysis_table.setRowCount(0) # Start empty
        self.analysis_table.setColumnCount(3) # Example: Time, Sensor A, Sensor B
        self.analysis_table.setHorizontalHeaderLabels(["Time", "Sensor A", "Sensor B"])
        self.analysis_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.analysis_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.analysis_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # --- End of Table Widget Creation ---

        main_page_layout.addStretch(1)
        main_page_layout.addLayout(plot_row_layout, 4)
        main_page_layout.addWidget(self.analysis_table, 4) # Add the analysis table
        main_page_layout.addStretch(0)
        # Set the layout on the page widget
        page.setLayout(main_page_layout) # Added this line
        return page

    # --- Function to handle incoming data and update UI ---
    def update_incoming_data(self):
        # Simulate connection status and data fetching
        is_connected = np.random.rand() > 0.1
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        if is_connected:
            self.connection_status_label.setText("Status: Connected")
            self.connection_status_label.setStyleSheet("font-weight: bold; color: green;")
            self.last_message_label.setText(f"Last Message: {now_str}")

            # Simulate new data points for different sensors
            param = f"Sensor_{np.random.choice(['A', 'B', 'C', 'Temp'])}"
            value = np.random.rand() * 100
            value_str = f"{value:.3f}"

            # --- Update Telemetry Table ---
            self.telemetry_table.insertRow(0)
            self.telemetry_table.setItem(0, 0, QTableWidgetItem(now_str))
            self.telemetry_table.setItem(0, 1, QTableWidgetItem(param))
            self.telemetry_table.setItem(0, 2, QTableWidgetItem(value_str))
            if self.telemetry_table.rowCount() > MAX_TABLE_ROWS:
                self.telemetry_table.removeRow(MAX_TABLE_ROWS)
            # --- End Telemetry Table Update ---

            # --- Store Data for Analysis ---
            self.timestamps.append(now) # Store datetime objects for plotting if needed
            if param == "Sensor_A":
                self.sensor_a_data.append(value)
                self.sensor_b_data.append(np.nan) # Append NaN if no B value this tick
            elif param == "Sensor_B":
                self.sensor_b_data.append(value)
                self.sensor_a_data.append(np.nan) # Append NaN if no A value this tick
            else:
                # Handle other sensors if needed, or append NaN to keep lengths consistent
                self.sensor_a_data.append(np.nan)
                self.sensor_b_data.append(np.nan)
            # --- End Data Storage ---

            # --- Update Analysis Page ---
            self.update_analysis_plots()
            self.update_analysis_table()
            # --- End Analysis Update ---

        else:
            self.connection_status_label.setText("Status: Disconnected")
            self.connection_status_label.setStyleSheet("font-weight: bold; color: red;")
            # Optionally append NaNs when disconnected to show gaps in plots
            # self.timestamps.append(now)
            # self.sensor_a_data.append(np.nan)
            # self.sensor_b_data.append(np.nan)
            # self.update_analysis_plots() # Update plots to show gap

    # --- Update analysis plots ---
    def update_analysis_plots(self):
        # Check if canvases exist before plotting
        if hasattr(self, 'plot_canvas1'):
            self.plot_canvas1.plot()
        if hasattr(self, 'plot_canvas2'):
            self.plot_canvas2.plot()

    # --- Update analysis table ---
    def update_analysis_table(self):
        if not hasattr(self, 'analysis_table'):
            return # Don't try to update if table doesn't exist yet

        self.analysis_table.setRowCount(0) # Clear existing rows
        # Display the latest data points (up to table capacity or data length)
        num_rows_to_show = min(len(self.timestamps), MAX_TABLE_ROWS) # Or a different limit
        for i in range(num_rows_to_show):
            # Get data from the end of the deque (most recent)
            idx = len(self.timestamps) - 1 - i
            ts = self.timestamps[idx].strftime("%H:%M:%S.%f")[:-3] # Format time
            val_a = f"{self.sensor_a_data[idx]:.2f}" if not np.isnan(self.sensor_a_data[idx]) else "-"
            val_b = f"{self.sensor_b_data[idx]:.2f}" if not np.isnan(self.sensor_b_data[idx]) else "-"

            self.analysis_table.insertRow(0) # Insert at top
            self.analysis_table.setItem(0, 0, QTableWidgetItem(ts))
            self.analysis_table.setItem(0, 1, QTableWidgetItem(val_a))
            self.analysis_table.setItem(0, 2, QTableWidgetItem(val_b))


    def change_page(self):
        sender = self.sender()
        try:
            index = self.buttons.index(sender)
            self.pages.setCurrentIndex(index)
        except ValueError:
            print("Error: Sender button not found in the list.")


# --- Modify PlotCanvas class ---
class PlotCanvas(FigureCanvas):
    # Add main_window parameter
    def __init__(self, parent=None, width=5, height=3.5, dpi=100, plot_title='Sample Plot', bg_color='#F0F0F0', data_source=None, main_window=None): # Added main_window
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor(bg_color)
        fig.subplots_adjust(left=0.15, right=0.9, bottom=0.15, top=0.9)
        self.axes = fig.add_subplot(111)
        self.axes.set_facecolor(bg_color)
        super().__init__(fig)
        self.setParent(parent)
        self._plot_title = plot_title
        self.data_source = data_source # 'a' or 'b'
        self.main_window = main_window # Store reference to MainWindow
        self.plot() # Initial plot (likely empty)

    def plot(self):
        self.axes.clear()
        bg_color = self.figure.patch.get_facecolor()
        self.axes.set_facecolor(bg_color)

        # Get data from stored main_window reference
        if not self.main_window:
             data = []
             timestamps = []
        else:
            timestamps = list(self.main_window.timestamps)
            if self.data_source == 'a':
                data = list(self.main_window.sensor_a_data)
            elif self.data_source == 'b':
                data = list(self.main_window.sensor_b_data)
            else:
                data = [] # No data if source not specified

        if timestamps and data:
            # Convert datetime objects to numerical format for plotting if needed
            # For simplicity, using indices if timestamps are regular, otherwise convert properly
            # Example using indices:
            x_values = range(len(timestamps))
            # Filter out NaNs for plotting
            valid_indices = [i for i, y in enumerate(data) if not np.isnan(y)]
            if valid_indices:
                x_plot = [x_values[i] for i in valid_indices]
                y_plot = [data[i] for i in valid_indices]
                self.axes.plot(x_plot, y_plot, marker='.', linestyle='-') # Plot valid data
            # Optionally set x-axis labels to timestamps later if needed

        self.axes.set_title(self._plot_title, fontsize=10)
        self.axes.set_xlabel('Time (Index)', fontsize=8) # Changed label
        self.axes.set_ylabel('Value', fontsize=8)
        self.axes.tick_params(axis='both', which='major', labelsize=7)
        self.axes.grid(True, linestyle='--', alpha=0.6) # Add grid
        self.draw()
# --- End of modified class ---


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    from main_window import MainWindow # Import the main window class

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())