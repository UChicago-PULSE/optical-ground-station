from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class PlotCanvas(FigureCanvas):
    """A custom Matplotlib canvas widget for plotting data."""
    def __init__(self, parent=None, width=5, height=3.5, dpi=100, plot_title='Sample Plot', bg_color='#F0F0F0', data_source=None, main_window=None):
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
        """Clears and redraws the plot based on data from the main window."""
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
            # Example using indices:
            x_values = range(len(timestamps))
            # Filter out NaNs for plotting
            valid_indices = [i for i, y in enumerate(data) if not np.isnan(y)]
            if valid_indices:
                x_plot = [x_values[i] for i in valid_indices]
                y_plot = [data[i] for i in valid_indices]
                self.axes.plot(x_plot, y_plot, marker='.', linestyle='-') # Plot valid data

        self.axes.set_title(self._plot_title, fontsize=10)
        self.axes.set_xlabel('Time (Index)', fontsize=8)
        self.axes.set_ylabel('Value', fontsize=8)
        self.axes.tick_params(axis='both', which='major', labelsize=7)
        self.axes.grid(True, linestyle='--', alpha=0.6)
        self.draw()