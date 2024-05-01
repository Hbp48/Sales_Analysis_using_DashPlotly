import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import dash_table as dt
import numpy as np

sales = pd.read_csv('./csv_files/Data.csv')
sales['Last_Day_of_Week'] = pd.to_datetime(sales['Last_Day_of_Week'])
sales['Year'] = sales['Last_Day_of_Week'].dt.year

#rohan
sums = sales.sum()
#everything other than the Year and Last_Day_of_Week
sums = sums[[x for x in sums.index if x not in ['Year', 'Last_Day_of_Week']]]
sorted_sums = sums.sort_values(ascending=True)
sorted_sums

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.H3('Sales Scorecard', style = {'margin-bottom': '0px', 'color': 'white'}),
            ])
        ], className = "one-third column", id = "title1"),

        html.Div([
            html.P('Year', className = 'fix_label', style = {'color': 'white'}),
            dcc.Slider(id = 'select_year',
                       included = False,
                       updatemode = 'drag',
                       tooltip = {'always_visible': True},
                       min = 2017,
                       max = 2024,
                       step = 1,
                       value = 2024,
                       marks = {str(yr): str(yr) for yr in range(2017, 2025)},
                       className = 'dcc_compon'),

        ], className = "one-half column", id = "title2"),
        
        ],id = "header", className = "row flex-display create_container2", style = {"margin-bottom": "25px"}),
    
         html.Div([
            dcc.Graph(id = 'donut_chart',
                      config = {'displayModeBar': 'hover'}, style = {'height': '450px'}),

        ], className = 'create_container2 six columns', style = {'height': '500px'}),
         

        html.Div([
                dt.DataTable(id = 'my_datatable',
                            columns = [{'name': i, 'id': i} for i in
                                        sales.loc[:, ['Last_Day_of_Week','Xerox','Print_BW','Files','Binding', 'Print_Colour', 'Colour_Xerox']]],
                            
                            # page_action='native',
                            page_size=20,
                            # editable=False,
                            sort_action = "native",
                            sort_mode = "multi",
                            # column_selectable="single",
                            # fill_width=False,
                            style_table={
                                    "width": "100%",
                                    "height": "100vh"},
                            virtualization = True,
                            style_cell = {'textAlign': 'left',
                                        'min-width': '100px',
                                        'backgroundColor': '#1f2c56',
                                        'color': '#FEFEFE',
                                        'border-bottom': '0.01rem solid #19AAE1',
                                        },
                            style_as_list_view = True,
                            style_header = {
                                'backgroundColor': '#1f2c56',
                                'fontWeight': 'bold',
                                'font': 'Lato, sans-serif',
                                'color': 'orange',
                                'border': '#1f2c56',
                            },
                            style_data = {'textOverflow': 'hidden', 'color': 'white'},
                            fixed_rows = {'headers': True},
                            )

            ], className = 'create_container2 seven columns'),
#rohan starts
            html.Div(children=[
                html.H1(children='Summary', style={'textAlign': 'center', 'color': '#fff', 'font-size': 24}),

                dcc.Graph(
                    id='summary-bar-graph',
                    figure=px.bar(
                        x=sorted_sums.values,
                        y=sorted_sums.index,
                        orientation='h',
                        labels={'x': 'Total Counts', 'y': 'Operations'},
                        title='Summary of Operations',
                        barmode='relative',  # Set bar mode to 'relative'
                        opacity=0.6,  # Set opacity for better visualization
                        #difference each x-axis value
                        text=sorted_sums.values,
                        range_x=[0, sorted_sums.max() + 1000],  # Set x-axis range
                    ),
                )
            ], style={'backgroundColor': '#1f2c56', 'color': 'white', 'width' : '45%', 'borderRadius': '10px', 'margin': 'auto', 'padding': '20px', 'marginTop': '20px'}),
#rohan ends
        
       
    ])

       

# Hawaiza Starts
def get_attribute_columns(select_year):
    """Helper function to return attribute columns based on the selected year."""
    if select_year in [2017, 2018, 2019]:
        return ['Xerox', 'Print_BW', 'Files', 'Binding']
    else:
        return ['Xerox', 'Print_BW', 'Files', 'Binding', 'Print_Colour', 'Colour_Xerox']


# DataTable
@app.callback(
    Output('my_datatable', 'data'),
    [Input('select_year', 'value')])
def display_table(select_year):
    data_table = sales[(sales['Year'] == select_year)]
    
    if select_year in [2017, 2018, 2019]:
        data_table = sales[sales['Year'] == select_year].drop(columns=['Print_Colour', 'Colour_Xerox'])
    # print(data_table)
       
    data_records = data_table.to_dict('records')
    return data_records



# Sales by Category
@app.callback(Output('donut_chart', 'figure'),
             [Input('select_year', 'value')])
def update_graph(select_year):

    attribute_columns = get_attribute_columns(select_year)
    filtered_sales = sales[(sales['Year'] == select_year)][attribute_columns]

    sales_values = filtered_sales[attribute_columns].sum()

    # Create Pie chart data
    labels = attribute_columns
    values = sales_values.tolist()

    
    colors = ['#30C9C7', '#7A45D1', 'orange','yellow', '#FF474C', '#ADD8E6']

    return {
        'data': [go.Pie(
            labels=labels,
            values=sales_values,
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label+value',
            textfont=dict(size=13),
            texttemplate='%{label} <br>₹%{value:,.2f}',
            textposition='auto',
            hole=0.5,
            rotation=200,
            insidetextorientation='radial'
        )],

        'layout': go.Layout(
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            hovermode='x',
            title={
                'text': f'Sales by Attributes in Year {select_year}',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            titlefont={
                'color': 'white',
                'size': 15
            },
            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center',
                'x': 0.5,
                'y': -0.15
            },
            font=dict(
                family="sans-serif",
                size=12,
                color='white'
            )
        )
    }
# Hawaiza ends


saels1 = pd.read_csv('csv_files\data_2017_monthly.csv')
#app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
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

if __name__ == '__main__':
    app.run_server(debug=True)
