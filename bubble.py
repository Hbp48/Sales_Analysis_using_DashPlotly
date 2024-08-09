import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Assuming you have a Dash app instance named app
sales1 = pd.read_csv('./csv_files/data_2017_monthly.csv')
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

@app.callback(
    Output('bubble_chart', 'figure'),
    [Input('radio_items', 'value')])
def update_graph(radio_item):
    # Extract the selected column based on radio item
    y_column = sales1[radio_item]
    
    return {
        'data': [
            go.Scatter(
                x=sales1['Month'],
                y=y_column,
                mode='markers',
                marker=dict(
                    size=y_column,  # Use sales value for bubble size
                    sizemode='area',
                    sizeref=2. * max(y_column) / (40. ** 2),
                    sizemin=4,
                    color=y_column,  # Color based on sales value
                    colorscale='Viridis',  # Choose colorscale
                    showscale=True,  # Show color scale
                    opacity=0.7
                ),
                text=['Month: {}<br>{}: {}'.format(month, radio_item, value) 
                      for month, value in zip(sales1['Month'], y_column)],
                hoverinfo='text',
                hoverlabel=dict(font=dict(size=12))
            )
        ],
        'layout': go.Layout(
            title='Sales Trend for {}'.format(radio_item),
            xaxis=dict(title='Month'),
            yaxis=dict(title=radio_item),
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
    dcc.Graph(id='bubble_chart')
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
