# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                    html.Div([
                                        dcc.Dropdown(id='site-dropdown', 
                                                options=[
                                                        {'label': 'All Sites', 'value': 'ALL'},
                                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                                        ],
                                                value='ALL',
                                                placeholder='Select a Launch Site here',
                                                #searchable=True,
                                                style={'width':'100%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}),
                                    ]),
                                html.Br(),


                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                #html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Div([ ], id='success-pie-chart'),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(0, 10000, value=[0, 10000], id='payload-slider'),
                                html.Div(id='output-container-range-slider'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Br(),
                                html.Div([ ], id='success-payload-scatter-chart'),
                                #html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback([Output(component_id='success-pie-chart', component_property='children')],
                [Input(component_id='site-dropdown', component_property='value')])
def get_graph(site):
    if site == 'ALL':
        df = spacex_df.groupby('class').count().reset_index()
        pie_fig = px.pie(df, values='Launch Site', names='class', title='Succes pie chart')
    else:
        df = spacex_df[spacex_df['Launch Site']==site]
        df = df.groupby('class').count().reset_index()
        pie_fig = px.pie(df, values='Launch Site', names='class', title='Succes pie chart')
    return [dcc.Graph(figure=pie_fig)]
#Add payload-slider callback
@app.callback(
    Output('output-container-range-slider', 'children'),
    [Input('payload-slider', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    [Output(component_id='success-payload-scatter-chart', component_property='children')],
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')])
def get_graph_2(site, payload):
    if site == 'ALL':
        mask = (spacex_df['Payload Mass (kg)']>=payload[0]) & (spacex_df['Payload Mass (kg)']<=payload[1]) 
        df = spacex_df[mask]
    else:
        mask = (spacex_df['Launch Site']==site) & (spacex_df['Payload Mass (kg)']>=payload[0]) & (spacex_df['Payload Mass (kg)']<=payload[1]) 
        df = spacex_df[mask]
    df = df[['class', 'Payload Mass (kg)']]
    sct_fig = px.scatter(df, x='Payload Mass (kg)', y='class', title='Succes payload scatter chart')
    return [dcc.Graph(figure=sct_fig)]

# Run the app

if __name__ == '__main__':
    app.run_server()
