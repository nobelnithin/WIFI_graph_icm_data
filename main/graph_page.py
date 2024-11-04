import sys
import requests
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg
from PyQt5.QtCore import QTimer

class RealTimeGraph(QMainWindow):
    def __init__(self):
        super().__init__()

        # ESP32 URL (replace with the actual IP address of your ESP32)
        self.esp_url = 'http://192.168.4.1/'

        # Set up the plot widget
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.graphWidget.setTitle("Real-Time Sensor Data")
        self.graphWidget.setLabel('left', 'Value')
        self.graphWidget.setLabel('bottom', 'Time (s)')

        # Initialize data storage
        self.data = []  # Stores sensor values
        self.time_data = []  # Stores corresponding time values
        self.start_time = time.time()  # Record the initial time

        self.max_points = 100  # Maximum number of points to show on the graph

        # Set up a timer for real-time updating
        self.timer = QTimer()
        self.timer.setInterval(100)  # Interval in milliseconds (adjust as needed)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
        
    def update_plot(self):
        try:
            # Fetch data from ESP32
            response = requests.get(self.esp_url)
            response.raise_for_status()  # Check for HTTP errors
            
            # Convert response from string to float
            value = float(response.text.strip())  # Convert to float

            # Append the new data point and its time
            current_time = time.time() - self.start_time  # Elapsed time since start
            self.data.append(value)
            self.time_data.append(current_time)

            # Keep only the last `max_points` number of points
            if len(self.data) > self.max_points:
                self.data.pop(0)
                self.time_data.pop(0)

            # Update the plot with time and data arrays
            self.graphWidget.clear()
            self.graphWidget.plot(self.time_data, self.data, pen=pg.mkPen('b', width=2))

        except (requests.RequestException, ValueError) as e:
            print(f"Error fetching or parsing data: {e}")  # Handle request errors or parsing issues

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = RealTimeGraph()
    mainWin.show()
    sys.exit(app.exec_())
