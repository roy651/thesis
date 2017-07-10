import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import logging
import random as ran

app = dash.Dash()

my_css_url = "./my.css"
# app.css.append_css({
#     "external_url": my_css_url
# })

df = pd.read_csv('stats.csv')
available_indicators = pd.read_csv('indicators.csv')

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': j, 'value': i} for i,j in available_indicators.itertuples(index=False)],
                value='Regular Season Rank'
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': j, 'value': i} for i,j in available_indicators.itertuples(index=False)],
                value='Final Rank'
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
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

    html.Div(dcc.Slider(
        id='crossfilter-year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        step=None,
        marks={str(year): str(year) for year in df['Year'].unique()}
    ), style={'padding': '0px 20px 20px 20px'}),

    html.Div([
        dcc.Graph(id='x-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div([
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

])

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    dff = df[df['Year'] == year_value]
    dffc = dff[dff['Indicator Name'] == 'Conference']
    testme='Age'
    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            #text=dff[dff['Indicator Name'] == yaxis_column_name]['Team'],
            customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Team'],
            mode='markers',
            text='Team: ' + dff[dff['Indicator Name'] == yaxis_column_name]['Team'] +"<br>"+ 'Age: ' + (dff[dff['Indicator Name'] == yaxis_column_name]['Age']).astype(str) +"<br>"+ str(yaxis_column_name) + ': ' +(dff[dff['Indicator Name'] == yaxis_column_name][yaxis_column_name]).astype(str),
            # +"<br>"+ ' Rank in League: ' + dff[dff['Indicator Name'] == 'League Rank']['Value'] +"<br>" +' Rank in League: ' + dff[dff['Indicator Name'] == 'Final Rank']['Value'],
            hoverinfo='text',
            marker={
                #str((dff[dff['Indicator Name'] == 'W']['Value'])) ,
                'opacity': 0.5,
                'line': {'width': 3, 'color': dff[dff['Indicator Name'] == 'Secondary Color']['Value']},
                'color': dff[dff['Indicator Name'] == 'Primary Color']['Value'],
                'size': (dff[dff['Indicator Name'] == yaxis_column_name]['SRS'] +20).astype(str)

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
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Team'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, title)

@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name):
    dff = df[df['Team'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, yaxis_column_name)

def rannum(data):
    a = ran.randint(10, 30)
    logging.warning("Value1="+str(dffc['Value']))

    return {
        a
    }

if __name__ == '__main__':
    app.run_server()
