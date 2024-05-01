import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_table as dt

sales = pd.read_csv('./csv_files/Data.csv')
sales['Last_Day_of_Week'] = pd.to_datetime(sales['Last_Day_of_Week'])
sales['Year'] = sales['Last_Day_of_Week'].dt.year

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
       
        
       
    ])



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

if __name__ == '__main__':
    app.run_server(debug=True)
