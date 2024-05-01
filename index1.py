import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_table as dt
import plotly.express as px

sales = pd.read_csv('./csv_files/Data.csv')
sales['Last_Day_of_Week'] = pd.to_datetime(sales['Last_Day_of_Week'], format='%d-%m-%Y')
sales['Year'] = sales['Last_Day_of_Week'].dt.year
#Harsh
tsales = pd.read_csv('csv_files/Data.csv')
tsales['Sales'] = tsales['Xerox'] + tsales['Print_BW'] + tsales['Files'] + tsales['Binding'] + tsales['Print_Colour'] + tsales['Colour_Xerox']
# Convert 'Last_Day_of_Week' column to datetime format
tsales['Last_Day_of_Week'] = pd.to_datetime(tsales['Last_Day_of_Week'], format='%d-%m-%Y')

# Resample data to monthly
monthly_data = tsales.resample('M', on='Last_Day_of_Week').sum()

# Resample data to yearly for Sales column
yearly_data = tsales.resample('Y', on='Last_Day_of_Week', closed='right', label='right').sum()
yearly_data.index = yearly_data.index.year

#rohan
sums = sales.sum(numeric_only=True)
#everything other than the Year and Last_Day_of_Week
filtered_sums = sums[~sums.index.isin(['Year', 'Last_Day_of_Week'])]
# Sort filtered sums in ascending order
sorted_sums = filtered_sums.sort_values(ascending=True)

# Print the sorted sums
print(sorted_sums)
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
    # Hawaiza's code
    html.Div([
        dcc.Graph(id='donut_chart',
                  config={'displayModeBar': 'hover'},
                  style={'height': '450px'}),
    ], className='create_container2 six columns', style={'height': '550px'}),
    

    

    # Rohan's code
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
                barmode='relative',
                opacity=0.6,
                text=sorted_sums.values,
                range_x=[0, sorted_sums.max() + 1000],
            )
        )
    ], style={'backgroundColor': '#1f2c56', 'color': 'black', 'width': '45%', 'borderRadius': '10px', 'margin': 'auto', 'padding': '20px', 'marginTop': '20px', 'height': "500px"}),
], className='row', style={
        'display': 'flex',
        'flex-wrap': 'wrap',
}),  


#harsh layout 
html.Div([ 

html.Div([ 
    html.H1("   ", style={'textAlign': 'center', 'color': '#fff', 'font-size': 24}),
    html.H1("Time Series Analysis", style={'textAlign': 'center', 'color': '#fff', 'font-size': 24}),
    dcc.Graph(id='line_chart0')
]),
     
html.Div([
    dcc.Dropdown(
        id='select_year',
        options=[{'label': str(year), 'value': year} for year in tsales['Last_Day_of_Week'].dt.year.unique()],
        value=tsales['Last_Day_of_Week'].dt.year.min(),  # Default to the minimum year
        placeholder="Select a Year",
        style={'width': '50%'}
    ),
    dcc.Dropdown(
        id='select_column',
        options=[{'label': col, 'value': col} for col in tsales.columns[1:]],  # Exclude the first column (Date)
        value='Xerox',  # Default to 'Xerox'
        placeholder="Select a Column",
        style={'width': '50%'}
    ),
    dcc.Graph(id='line_chart1'),
     
]), ]),

#harsh end

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

# write a callback to update the bar graph
@app.callback(
    Output('summary-bar-graph', 'figure'),
    [Input('select_year', 'value')]
)
def update_bar_graph(select_year):
    attribute_columns = get_attribute_columns(select_year)
    filtered_sales = sales[(sales['Year'] == select_year)][attribute_columns]
    sales_values = filtered_sales[attribute_columns].sum()
    sorted_sales_values = sales_values.sort_values(ascending=True)
    return px.bar(
        x=sorted_sales_values.values,
        y=sorted_sales_values.index,
        orientation='h',
        labels={'x': 'Total Counts', 'y': 'Operations'},
        title='Summary of Operations',
        barmode='relative',
        opacity=0.6,
        text=sorted_sales_values.values,
        range_x=[0, sorted_sales_values.max() + 1000],
    )

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

#harsh's line charts

@app.callback(
    Output('line_chart0', 'figure'),
    [Input('line_chart0', 'id')]
)
def update_graph(_):
    # Create trace for Sales column
    
    trace = go.Scatter(
        
        x=yearly_data.index,
        y=yearly_data['Sales'],
        name='Sales',
        mode='lines+markers',
        marker=dict(size=8),
        line=dict(width=2),
        hoverinfo='x+y',
        hoverlabel=dict(font=dict(size=12))
    )
    
    # Update layout
    layout = go.Layout(
        title='Yearly Sales Trend',
        xaxis=dict(title='Year'),
        yaxis=dict(title='Sales'),
        hovermode='closest',
        plot_bgcolor='#1f2c56',
        paper_bgcolor='#1f2c56',
        font=dict(color='white')
    )

    return {'data': [trace], 'layout': layout}

@app.callback(
    Output('line_chart1', 'figure'),
    [Input('select_year', 'value'),
     Input('select_column', 'value')]
)
def update_graph(selected_year, selected_column):
    # Filter data for selected year
    year_data = monthly_data[monthly_data.index.year == selected_year]
    
    # Create traces for the selected column and total sales
    traces = []
    for col in [selected_column, 'Sales']:
        trace = go.Scatter(
            x=year_data.index,
            y=year_data[col],
            name=col,
            mode='lines+markers',
            marker=dict(size=8),
            line=dict(width=2),
            hoverinfo='x+y',
            hoverlabel=dict(font=dict(size=12))
        )
        traces.append(trace)

    # Update layout
    layout = go.Layout(
        title=f'Sales Trend for {selected_column} in {selected_year}',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Sales'),
        hovermode='closest',
        plot_bgcolor='#1f2c56',
        paper_bgcolor='#1f2c56',
        font=dict(color='white')
    )

    return {'data': traces, 'layout': layout}

print(yearly_data)

if __name__ == '__main__':
    app.run_server(debug=True)
