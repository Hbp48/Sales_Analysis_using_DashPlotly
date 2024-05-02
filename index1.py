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
# Harsh
tsales = pd.read_csv('csv_files/Data.csv')
tsales['Sales'] = tsales['Xerox'] + tsales['Print_BW'] + tsales['Files'] + tsales['Binding'] + tsales['Print_Colour'] + tsales['Colour_Xerox']
# Convert 'Last_Day_of_Week' column to datetime format
tsales['Last_Day_of_Week'] = pd.to_datetime(tsales['Last_Day_of_Week'], format='%d-%m-%Y')

# Resample data to monthly
monthly_data = tsales.resample('M', on='Last_Day_of_Week').sum()

# Resample data to yearly for Sales column
yearly_data = tsales.resample('Y', on='Last_Day_of_Week', closed='right', label='right').sum()
yearly_data.index = yearly_data.index.year

df17=pd.read_csv('csv_files/Data - 2017.csv')
df18=pd.read_csv('csv_files/Data - 2018.csv')
df19=pd.read_csv('csv_files/Data - 2019.csv')
df22=pd.read_csv('csv_files/Data - 2022.csv')
df23=pd.read_csv('csv_files/Data - 2023.csv')
df24=pd.read_csv('csv_files/Data - 2024.csv')

concatenated_df = pd.concat([df17, df18, df19], ignore_index=False)


# Convert 'Last_Day_of_Week' column to datetime format
concatenated_df['Last_Day_of_Week'] = pd.to_datetime(concatenated_df['Last_Day_of_Week'], format='%Y-%m-%d')

# Resample data to monthly
concatenated_df = concatenated_df.resample('M', on='Last_Day_of_Week').sum()
concatenated_df['Xerox']=concatenated_df['Xerox']*0.5
concatenated_df['Files']=concatenated_df['Files']*15
concatenated_df['Binding']=concatenated_df['Binding']*20
concatenated_df['Revenue']=concatenated_df['Xerox']+concatenated_df['Print_BW']+concatenated_df['Files']+concatenated_df['Binding']

concatenated_df1 = pd.concat([df22, df23], ignore_index=False)


# Convert 'Last_Day_of_Week' column to datetime format
concatenated_df1['Last_Day_of_Week'] = pd.to_datetime(concatenated_df1['Last_Day_of_Week'], format='%Y-%m-%d')

# Resample data to monthly
concatenated_df1 = concatenated_df1.resample('M', on='Last_Day_of_Week').sum()

concatenated_df1['Print_BW']=concatenated_df1['Print_BW']*2
concatenated_df1['Files']=concatenated_df1['Files']*20
concatenated_df1['Binding']=concatenated_df1['Binding']*20
concatenated_df1['Print_Colour']=concatenated_df1['Print_Colour']*5
concatenated_df1['Colour_Xerox']=concatenated_df1['Colour_Xerox']*5


concatenated_df1['Revenue']=concatenated_df1['Xerox']+concatenated_df1['Print_BW']+concatenated_df1['Files']+concatenated_df1['Binding']+(concatenated_df1['Print_Colour']+concatenated_df1['Colour_Xerox'])

df24['Last_Day_of_Week'] = pd.to_datetime(df24['Last_Day_of_Week'], format='%Y-%m-%d')
df24 = df24.resample('M', on='Last_Day_of_Week').sum()

df24['Print_BW']=df24['Print_BW']*2
df24['Files']=df24['Files']*20
df24['Binding']=df24['Binding']*25
df24['Print_Colour']=df24['Print_Colour']*5
df24['Colour_Xerox']=df24['Colour_Xerox']*5


df24['Revenue']=df24['Xerox']+df24['Print_BW']+df24['Files']+df24['Binding']+(df24['Print_Colour']+df24['Colour_Xerox'])

revenue = pd.concat([concatenated_df, concatenated_df1, df24], ignore_index=False)
# Check if 'Last_Day_of_Week' column exists in the revenue DataFrame
#if 'Last_Day_of_Week' in revenue.columns:
#revenue['Last_Day_of_Week'] = pd.to_datetime(revenue['Last_Day_of_Week'])
#revenue.set_index('Last_Day_of_Week', inplace=True)

#else:
print(revenue)

# Assuming revenue is your DataFrame containing the data
#revenue['Last_Day_of_Week'] = pd.to_datetime(revenue['Last_Day_of_Week'])
#revenue.set_index('Last_Day_of_Week', inplace=True)

# Resample the data by year
yrevenue = revenue.resample('Y').sum()
# Convert the index to integers
yrevenue.index = yrevenue.index.year

# Now you can select the row corresponding to the selected year




# Rohan
sums = sales.sum(numeric_only=True)
# Everything other than the Year and Last_Day_of_Week
filtered_sums = sums[~sums.index.isin(['Year', 'Last_Day_of_Week'])]
# Sort filtered sums in ascending order
sorted_sums = filtered_sums.sort_values(ascending=True)

# Attribute prices
attribute_prices = {
    'Xerox': 0.5,
    'Print_BW': 1,
    'Files': 15,
    'Binding': 20,
    'Print_Colour': 5,
    'Colour_Xerox': 5
}

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.Div([
                html.H3('Sales Scorecard', style={'margin-bottom': '0px', 'color': 'white'}),
            ])
        ], className="one-third column", id="title1"),

        html.Div([
            html.P('Year', className='fix_label', style={'color': 'white'}),
            dcc.Slider(
                id='select_year',
                included=False,
                updatemode='drag',
                tooltip={'always_visible': True},
                min=2017,
                max=2024,
                step=1,
                value=2024,
                marks={str(yr): str(yr) for yr in range(2017, 2025)},
                className='dcc_compon'
            ),
        ], className="one-half column", id="title2"),
    ], id="header", className="row flex-display create_container2", style={"margin-bottom": "25px"}),

    # Main content
    html.Div([
        # Sales by Category
        html.Div([
            dcc.Graph(id='donut_chart',
                      config={'displayModeBar': 'hover'},
                      style={'height': '450px'}),
        ], className='create_container2 six columns', style={'height': '550px'}),

        # Summary
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
        ], style={'backgroundColor': '#1f2c56', 'color': 'black', 'width': '45%', 'borderRadius': '10px',
                  'margin': 'auto', 'padding': '20px', 'marginTop': '20px', 'height': "500px"}),

    ], className='row', style={'display': 'flex', 'flex-wrap': 'wrap'}),

    # DataTable
    html.Div([
        dt.DataTable(id='my_datatable',
                     columns=[{'name': i, 'id': i} for i in
                              sales.loc[:, ['Last_Day_of_Week', 'Xerox', 'Print_BW', 'Files', 'Binding',
                                           'Print_Colour', 'Colour_Xerox']]],

                     page_size=20,
                     sort_action="native",
                     sort_mode="multi",
                     style_table={
                         "width": "100%",
                         "height": "100vh"},
                     virtualization=True,
                     style_cell={'textAlign': 'left',
                                 'min-width': '100px',
                                 'backgroundColor': '#1f2c56',
                                 'color': '#FEFEFE',
                                 'border-bottom': '0.01rem solid #19AAE1',
                                 },
                     style_as_list_view=True,
                     style_header={
                         'backgroundColor': '#1f2c56',
                         'fontWeight': 'bold',
                         'font': 'Lato, sans-serif',
                         'color': 'orange',
                         'border': '#1f2c56',

                     },
                     style_data={'textOverflow': 'hidden', 'color': 'white'},
                     fixed_rows={'headers': True},
                     )

    ], className='create_container2 seven columns', style={'width': '96%'}),

    # Harsh layout
    html.Div([
        html.H1("   ", style={'textAlign': 'center', 'color': '#fff', 'font-size': 24}),
        html.H1("Time Series Analysis", style={'textAlign': 'center', 'color': '#fff', 'font-size': 24}),
        dcc.Graph(id='line_chart0')
    ]),

    html.Div([
        html.P('Product', className='fix_label', style={'color': 'white'}),
        dcc.Slider(
            id='select_column',
            min=0,
            max=len(tsales.columns[1:]) - 1,  # adjust max to the length of columns - 1
            step=1,
            value=len(tsales.columns[1:]) - 1,  # set the default value to the maximum index
            marks={i: col for i, col in enumerate(tsales.columns[1:])},  # use index as position and column name as label
            className='dcc_compon'
        ),
        dcc.Graph(id='line_chart1'),
    ], className="one-half column", id="title3", style={'width': '96%'}),

    # Bubble chart
    html.Div([
        dcc.Graph(id='bubble_chart',
                  config={'displayModeBar': 'hover'},
                  style={'height': '450px'}),
    ], className='create_container2 six columns', style={'height': '550px', 'width': '46%'}),

    # Revenue bar chart
    html.Div([
        dcc.Graph(id='revenue_bar_chart',
                  config={'displayModeBar': 'hover'},
                  style={'height': '450px'}),
    ], className='create_container2 six columns', style={'height': '550px', 'width': '50%'}),

    html.Div([
        dcc.Graph(id='revenue_line_chart',
                  config={'displayModeBar': 'hover'},
                  style={'height': '450px'}),
    ], className='create_container2 six columns', style={'height': '550px', 'width': '100%'}),

])


# Helper function to get attribute columns based on the selected year
def get_attribute_columns(select_year):
    if select_year in [2017, 2018, 2019]:
        return ['Xerox', 'Print_BW', 'Files', 'Binding']
    else:
        return ['Xerox', 'Print_BW', 'Files', 'Binding', 'Print_Colour', 'Colour_Xerox']


# DataTable callback
@app.callback(
    Output('my_datatable', 'data'),
    [Input('select_year', 'value')])
def display_table(select_year):
    data_table = sales[(sales['Year'] == select_year)]

    if select_year in [2017, 2018, 2019]:
        data_table = sales[sales['Year'] == select_year].drop(columns=['Print_Colour', 'Colour_Xerox'])
    data_records = data_table.to_dict('records')
    return data_records


# Summary bar graph callback
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

    labels = attribute_columns
    values = sales_values.tolist()

    colors = ['#30C9C7', '#7A45D1', 'orange', 'yellow', '#FF474C', '#ADD8E6']

    # Calculate percentage values
    percentage_values = sales_values / sales_values.sum() * 100

    return {
        'data': [go.Pie(
            labels=labels,
            values=percentage_values,
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label+percent',
            textfont=dict(size=13),
            texttemplate='%{label} <br>%{value:.2f}%)',
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


# Harsh's line charts callback
@app.callback(
    Output('line_chart0', 'figure'),
    [Input('line_chart0', 'id')]
)
def update_graph(_):
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
def update_graph(selected_year, selected_column_index):
    year_data = monthly_data[monthly_data.index.year == selected_year]

    # Get the list of attribute columns
    attribute_columns = get_attribute_columns(selected_year)

    # Convert the selected column index to the corresponding column label
    if selected_column_index < len(attribute_columns):
        selected_column = attribute_columns[selected_column_index]
    else:
        selected_column = 'Sales'  # If the selected index is out of range, default to 'Sales'

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

# Add a new callback for the revenue line chart
@app.callback(
    Output('revenue_line_chart', 'figure'),
    [Input('select_year', 'value')]
)
def update_revenue_line_chart(select_year):
    year_data = revenue.loc[revenue.index.year == select_year]  # Filter by year using index

    trace = go.Scatter(
        x=year_data.index,
        y=year_data['Revenue'],
        mode='lines+markers',
        name='Revenue',
        marker=dict(size=8),
        line=dict(width=2),
        hoverinfo='x+y',
        hoverlabel=dict(font=dict(size=12))
    )

    layout = go.Layout(
        title=f'Revenue Trend in {select_year}',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Revenue'),
        hovermode='closest',
        plot_bgcolor='#1f2c56',
        paper_bgcolor='#1f2c56',
        font=dict(color='white')
    )

    return {'data': [trace], 'layout': layout}

#RIYA
# Bubble chart
@app.callback(Output('bubble_chart', 'figure'),
              [Input('select_year', 'value')])
def update_bubble_chart(select_year):
    # Filter yearly data for the selected year
    filtered_yearly_data = yearly_data[yearly_data.index == select_year]

    # Extract attribute columns and sales data
    attribute_columns = get_attribute_columns(select_year)
    sales_data = filtered_yearly_data['Sales']
    attribute_sales_data = filtered_yearly_data[attribute_columns]

    bubble_data = []
    for col in attribute_columns:
        bubble_data.append(go.Scatter(
            x=[col] * len(attribute_sales_data),  # X-axis represents attributes
            y=attribute_sales_data[col],  # Y-axis represents sales
            mode='markers',
            name=col,
            marker=dict(size=10),
            text=attribute_sales_data.index,
            hoverinfo='text+x+y',
        ))

    layout = go.Layout(
        title=f'Sales vs. Attributes in Year {select_year}',
        xaxis=dict(title='Attributes'),
        yaxis=dict(title='Sales'),
        hovermode='closest',
        plot_bgcolor='#1f2c56',
        paper_bgcolor='#1f2c56',
        font=dict(color='white')
    )

    return {'data': bubble_data, 'layout': layout}

print(yrevenue)

@app.callback(
    Output('revenue_bar_chart', 'figure'),
    [Input('select_year', 'value')]
)
def update_revenue_bar_chart(select_year):
    # Filter the revenue data for the selected year
    year_data = revenue.loc[revenue.index.year == select_year]
    
    # Sum the revenue for each attribute
    total_revenue = year_data.sum()
    
    # Create a bar plot
    fig = go.Figure(data=[go.Bar(
        x=total_revenue.index,
        y=total_revenue.values,
        text=total_revenue.values,
        textposition='auto',
        marker=dict(
            color='orange',
            line=dict(
                color='#1f2c56',
                width=1
            )
        )
    )])
    
    # Update layout
    fig.update_layout(
        title=f'Total Revenue by Attribute in Year {select_year}',
        xaxis=dict(title='Attribute'),
        yaxis=dict(title='Revenue'),
        plot_bgcolor='#1f2c56',
        paper_bgcolor='#1f2c56',
        font=dict(color='white')
    )
    
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)
    
