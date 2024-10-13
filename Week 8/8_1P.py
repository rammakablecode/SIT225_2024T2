import time
import requests
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import csv
from datetime import datetime
# Arduino Cloud API Information
THING_ID = 'your_thing_id'
DEVICE_ID = 'your_device_id'
TOKEN = 'your_auth_token'
# Initialize variables for accelerometer data
x_data = []
y_data = []
z_data = []
timestamps = []
# Initialize Dash app
app = Dash(__name__)
# Layout of the dashboard
app.layout = html.Div([
 html.H1("Accelerometer Data Visualization"),
 dcc.Graph(id="live-graph"),
 dcc.Interval(
 id='interval-component',
 interval=10000, # Update every 10 seconds
 n_intervals=0
 )
])
# Function to get data from Arduino Cloud
def get_accelerometer_data():
 global x_data, y_data, z_data, timestamps
 url = f"https://api2.arduino.cc/iot/v2/things/{THING_ID}/properties"
 headers = {
 'Authorization': f'Bearer {TOKEN}'
 }
 response = requests.get(url, headers=headers)
 if response.status_code == 200:
 data = response.json()
 # Assuming x, y, and z properties are available
 py_x = data['py_x']
 py_y = data['py_y']
 py_z = data['py_z']

 x_data.append(py_x)
 y_data.append(py_y)
 z_data.append(py_z)
 timestamps.append(datetime.now().strftime('%H:%M:%S'))
 # Save data to CSV
 with open('accelerometer_data.csv', 'a', newline='') as f:
 writer = csv.writer(f)
 writer.writerow([datetime.now(), py_x, py_y, py_z])
# Callback to update graph
@app.callback(
 Output('live-graph', 'figure'),
 [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
 get_accelerometer_data()

 fig = go.Figure()
 fig.add_trace(go.Scatter(x=timestamps, y=x_data, mode='lines+markers', name='X-axis'))
 fig.add_trace(go.Scatter(x=timestamps, y=y_data, mode='lines+markers', name='Y-axis'))
 fig.add_trace(go.Scatter(x=timestamps, y=z_data, mode='lines+markers', name='Z-axis'))
 fig.update_layout(title="Accelerometer Data (X, Y, Z)",
 xaxis_title="Timestamp",
 yaxis_title="Accelerometer Values")

 return fig
if __name__ == '__main__':
 app.run_server(debug=True)