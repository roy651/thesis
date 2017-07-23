import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import plotly.graph_objs as go
import pandas as pd
import logging
import random as ran
from flask import Flask, render_template, request, jsonify
import locale

# server = Flask(__name__)
# app = dash.Dash(__name__, server=server)
app = dash.Dash()

my_css_url = "https://ds-ra-viz.eu-gb.mybluemix.net/my.css"
app.css.append_css({
    "external_url": my_css_url
})

df = pd.read_csv('1.csv')
available_indicators = pd.read_csv('indicators.csv')

app.layout = html.Div([
    html.H1('NBA Stats', id="page_header"),
    html.H2('An interactive visualization exploring correlation between various factors influencing the NBA\'s teams success'),
    html.H4('Select from the left spinner the desired X axis metric and from the right spinner the Y axis metric. Select a year from the timeline slider and observe the scatter plot. Hovering over the balloons in the plot highlights the team\'s name and its respective X and Y values. Hovering also allows drilling down into a detailed timeline of the specific team for the selected X and Y metrics.'),
    # html.H4('At the bottom, there are a number of preset buttons setting the charts to several chosen setups allowing a story like view of the data.'),

    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': j, 'value': i} for i,j in available_indicators.itertuples(index=False)],
                value='Regular Season Rank'
            )
        ], style={'width': '49%', 'display': 'inline-block'}),


        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': j, 'value': i} for i,j in available_indicators.itertuples(index=False)],
                value='Final Rank'
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),

        html.Label('Choose Year:'),

        html.Div(dcc.Slider(
            id='crossfilter-year--slider',
            min=df['Year'].min(),
            max=df['Year'].max(),
            value=df['Year'].max(),
            step=None,
            marks={str(year): str(year) for year in df['Year'].unique()}
        ), style={'padding': '0px 20px 20px 20px'}),

        dcc.Checklist(
            id='my-dropdown',
                options=[
                    {'label': 'Size As Budget', 'value': 'True'}
                ],
                values=['True'],
                labelStyle={'display': 'inline-block'}
        ),
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Golden State Warriors'}]},
        )
    ], style={'padding': '0 20'}),

    html.Hr(style={'border-width': '3px'}),

    html.Div([
        dcc.Graph(id='x-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div([
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%', 'float': 'right'}),

    # html.Button(children=['Preset 1'], type='submit', id='preset1')

])

# @app.callback(Output('page_header', 'children'),
#     [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData')],
#     events=[Event('preset1', 'click')])
# def preset1Click(hoverData):
#     team_name = hoverData['points'][0]['customdata']
#     dff = df[df['Team'] == team_name]
#     dff = dff[dff['Indicator Name'] == 'SRS']
#     title = '<b>{}</b><br>{}'.format(team_name, 'SRS')
#     return create_time_series(dff, title)

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value'),
     dash.dependencies.Input('my-dropdown', 'values')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value,checkVal):
    dff = df[df['Year'] == year_value]
    dffc = dff[dff['Indicator Name'] == 'Conference']
    print(checkVal)
    print(len(checkVal))
    size = 20
    tooltipText = 'Team: ' + dff[dff['Indicator Name'] == yaxis_column_name]['Team'] +"<br>"+ str(yaxis_column_name) + ': ' +(dff[dff['Indicator Name'] == yaxis_column_name][yaxis_column_name] ).astype(str)+"<br>"+ str(xaxis_column_name) + ': '+(dff[dff['Indicator Name'] == yaxis_column_name][xaxis_column_name] ).astype(str)
    if (len(checkVal) == 1):
        size = (dff[dff['Indicator Name'] == yaxis_column_name]['Budget'] /2000000).astype(str)
        tooltipText = 'Team: ' + dff[dff['Indicator Name'] == yaxis_column_name]['Team'] +"<br>"+ str(yaxis_column_name) + ': ' +(dff[dff['Indicator Name'] == yaxis_column_name][yaxis_column_name] ).astype(str)+"<br>"+ str(xaxis_column_name) + ': '+(dff[dff['Indicator Name'] == yaxis_column_name][xaxis_column_name] ).astype(str)  +'<br>'+'budget: $'+((dff[dff['Indicator Name'] == yaxis_column_name]['Budget'] /1000000).astype(str)) +'M'
    testme='Age'
    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            #text=dff[dff['Indicator Name'] == yaxis_column_name]['Team'],
            customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Team'],
            mode='markers',
            text=tooltipText,#intWithCommas((dff[dff['Indicator Name'] == yaxis_column_name]['Budget'] ).astype(str)),#(dff[dff['Indicator Name'] == yaxis_column_name]['Budget'] ).astype(str),
            # +"<br>"+ ' Rank in League: ' + dff[dff['Indicator Name'] == 'League Rank']['Value'] +"<br>" +' Rank in League: ' + dff[dff['Indicator Name'] == 'Final Rank']['Value'],
            hoverinfo='text',
            marker={
                #str((dff[dff['Indicator Name'] == 'W']['Value'])) ,
                'opacity': 0.5,
                'line': {'width': 3, 'color': dff[dff['Indicator Name'] == 'Secondary Color']['Value']},
                'color': dff[dff['Indicator Name'] == 'Primary Color']['Value'],
                'size': size

            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=400,
            hovermode='closest',
            legend={'x': 1, 'y': 1}
        )
    }

def create_time_series(dff, title):
    return {
        'data': [go.Scatter(
            x=dff['Year'],
            y=dff['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': False}
        }
    }

@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name):
    team_name = hoverData['points'][0]['customdata']
    dff = df[df['Team'] == team_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(team_name, xaxis_column_name)
    return create_time_series(dff, title)

@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name):
    dff = df[df['Team'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, yaxis_column_name)

port = int(os.getenv('PORT', 8080))

if __name__ == '__main__':
    app.run_server()
    # server.run(host='0.0.0.0', port=port, debug=True)
