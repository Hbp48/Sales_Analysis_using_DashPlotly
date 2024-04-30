import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_table as dt

sales = pd.read_csv('dataset.csv')
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
                       value = 2017,
                       marks = {str(yr): str(yr) for yr in range(2017, 2025)},
                       className = 'dcc_compon'),

        ], className = "one-half column", id = "title2"),
        
        ],id = "header", className = "row flex-display create_container2", style = {"margin-bottom": "25px"}),
    
        html.Div((
            html.Div([
                dt.DataTable(id = 'my_datatable',
                            columns = [{'name': i, 'id': i} for i in
                                        sales.loc[:, ['Last_Day_of_Week','Xerox','Print_BW','Files','Binding']]],
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
        ), className = "row flex-display "),
    ])

@app.callback(
    Output('my_datatable', 'data'),
    [Input('select_year', 'value')])
    # [Input('radio_items', 'value')])
def display_table(select_year):
    data_table = sales[(sales['Year'] == select_year)]
    return data_table.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
