import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output
import plotly.express as px

import plotly.graph_objects as go # or plotly.express as px
fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)

def make_graph_from_adjacency_list(data):
	# data is a huge json dict
	# you have to filter out redundancies, and make the final graph out of it
	edges = []
	# convert data into graph elements
	for key in data.keys():
		for node in data[key]:
			edges.append([key, node])


	for edge in edges:
		print(edge)