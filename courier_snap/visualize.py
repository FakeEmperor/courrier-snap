import os
import json
import numpy as np
import plotly.graph_objects as go
from courier_snap.utils import get_project_path


path_to_data = os.path.join(
    get_project_path(), 'task-data', 'data', 'contest_input.json')
f = open(path_to_data)
json_contents = json.load(f)
print(json_contents)

x_couriers = []
y_couriers = []
x_depots = []
y_depots = []
x_start_order = []
y_start_order = []
x_end_order = []
y_end_order = []

for courier in json_contents['couriers']:
    x_couriers.append(courier['location_x'])
    y_couriers.append(courier['location_y'])

for depot in json_contents['depots']:
    print(depot['location_x'], depot['location_y'])
    x_depots.append(depot['location_x'])
    y_depots.append(depot['location_y'])

for order in json_contents['orders']:
    # print(order)
    x_start_order.append(order['pickup_location_x'])
    y_start_order.append(order['pickup_location_y'])
    x_end_order.append(order['dropoff_location_x'])
    y_end_order.append(order['dropoff_location_y'])


fig = go.Figure()
fig = go.Figure(data=go.Scatter(x=x_couriers, y=y_couriers, mode='markers', name='courier'))
fig.add_trace(go.Scatter(x=x_depots, y=y_depots, mode='markers', name='depots'))
#fig.add_trace(go.Scatter(x=x_start_order, y=y_start_order, mode='markers', name='start_order'))
# fig.add_trace(go.Scatter(x=x_end_order, y=y_end_order, mode='markers', name='end_order'))
# ord_len = len(x_start_order)
# for i in range(ord_len):
#     if i % 10 == 0:
#         print('{}/{}'.format(i, ord_len))
#     fig.add_trace(go.Scatter(x=[x_start_order[i], x_end_order[i]], y=[
#                   y_start_order[i], y_end_order[i]], mode='lines'))
#

fig.show()
