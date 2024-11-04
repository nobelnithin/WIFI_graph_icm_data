# import sys
# import requests
# import time
# from PyQt5.QtWidgets import QApplication, QMainWindow
# import pyqtgraph as pg
# from PyQt5.QtCore import QTimer

# class RealTimeGraph(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # ESP32 URL (replace with the actual IP address of your ESP32)
#         self.esp_url = 'http://192.168.4.1/'

#         # Set up the plot widget
#         self.graphWidget = pg.PlotWidget()
#         self.setCentralWidget(self.graphWidget)
#         self.graphWidget.setTitle("Real-Time Sensor Data")
#         self.graphWidget.setLabel('left', 'Value')
#         self.graphWidget.setLabel('bottom', 'Time (s)')

#         # Initialize data storage
#         self.data1 = []  # Stores first sensor value
#         self.data2 = []  # Stores second sensor value
#         self.time_data = []  # Stores corresponding time values
#         self.start_time = time.time()  # Record the initial time

#         self.max_points = 100  # Maximum number of points to show on the graph

#         # Set up a timer for real-time updating
#         self.timer = QTimer()
#         self.timer.setInterval(100)  # Interval in milliseconds (adjust as needed)
#         self.timer.timeout.connect(self.update_plot)
#         self.timer.start()

#     def update_plot(self):
#         try:
#             # Fetch data from ESP32
#             response = requests.get(self.esp_url)
#             response.raise_for_status()  # Check for HTTP errors

#             # Split response into two float values
#             values = response.text.strip().split(',')
#             if len(values) == 2:
#                 value1 = float(values[0])
#                 value2 = float(values[1])

#                 # Append the new data points and their time
#                 current_time = time.time() - self.start_time  # Elapsed time since start
#                 self.data1.append(value1)
#                 self.data2.append(value2)
#                 self.time_data.append(current_time)

#                 # Keep only the last `max_points` number of points
#                 if len(self.data1) > self.max_points:
#                     self.data1.pop(0)
#                     self.data2.pop(0)
#                     self.time_data.pop(0)

#                 # Update the plot with time and data arrays
#                 self.graphWidget.clear()
#                 self.graphWidget.plot(self.time_data, self.data1, pen=pg.mkPen('b', width=2), name='Sensor 1')
#                 self.graphWidget.plot(self.time_data, self.data2, pen=pg.mkPen('r', width=2), name='Sensor 2')

#         except (requests.RequestException, ValueError) as e:
#             print(f"Error fetching or parsing data: {e}")  # Handle request errors or parsing issues

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     mainWin = RealTimeGraph()
#     mainWin.show()
#     sys.exit(app.exec_())


import sys
import requests
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton
import pyqtgraph as pg
from PyQt5.QtCore import QTimer

class RealTimeGraph(QMainWindow):
    def __init__(self):
        super().__init__()

        # ESP32 URL (replace with the actual IP address of your ESP32)
        self.esp_url = 'http://192.168.4.1/'
        self.esp_url2 = 'http://192.168.4.1/send'

        # Set up the main layout
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

        # Set up the plot widget
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setTitle("Real-Time Sensor Data")
        self.graphWidget.setLabel('left', 'Value')
        self.graphWidget.setLabel('bottom', 'Time (s)')
        self.layout.addWidget(self.graphWidget)

        # Add a type box (input field) and a button
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter a number to send to ESP32")
        self.layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.layout.addWidget(self.send_button)
        self.send_button.clicked.connect(self.send_data_to_esp32)

        # Initialize data storage
        self.data1 = []  # Stores first sensor value
        self.data2 = []  # Stores second sensor value
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

            # Split response into two float values
            values = response.text.strip().split(',')
            if len(values) == 2:
                value1 = float(values[0])
                value2 = float(values[1])

                # Append the new data points and their time
                current_time = time.time() - self.start_time  # Elapsed time since start
                self.data1.append(value1)
                self.data2.append(value2)
                self.time_data.append(current_time)

                # Keep only the last `max_points` number of points
                if len(self.data1) > self.max_points:
                    self.data1.pop(0)
                    self.data2.pop(0)
                    self.time_data.pop(0)

                # Update the plot with time and data arrays
                self.graphWidget.clear()
                self.graphWidget.plot(self.time_data, self.data1, pen=pg.mkPen('b', width=2), name='Sensor 1')
                self.graphWidget.plot(self.time_data, self.data2, pen=pg.mkPen('r', width=2), name='Sensor 2')

        except (requests.RequestException, ValueError) as e:
            print(f"Error fetching or parsing data: {e}")  # Handle request errors or parsing issues

    def send_data_to_esp32(self):
        input_text = self.input_field.text()
        if input_text:
            try:
                # Send data to ESP32 as a GET request with the input as a parameter
                # esp32_url = f'http://192.168.4.1/send?number={number}'
                # response = requests.get(esp32_url)
                esp_url = f'http://192.168.4.1/send?number={input_text}'
                response = requests.get(esp_url)
                response.raise_for_status()  # Check for HTTP errors
                print(f"Data sent to ESP32: {input_text}")
            except requests.RequestException as e:
                print(f"Error sending data to ESP32: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = RealTimeGraph()
    mainWin.show()
    sys.exit(app.exec_())
