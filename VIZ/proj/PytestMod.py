import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import random as ran

#df = pd.read_csv(
#    'https://raw.githubusercontent.com/plotly/'
#    'datasets/master/gapminderDataFiveYear.csv')

df = pd.read_csv('test1.csv')

app = dash.Dash()

app.layout = html.Div([  # @UndefinedVariable
    dcc.Graph(id='graph-with-slider', animate=True),  # @UndefinedVariable
    dcc.Slider(  # @UndefinedVariable
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        step=None,
        marks={str(year): str(year) for year in df['year'].unique()}
    )
])

@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    traces = []
    for i in filtered_df.Team.unique():
        df_by_continent = filtered_df[filtered_df['Team'] == i]
        a = df_by_continent['Age']
        #a ='{0:.2f}'.format(a)
        traces.append(go.Scatter(
            x=df_by_continent['L'],
            y=df_by_continent['W'],
            text='Team: ' + df_by_continent['Team']+ '</br>' + ' Age: '+ str(a.tolist()[0]),
            mode='markers',
            hoverinfo='text',
            opacity=0.7,
            marker={
                'size':df_by_continent['AgeSort'],
                'line': {'width': 2, 'color': 'black'}

            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={ 'title': 'Lose'},
            yaxis={'title': 'Win' },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 100, 'y': 1},
            hovermode='closest'
        )
    }

def number_return():
    return {
        ran.randint(10, 30)
    }
    
if __name__ == '__main__':
    app.run_server()
    
    
