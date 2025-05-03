from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel,
                             QSizePolicy, QGridLayout, QPushButton, QFileDialog)
from PyQt6.QtGui import QPalette
from PyQt6.QtCore import Qt
import numpy as np
import os

# Import the custom plot canvas
from plot_canvas import PlotCanvas
from constants import LIVE_DATA_SOURCES, ARCHIVE_SOURCE_PREFIX

class DataPlotterPage(QWidget):
    """Widget for displaying configurable data plots with Live and Archive modes."""
    MAX_PLOTS = 4

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.current_mode = "Live Data" # Modes: "Live Data", "Archived Data"
        self.loaded_archive_path = None

        # Main layout
        main_page_layout = QVBoxLayout(self)
        main_page_layout.setContentsMargins(10, 10, 10, 10)
        main_page_layout.setSpacing(15)

        # --- Mode Selection and Archive Controls ---
        mode_archive_layout = QHBoxLayout()

        # Mode Selection
        mode_archive_layout.addWidget(QLabel("Data Source Mode:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Live Data", "Archived Data"])
        self.mode_combo.currentTextChanged.connect(self.handle_mode_change)
        mode_archive_layout.addWidget(self.mode_combo)
        mode_archive_layout.addSpacing(20)

        # Archive Controls (initially hidden)
        self.load_archive_button = QPushButton("Load Archive Directory...")
        self.load_archive_button.clicked.connect(self.load_archive_directory)
        self.load_archive_button.hide()
        mode_archive_layout.addWidget(self.load_archive_button)

        self.loaded_archive_label = QLabel("No archive loaded.")
        self.loaded_archive_label.hide()
        mode_archive_layout.addWidget(self.loaded_archive_label)

        self.clear_archive_button = QPushButton("Clear Archive")
        self.clear_archive_button.clicked.connect(self.clear_loaded_archive)
        self.clear_archive_button.hide()
        mode_archive_layout.addWidget(self.clear_archive_button)

        mode_archive_layout.addStretch(1)
        main_page_layout.addLayout(mode_archive_layout)
        # --- End Mode Selection ---

        # --- Plot Count Configuration Row ---
        config_layout = QHBoxLayout()
        config_layout.addWidget(QLabel("Number of Plots:"))
        self.plot_count_combo = QComboBox()
        self.plot_count_combo.addItems([str(i) for i in range(1, self.MAX_PLOTS + 1)])
        self.plot_count_combo.setCurrentIndex(1) # Default to 2 plots
        self.plot_count_combo.currentIndexChanged.connect(self.update_plot_layout)
        config_layout.addWidget(self.plot_count_combo)
        config_layout.addStretch(1)
        main_page_layout.addLayout(config_layout)
        # --- End Plot Count ---

        # --- Plot Area (using QGridLayout) ---
        self.plot_grid_layout = QGridLayout()
        self.plot_grid_layout.setSpacing(10)
        main_page_layout.addLayout(self.plot_grid_layout)
        # --- End Plot Area ---

        self.plot_widgets = []
        self.plot_config_combos = []
        self.plot_containers = []

        self.setup_plots() # Creates widgets
        self.update_source_dropdowns() # Populates dropdowns based on initial mode
        self.update_plot_layout() # Arranges plots

    def handle_mode_change(self, mode_text):
        """Updates UI and plot sources when the mode changes."""
        self.current_mode = mode_text
        is_archive_mode = (self.current_mode == "Archived Data")

        # Show/hide archive controls
        self.load_archive_button.setVisible(is_archive_mode)
        self.loaded_archive_label.setVisible(is_archive_mode)
        self.clear_archive_button.setVisible(is_archive_mode and self.loaded_archive_path is not None)

        # Update plot source options
        self.update_source_dropdowns()
        # Clear plots when mode changes
        self.clear_all_plots()

    def load_archive_directory(self):
        """Opens a dialog to select an archive directory."""
        # Use main_window's archive_dir as the starting point
        start_dir = self.main_window.archive_dir
        selected_dir = QFileDialog.getExistingDirectory(
            self,
            "Select Archive Directory",
            start_dir
        )

        if selected_dir: # Check if a directory was selected
            # Clear cache before loading new archive data
            self.main_window.clear_csv_cache()
            self.loaded_archive_path = selected_dir
            # Display relative path if possible, otherwise full path
            try:
                display_path = os.path.relpath(selected_dir, self.main_window.base_dir)
            except ValueError:
                display_path = selected_dir # On different drives (Windows)
            self.loaded_archive_label.setText(f"Loaded: ...{display_path[-40:]}" if len(display_path) > 40 else f"Loaded: {display_path}")
            self.clear_archive_button.show()
            self.update_source_dropdowns()
            self.clear_all_plots() # Clear plots after loading new source list
        else:
            print("No archive directory selected.")

    def clear_loaded_archive(self):
        """Clears the currently loaded archive path and updates UI."""
        if self.loaded_archive_path:
            print(f"Clearing loaded archive: {self.loaded_archive_path}")
            self.loaded_archive_path = None
            self.loaded_archive_label.setText("No archive loaded.")
            self.clear_archive_button.hide()
            # Clear cache when archive is cleared
            self.main_window.clear_csv_cache()
            self.update_source_dropdowns()
            self.clear_all_plots()

    def update_source_dropdowns(self):
        """Populates the source combo boxes based on the current mode."""
        sources = []
        if self.current_mode == "Live Data":
            sources = list(LIVE_DATA_SOURCES) # Get live sources
        elif self.current_mode == "Archived Data" and self.loaded_archive_path:
            # Get CSV files from the loaded archive directory via main_window
            csv_files = self.main_window.get_csvs_in_archive_dir(self.loaded_archive_path)
            sources = ["None"] + [f"{ARCHIVE_SOURCE_PREFIX}{fname}" for fname in csv_files]
        else: # Archived mode but no directory loaded, or invalid mode
            sources = ["None"]

        # Update all combo boxes
        for combo in self.plot_config_combos:
            current_text = combo.currentText() # Store current selection
            combo.blockSignals(True) # Prevent signals during update
            combo.clear()
            combo.addItems(sources)
            # Try to restore previous selection if it exists in new list
            if current_text in sources:
                combo.setCurrentText(current_text)
            elif sources: # Otherwise select the first item (usually "None")
                 combo.setCurrentIndex(0)
            combo.blockSignals(False)

        # Trigger plot update for any plots whose source might have changed implicitly
        self.update_plots()

    def setup_plots(self):
        """Creates all potential plot widgets, configs, and their containers."""
        bg_color = self.main_window.palette().color(QPalette.ColorRole.Window).name()

        for i in range(self.MAX_PLOTS):
            container = QWidget(self)
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(0,0,0,0)
            self.plot_containers.append(container)

            combo = QComboBox(container)
            # Don't add items here, update_source_dropdowns will do it
            combo.currentIndexChanged.connect(lambda index, plot_index=i: self.change_plot_source(plot_index, index))
            self.plot_config_combos.append(combo)

            canvas = PlotCanvas(container, width=5, height=3.5, plot_title=f"Plot Area {i+1}", bg_color=bg_color, data_key="None", main_window=self.main_window)
            self.plot_widgets.append(canvas)

            config_row = QHBoxLayout()
            config_row.addWidget(QLabel(f"Plot {i+1} Source:", container))
            config_row.addWidget(combo)
            config_row.addStretch(1)
            container_layout.addLayout(config_row)
            container_layout.addWidget(canvas)

            container.hide() # Initially hide all

    def update_plot_layout(self):
        """Shows/hides plots and arranges them in the grid based on selection."""
        num_plots_to_show = int(self.plot_count_combo.currentText())

        # --- Detach and Hide ALL plot containers first ---
        for i in range(self.MAX_PLOTS):
            container = self.plot_containers[i]
            # Remove from layout management (does not delete)
            self.plot_grid_layout.removeWidget(container)
            # Ensure it's hidden
            container.hide()
        # --- End Detach and Hide ---

        # --- Add and Show required plot containers ---
        for i in range(num_plots_to_show):
            container = self.plot_containers[i]

            # Add container to grid based on num_plots_to_show
            if num_plots_to_show == 1:
                self.plot_grid_layout.addWidget(container, 0, 0, 2, 2)
            elif num_plots_to_show == 2:
                self.plot_grid_layout.addWidget(container, 0, i)
            elif num_plots_to_show == 3:
                if i < 2:
                    self.plot_grid_layout.addWidget(container, 0, i)
                else:
                    self.plot_grid_layout.addWidget(container, 1, 0, 1, 2)
            elif num_plots_to_show == 4:
                row = i // 2
                col = i % 2
                self.plot_grid_layout.addWidget(container, row, col)

            # Make the container (and its children) visible
            container.show()
        # --- End Add and Show ---

        # Update plots immediately after layout change
        self.update_plots()

    def change_plot_source(self, plot_index, combo_index):
        """Updates the data source for a specific plot when its combo box changes."""
        if 0 <= plot_index < len(self.plot_widgets):
            selected_source = self.plot_config_combos[plot_index].itemText(combo_index)
            # Pass the archive path if in archive mode
            archive_path = self.loaded_archive_path if self.current_mode == "Archived Data" else None
            self.plot_widgets[plot_index].set_data_key(selected_source, archive_path=archive_path)

    def update_live_plots(self):
        """Called by main_window timer ONLY to update plots showing live data."""
        if self.current_mode == "Live Data":
            self.update_plots() # Just call the regular update

    def update_plots(self):
        """Updates all currently visible plot canvases based on their source."""
        num_plots_to_show = int(self.plot_count_combo.currentText())
        for i in range(num_plots_to_show):
            plot_widget = self.plot_widgets[i]
            current_key = self.plot_config_combos[i].currentText()
            archive_path = self.loaded_archive_path if self.current_mode == "Archived Data" else None

            # Update if key changed OR if it's live data
            if plot_widget.data_key != current_key or self.current_mode == "Live Data":
                 plot_widget.set_data_key(current_key, archive_path=archive_path)

    def clear_all_plots(self):
         """Clears data from all plot canvases."""
         print("Clearing all plots.")
         for i in range(self.MAX_PLOTS):
             # Set data key to None, which should clear the plot via set_data_key -> plot
             self.plot_widgets[i].set_data_key("None")
             # Also reset the combo box if desired
             if self.plot_config_combos[i].count() > 0:
                 self.plot_config_combos[i].setCurrentIndex(0) # Select "None" if available