from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from constants import ARCHIVE_SOURCE_PREFIX
# --- Import Qt key constants ---
from PyQt6.QtCore import Qt
# --- End import ---

class PlotCanvas(FigureCanvas):
    """A custom Matplotlib canvas widget for plotting data with keyboard navigation."""
    def __init__(self, parent=None, width=5, height=3.5, dpi=100, plot_title='Plot', bg_color='#F0F0F0', data_key="None", main_window=None):
        # ... (existing __init__ code remains the same) ...
        super().__init__(fig)
        self.setParent(parent)
        self._plot_title = plot_title
        self.data_key = data_key
        self.main_window = main_window
        self.current_archive_path = None
        self.plot()

        # --- Enable keyboard focus ---
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # --- End enable focus ---

    # ... (set_data_key, set_plot_title remain the same) ...

    def plot(self):
        # --- Store original limits before clearing ---
        # Store only if axes already have data and valid limits
        xlim = None
        ylim = None
        if self.axes.has_data():
            try:
                xlim = self.axes.get_xlim()
                ylim = self.axes.get_ylim()
            except Exception: # Catch potential errors if limits are invalid initially
                pass
        # --- End store limits ---

        self.axes.clear()
        bg_color = self.figure.patch.get_facecolor()
        self.axes.set_facecolor(bg_color)

        # ... (existing data fetching logic: get_plot_data) ...

        is_archive_source = self.data_key.startswith(ARCHIVE_SOURCE_PREFIX)

        if timestamps and data:
            valid_indices = [i for i, y in enumerate(data) if pd.notna(y) and pd.notna(timestamps[i])]
            if valid_indices:
                x_plot = [timestamps[i] for i in valid_indices]
                y_plot = [data[i] for i in valid_indices]
                self.axes.plot(x_plot, y_plot, marker='.', linestyle='-')
                self.figure.autofmt_xdate()
                self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M:%S'))

                # --- Restore limits if they were stored ---
                if xlim is not None and ylim is not None:
                    try:
                        self.axes.set_xlim(xlim)
                        self.axes.set_ylim(ylim)
                    except Exception:
                        # If restoring fails (e.g., limits became invalid), let Matplotlib autoscale
                        pass
                # --- End restore limits ---

            else:
                 self.axes.text(0.5, 0.5, 'No valid data points', ...)
        elif self.data_key != "None":
             self.axes.text(0.5, 0.5, 'No data loaded or available', ...)

        # ... (existing title, labels, grid setup) ...
        self.draw()

    # --- Add keyPressEvent handler ---
    def keyPressEvent(self, event):
        """Handle keyboard navigation: Zoom (Up/Down), Pan (Left/Right)."""
        key = event.key()
        ax = self.axes

        # Define zoom factor and pan step (adjust as needed)
        zoom_factor = 0.1 # 10% zoom in/out
        pan_factor = 0.1 # Pan by 10% of the current view width/height

        try:
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            x_range = cur_xlim[1] - cur_xlim[0]
            y_range = cur_ylim[1] - cur_ylim[0]

            if key == Qt.Key.Key_Up: # Zoom In (Y-axis)
                new_ymin = cur_ylim[0] + y_range * zoom_factor / 2
                new_ymax = cur_ylim[1] - y_range * zoom_factor / 2
                if new_ymax > new_ymin: # Prevent limits inversion
                    ax.set_ylim(new_ymin, new_ymax)
            elif key == Qt.Key.Key_Down: # Zoom Out (Y-axis)
                new_ymin = cur_ylim[0] - y_range * zoom_factor / 2
                new_ymax = cur_ylim[1] + y_range * zoom_factor / 2
                ax.set_ylim(new_ymin, new_ymax)
            elif key == Qt.Key.Key_Left: # Pan Left (X-axis)
                pan_step = x_range * pan_factor
                ax.set_xlim(cur_xlim[0] - pan_step, cur_xlim[1] - pan_step)
            elif key == Qt.Key.Key_Right: # Pan Right (X-axis)
                pan_step = x_range * pan_factor
                ax.set_xlim(cur_xlim[0] + pan_step, cur_xlim[1] + pan_step)
            # --- Add X-axis zoom (Optional, e.g., using Shift + Up/Down) ---
            # elif key == Qt.Key.Key_Up and event.modifiers() & Qt.KeyboardModifier.ShiftModifier: # Zoom In (X-axis)
            #     new_xmin = cur_xlim[0] + x_range * zoom_factor / 2
            #     new_xmax = cur_xlim[1] - x_range * zoom_factor / 2
            #     if new_xmax > new_xmin:
            #         ax.set_xlim(new_xmin, new_xmax)
            # elif key == Qt.Key.Key_Down and event.modifiers() & Qt.KeyboardModifier.ShiftModifier: # Zoom Out (X-axis)
            #     new_xmin = cur_xlim[0] - x_range * zoom_factor / 2
            #     new_xmax = cur_xlim[1] + x_range * zoom_factor / 2
            #     ax.set_xlim(new_xmin, new_xmax)
            # --- End X-axis zoom ---
            else:
                # If not one of our keys, pass the event to the parent
                super().keyPressEvent(event)
                return # Don't redraw if we didn't handle it

            # Redraw the canvas to show the changes
            self.draw()

        except Exception as e:
            print(f"Error during plot navigation: {e}")
            # Pass event up if error occurs during limit calculation
            super().keyPressEvent(event)
    # --- End keyPressEvent handler ---

    def set_data_key(self, data_key, archive_path=None):
        """Sets the data source key and optional archive path, triggers a replot."""
        self.data_key = data_key
        self.current_archive_path = archive_path  # Store path used for this key
        self.plot()

    def set_plot_title(self, title):
        """Sets the base plot title."""
        self._plot_title = title

    def plot(self):
        """Clears and redraws the plot based on data from the main window using data_key and archive_path."""
        self.axes.clear()
        bg_color = self.figure.patch.get_facecolor()
        self.axes.set_facecolor(bg_color)

        data = []
        timestamps = []
        if self.main_window:
            timestamps, data = self.main_window.get_plot_data(self.data_key, archive_base_path=self.current_archive_path)

        is_archive_source = self.data_key.startswith(ARCHIVE_SOURCE_PREFIX)

        if timestamps and data:
            valid_indices = [i for i, y in enumerate(data) if pd.notna(y) and pd.notna(timestamps[i])]
            if valid_indices:
                x_plot = [timestamps[i] for i in valid_indices]
                y_plot = [data[i] for i in valid_indices]
                self.axes.plot(x_plot, y_plot, marker='.', linestyle='-')
                self.figure.autofmt_xdate()
                self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M:%S'))  # Multi-line format
            else:
                self.axes.text(0.5, 0.5, 'No valid data points', horizontalalignment='center', verticalalignment='center', transform=self.axes.transAxes)
        elif self.data_key != "None":
            self.axes.text(0.5, 0.5, 'No data loaded or available', horizontalalignment='center', verticalalignment='center', transform=self.axes.transAxes)

        title = self._plot_title
        source_name = self.data_key
        if is_archive_source:
            source_name = self.data_key[len(ARCHIVE_SOURCE_PREFIX):]
            title = f"{title}: {source_name} (Archive)"  # Indicate Archive source
        elif self.data_key != "None":
            title = f"{title}: {source_name} (Live)"  # Indicate Live source

        self.axes.set_title(title, fontsize=10)
        self.axes.set_xlabel('Time', fontsize=8)
        self.axes.set_ylabel('Value', fontsize=8)
        self.axes.tick_params(axis='both', which='major', labelsize=7)
        self.axes.grid(True, linestyle='--', alpha=0.6)
        self.draw()