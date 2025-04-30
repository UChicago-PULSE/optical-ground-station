from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView, QSizePolicy)
from PyQt6.QtGui import QPalette
from PyQt6.QtCore import Qt
import numpy as np

# Import the custom plot canvas
from plot_canvas import PlotCanvas

class DataAnalysisPage(QWidget):
    """Widget for displaying data analysis plots and table."""
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window # Reference to access data

        main_page_layout = QVBoxLayout(self)
        main_page_layout.setContentsMargins(10, 10, 10, 10)
        main_page_layout.setSpacing(15)

        plot_row_layout = QHBoxLayout()
        plot_row_layout.setSpacing(10)
        # Use main_window's palette to get background color
        bg_color = self.main_window.palette().color(QPalette.ColorRole.Window).name()

        # Create plot canvases, passing the main_window reference
        self.plot_canvas1 = PlotCanvas(self, width=5, height=3.5, plot_title="Sensor A", bg_color=bg_color, data_source='a', main_window=self.main_window)
        self.plot_canvas2 = PlotCanvas(self, width=5, height=3.5, plot_title="Sensor B", bg_color=bg_color, data_source='b', main_window=self.main_window)
        plot_row_layout.addWidget(self.plot_canvas1)
        plot_row_layout.addWidget(self.plot_canvas2)

        # --- Analysis Table ---
        self.analysis_table = QTableWidget()
        self.analysis_table.setRowCount(0)
        self.analysis_table.setColumnCount(3)
        self.analysis_table.setHorizontalHeaderLabels(["Time", "Sensor A", "Sensor B"])
        self.analysis_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.analysis_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.analysis_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # --- End Analysis Table ---

        main_page_layout.addStretch(1)
        main_page_layout.addLayout(plot_row_layout, 4)
        main_page_layout.addWidget(self.analysis_table, 4)
        main_page_layout.addStretch(0)

    def update_plots(self):
        """Updates both plot canvases."""
        self.plot_canvas1.plot()
        self.plot_canvas2.plot()

    def update_table(self, max_rows):
        """Updates the analysis table with the latest data."""
        self.analysis_table.setRowCount(0) # Clear existing rows
        timestamps = self.main_window.timestamps
        sensor_a_data = self.main_window.sensor_a_data
        sensor_b_data = self.main_window.sensor_b_data

        num_rows_to_show = min(len(timestamps), max_rows)
        for i in range(num_rows_to_show):
            idx = len(timestamps) - 1 - i
            # Check index bounds just in case deques aren't perfectly aligned momentarily
            if idx < 0 or idx >= len(sensor_a_data) or idx >= len(sensor_b_data):
                continue

            ts = timestamps[idx].strftime("%H:%M:%S.%f")[:-3]
            val_a = f"{sensor_a_data[idx]:.2f}" if not np.isnan(sensor_a_data[idx]) else "-"
            val_b = f"{sensor_b_data[idx]:.2f}" if not np.isnan(sensor_b_data[idx]) else "-"

            self.analysis_table.insertRow(0)
            self.analysis_table.setItem(0, 0, QTableWidgetItem(ts))
            self.analysis_table.setItem(0, 1, QTableWidgetItem(val_a))
            self.analysis_table.setItem(0, 2, QTableWidgetItem(val_b))