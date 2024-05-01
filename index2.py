import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Assuming you have a Dash app instance named app
saels1 = pd.read_csv('csv_files\data_2017_monthly.csv')
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
@app.callback(
    Output('line_chart', 'figure'),
    [Input('radio_items', 'value')])
def update_graph(radio_item):
    # Extract the selected column based on radio item
    y_column = saels1[radio_item]
    
    return {
        'data': [
            go.Scatter(
                x=saels1['Month'],
                y=y_column,
                name=radio_item,
                mode='lines+markers',
                marker=dict(size=8),
                line=dict(width=2),
                hoverinfo='x+y',
                hoverlabel=dict(font=dict(size=12))
            )
        ],
        'layout': go.Layout(
            title='Sales Trend for {}'.format(radio_item),
            xaxis=dict(title='Month'),
            yaxis=dict(title='Sales'),
            hovermode='closest',
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            font=dict(color='white')
        )
    }

# Layout of your Dash app
app.layout = html.Div([
    dcc.RadioItems(
        id='radio_items',
        options=[
            {'label': 'Xerox', 'value': 'Xerox'},
            {'label': 'Print_BW', 'value': 'Print_BW'},
            {'label': 'Files', 'value': 'Files'},
            {'label': 'Binding', 'value': 'Binding'}
        ],
        value='Xerox',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id='line_chart')
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)