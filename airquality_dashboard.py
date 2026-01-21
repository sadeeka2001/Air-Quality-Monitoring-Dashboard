import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load city datasets
city_data = {
    "Colombo": pd.read_csv("/Users//Hehe/Data Science/HND/Dashboard Building/DashApp/data/Colombo.csv"),
    "Kandy": pd.read_csv("/Users//Desktop/Hehe/Data Science/HND/Dashboard Building/DashApp/data/Kandy.csv"),
    "Jaffna": pd.read_csv("/Users//Desktop/Hehe/Data Science/HND/Dashboard Building/DashApp/data/Jaffna.csv"),
    "Trincomalee": pd.read_csv("/Users//Desktop/Hehe/Data Science/HND/Dashboard Building/DashApp/data/Trincomalee.csv"),
    "Gampaha": pd.read_csv("/Users//Desktop/Hehe/Data Science/HND/Dashboard Building/DashApp/data/Gampaha.csv"),
    "Galle": pd.read_csv("/Users//Desktop/Hehe/Data Science/HND/Dashboard Building/DashApp/data/Galle.csv"),
    "Kalutara": pd.read_csv("/Users//Desktop/Hehe/Data Science/HND/Dashboard Building/DashApp/data/Kalutara.csv"),
    "Kurunegala": pd.read_csv("/Users//Desktop/Hehe/Data Science/HND/Dashboard Building/DashApp/data/Kurunegala.csv"),
    "Matara": pd.read_csv("/Users//Desktop/Hehe/Data Science/HND/Dashboard Building/DashApp/data/Matara.csv"),
    "NuwaraEliya": pd.read_csv("/Users//Desktop/Hehe/Data Science/HND/Dashboard Building/DashApp/data/Nuwaraeliya.csv"),
}

months = ['September', 'October', 'November', 'December']

# Process UV index data
processed_city_data = {}
for city, df in city_data.items():
    df['time'] = pd.to_datetime(df['time'])
    df['date'] = df['time'].dt.date
    df['daily_mean_uv'] = df.groupby('date')['uv_index ()'].transform('mean')
    df['city'] = city
    processed_city_data[city] = df[['date', 'city', 'pm10 (μg/m³)', 'pm2_5 (μg/m³)', 'daily_mean_uv','time', 'carbon_monoxide (μg/m³)', 'carbon_dioxide (ppm)', 'nitrogen_dioxide (μg/m³)', 'sulphur_dioxide (μg/m³)', 'dust (μg/m³)', 'uv_index ()']].drop_duplicates().reset_index(drop=True)
    combined_uv_index = pd.concat(processed_city_data.values(), ignore_index=True)


#------------------------
# Load Data
cities = ['Colombo', 'Kandy', 'Anuradhapura', 'Galle', 'Jaffna', 'Nuwaraeliya', 
          'Kurunegala', 'Gampaha', 'Trincomalee', 'Matara', 'Kalutara']
dataframes = {}
for city in cities:
    # Read each CSV file
    try:
        dat = pd.read_csv(f"data/{city}.csv")
        dat['City'] = city  # Add city name to a new column
        dataframes[city] = dat
    except Exception as e:
        print(f"Error loading data for {city}: {e}")

# Combine all city data into a single DataFrame
combined_data = pd.concat(dataframes.values(), ignore_index=True)




#--------------------------


# Initialize Dash app
app = dash.Dash(__name__)
app.title = 'Air Quality Dashboard'

# App Layout
app.layout = html.Div([
    dcc.Tabs([
        # Tab 1: Overview
        dcc.Tab(label='Overview', children=[
            html.Div([
                html.H3("Air Quality Overview", style={'font-size': '25px', 'text-align': 'center', 'margin-bottom': '20px'}),
                
                # Dropdowns in the same line
                html.Div([
                    html.Div([
                        html.Label("Select a City:", style={'font-weight': 'bold', 'margin-bottom': '5px'}),
                        dcc.Dropdown(
                            id='overview-city-dropdown',
                            options=[{'label': city, 'value': city} for city in city_data.keys()],
                            value='Colombo'
                        )
                    ], style={'flex': '1', 'margin-right': '10px'}),  # Styling for the first dropdown

                    html.Div([
                        html.Label("Select a Month:", style={'font-weight': 'bold', 'margin-bottom': '5px'}),
                        dcc.Dropdown(
                            id='month-dropdown',
                            options=[{'label': month, 'value': idx+9} for idx, month in enumerate(months)],
                            value=9
                        )
                    ], style={'flex': '1'})  # Styling for the second dropdown
                ], style={
                    'display': 'flex', 
                    'align-items': 'center', 
                    'margin-bottom': '20px'
                }),

                # Summary Cards and Graphs
                html.Div(id='overview-summary-cards'),
                dcc.Graph(id='overview-heatmap'),
                dcc.Graph(id='overview-bar-chart'),
            ])
        ]),

        # Tab 2: City Trends
        dcc.Tab(label='City Trends', children=[
            dcc.Tabs([
                # Sub-Tab 1: Particulate Matter Trends
                dcc.Tab(label='Particulate Matter Concentration', children=[
                    html.Div([
                        # Dropdown and Radio Items in the Same Line
                        html.Div([
                            html.Div([
                                html.Label("Select a City:", style={'font-weight': 'bold', 'margin-bottom': '5px'}),
                                dcc.Dropdown(
                                    id='city-dropdown',
                                    options=[{'label': city, 'value': city} for city in city_data.keys()],
                                    value='Colombo'
                                )
                            ], style={'flex': '1', 'margin-right': '10px'}),  # City Dropdown

                            html.Div([
                                html.Label("Select a Month:", style={'font-weight': 'bold', 'margin-bottom': '5px'}),
                                dcc.RadioItems(
                                    id='month-radio',
                                    options=[{'label': month, 'value': month} for month in months],
                                    value='September',
                                    inline=True,
                                    style={'padding': '10px'}
                                )
                            ], style={'flex': '1'})  # Month Radio Items
                        ], style={
                            'display': 'flex',
                            'align-items': 'center',
                            'margin-bottom': '20px'
                        }),

                        # Graph Container
                        html.Div(id='city-graph-container')
                    ])
                ]),

                # Sub-Tab 2: Pollutant Analysis
                dcc.Tab(label='Pollutant Analysis', children=[
                    html.Div([
                        # Dropdown in Pollutant Analysis
                        html.Div([
                            html.Label("Select a City:", style={'font-weight': 'bold', 'margin-bottom': '5px'}),
                            dcc.Dropdown(
                                id='pollutant-city-dropdown',
                                options=[{'label': city, 'value': city} for city in city_data.keys()],
                                value='Colombo'
                            )
                        ], style={'margin-bottom': '20px'}),  # Add margin between dropdown and graphs

                        # Graphs
                        dcc.Graph(id='pollutant-bar-chart'),
                        # html.Label("Seasonal Contribution:", style={'font-weight': 'bold', 'margin-top': '20px'}),
                        dcc.Graph(id='seasonal-pie-chart'),
                        # html.Label("UV Index Analysis:", style={'font-weight': 'bold', 'margin-top': '20px'}),
                        dcc.Graph(id='uv-heatmap')
                    ])
                ])
            ])

        ]),

        # Tab 3: Air Quality Analysis
        dcc.Tab(label="Air Quality Analysis", children=[
            # Section 1: Bar Chart
            html.Div([
                html.H3("City Comparison (Bar Chart)", style={'font-size':'25' ,'text-align': 'center', 
                'background-color': '#f0f8ff',                    
                'margin-bottom': '20px',
                'padding': '10px',
                'border-radius': '10px',}),
                html.Div([
                    html.Div([
                        html.Label("Select Metric for Y-Axis:", style={'font-weight': 'bold'}),
                        dcc.Dropdown(
                            id="bar_x_axis",
                            options=[{"label": col, "value": col} for col in combined_data.columns if col not in ["City", "time"]],
                            value="pm10 (μg/m³)",
                            placeholder="Select Metric for Y-Axis"
                        )
                    ], style={'flex': '1', 'margin-right': '10px'}),
                ], style={
                    'display': 'flex',
                    'align-items': 'center',
                    'margin-bottom': '20px'

                }),
                dcc.Graph(id="city_bar_chart")
            ]),

            html.Hr(),

            # Section 2: Scatter Plot
            html.Div([
                html.H3("Scatter Plot (Pollutant Correlation)", style={'font-size':'25', 'text-align': 'center', 
                'background-color': '#f0f8ff',                    
                'margin-bottom': '20px',
                'padding': '10px',
                'border-radius': '10px',}),
                html.Div([
                    html.Div([
                        html.Label("Select Metric for X-Axis:", style={'font-weight': 'bold'}),
                        dcc.Dropdown(
                            id="scatter_x_axis",
                            options=[{"label": col, "value": col} for col in combined_data.columns if col not in ["City", "time"]],
                            value="pm10 (μg/m³)",
                            placeholder="Select Metric for X-Axis"
                        )
                    ], style={'flex': '1', 'margin-right': '10px'}),

                    html.Div([
                        html.Label("Select Metric for Y-Axis:", style={'font-weight': 'bold'}),
                        dcc.Dropdown(
                            id="scatter_y_axis",
                            options=[{"label": col, "value": col} for col in combined_data.columns if col not in ["City", "time"]],
                            value="pm2_5 (μg/m³)",
                            placeholder="Select Metric for Y-Axis"
                        )
                    ], style={'flex': '1'})
                ], style={
                    'display': 'flex',
                    'align-items': 'center',
                    'margin-bottom': '20px'
                }),
                dcc.Graph(id="scatter_plot")
            ]),

            html.Hr(),

            # Section 3: Alerts and Outliers
            html.Div([
                html.H3("Alerts and Outliers", style={'font-size':'25', 'text-align': 'center', 
                'background-color': '#f0f8ff',                    
                'margin-bottom': '20px',
                'padding': '10px',
                'border-radius': '10px',}),
                html.Div([
                    html.Label("Thresholds:", style={'font-weight': 'bold', 'margin-right': '10px'}),
                    dcc.Checklist(
                        id="threshold_checklist",
                        options=[
                            {"label": "PM2.5 > 100 (μg/m³)", "value": "pm2_5 (μg/m³)"},
                            {"label": "PM10 > 150 (μg/m³)", "value": "pm10 (μg/m³)"},
                            {"label": "CO > 10 (μg/m³)", "value": "carbon_monoxide (μg/m³)"},
                            {"label": "NO2 > 80 (μg/m³)", "value": "nitrogen_dioxide (μg/m³)"},
                        ],
                        value=["pm2_5 (μg/m³)", "pm10 (μg/m³)"],
                        inline=True,
                        style={'padding': '10px'}
                    )
                ], style={
                    'display': 'flex',
                    'align-items': 'center',
                    'margin-bottom': '20px',
                    'padding': '10px',
                    'border-radius': '10px',
                    'background-color': '#f0f8ff'
                }),
                dcc.Graph(id="alerts_outliers")
            ]),
        ])

    ])
])

def get_air_quality_status(pm10, pm25, co):
    if (pm10 <= 50 and pm25 <= 25 and co <= 4400):
        return "Good", "green"
    elif (pm10 <= 100 and pm25 <= 50 and co <= 9400):
        return "Moderate", "yellow"
    elif (pm10 <= 150 and pm25 <= 75 and co <= 12400):
        return "Unhealthy for Sensitive Groups", "orange"
    else:
        return "Unhealthy", "red"

# Callbacks for Tab 1
@app.callback(
    [Output('overview-summary-cards', 'children'),
     Output('overview-heatmap', 'figure'),
     Output('overview-bar-chart', 'figure')],
    [Input('overview-city-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)

def update_overview(selected_city, selected_month):
    # Data processing logic remains the same
    df = city_data[selected_city]
    df['time'] = pd.to_datetime(df['time'])
    df['date'] = df['time'].dt.date
    df['month'] = df['time'].dt.month
    df = df[df['month'] == selected_month]
    
    if df.empty:
        return (
            html.Div("No data available for the selected filters.", className="summary-card"),
            go.Figure(),
            go.Figure()
        )

    numeric_columns = ['pm10 (μg/m³)', 'pm2_5 (μg/m³)', 'carbon_monoxide (μg/m³)', 
                       'carbon_dioxide (ppm)', 'nitrogen_dioxide (μg/m³)', 
                       'sulphur_dioxide (μg/m³)', 'dust (μg/m³)', 'uv_index ()']
    
    numeric_df = df[['date'] + numeric_columns].copy()
    numeric_df[numeric_columns] = numeric_df[numeric_columns].apply(pd.to_numeric, errors='coerce')
    daily_aggregates = numeric_df.groupby('date').mean().reset_index()

    avg_pm10 = daily_aggregates['pm10 (μg/m³)'].mean()
    avg_pm25 = daily_aggregates['pm2_5 (μg/m³)'].mean()
    avg_co = daily_aggregates['carbon_monoxide (μg/m³)'].mean()
    avg_co2 = daily_aggregates['carbon_dioxide (ppm)'].mean()
    avg_no2 = daily_aggregates['nitrogen_dioxide (μg/m³)'].mean()
    avg_so2 = daily_aggregates['sulphur_dioxide (μg/m³)'].mean()
    avg_dust = daily_aggregates['dust (μg/m³)'].mean()
    avg_uv = daily_aggregates['uv_index ()'].mean()

    status, color = get_air_quality_status(avg_pm10, avg_pm25, avg_co)

    # Summary Cards
    summary_cards = html.Div(
        [
            html.Div(
                [
                    html.H4("Particulate Matter", style={'margin-bottom': '10px'}),
                    html.P(f"PM10: {avg_pm10:.2f} μg/m³"),
                    html.P(f"PM2.5: {avg_pm25:.2f} μg/m³"),
                    html.P(f"Dust: {avg_dust:.2f} μg/m³")
                ],
                style={
                    'padding': '20px',
                    'background-color': '#f9f9f9',
                    'border': '3px solid red',
                    'border-radius': '10px',  # Curved edges
                    'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.05)',
                    'flex': '1',
                    'text-align': 'center',  # Center the text
                    'display': 'flex',  # Align text vertically
                    'flex-direction': 'column',  # Arrange items vertically
                    'justify-content': 'center',  # Center content vertically
                    'width': '159px',  # Set card width
                    'height': '150px'  # Set card height
                }
            ),
            html.Div(
                [
                    html.H4("Other Pollutants", style={'margin-bottom': '10px'}),
                    html.P(f"CO: {avg_co:.2f} μg/m³"),
                    html.P(f"CO2: {avg_co2:.2f} ppm"),
                    html.P(f"NO2: {avg_no2:.2f} μg/m³"),
                    html.P(f"SO2: {avg_so2:.2f} μg/m³"),
                    html.P(f"UV Index: {avg_uv:.2f}")
                ],
                style={
                    'padding': '20px',
                    'background-color': '#f9f9f9',
                    'border': '3px solid orange',
                    'border-radius': '10px',  # Curved edges
                    'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.05)',
                    'flex': '1',
                    'text-align': 'center',
                    'display': 'flex',
                    'flex-direction': 'column',
                    'justify-content': 'center',
                    'width': '159px',  # Set card width
                    'height': '250px'  # Set card height
                }
            ),
            html.Div(
                [
                    html.H4("Air Quality Status", style={'margin-bottom': '10px'}),
                    html.P(status, style={'color': color, 'font-weight': 'bold', 'font-size': '1.2em'}),
                    html.P("Based on PM10, PM2.5, and CO levels")
                ],
                style={
                    'padding': '20px',
                    'background-color': '#f9f9f9',
                    'border': '3px solid green',
                    'border-radius': '10px',
                    'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.05)',
                    'flex': '1',
                    'text-align': 'center',
                    'display': 'flex',
                    'flex-direction': 'column',
                    'justify-content': 'center',
                    'width': '159px',  # Set card width
                    'height': '150px'  # Set card height
                }
            )
        ],
        style={
            'display': 'flex',
            'justify-content': 'space-between',
            'gap': '20px',
            'margin': '20px 0'
        }
    )

    # Heatmap and bar chart remain unchanged
    pollutants = ['pm10 (μg/m³)', 'pm2_5 (μg/m³)', 'carbon_monoxide (μg/m³)', 'carbon_dioxide (ppm)', 'nitrogen_dioxide (μg/m³)', 'sulphur_dioxide (μg/m³)', 'dust (μg/m³)', 'uv_index ()']
    heatmap_data = daily_aggregates[['date'] + pollutants]
    heatmap_fig = go.Figure(data=go.Heatmap(z=heatmap_data[pollutants].values.T, x=heatmap_data['date'], y=pollutants, colorscale='Viridis', colorbar=dict(title='Concentration')))
    heatmap_fig.update_layout(title=f"Air Quality Heatmap - {selected_city}", xaxis_title='Date', yaxis_title='Pollutants', height=600)

    bar_chart_fig = px.bar(daily_aggregates, x='date', y=pollutants, title=f"Daily Pollutant Levels in {selected_city}", labels={'value': 'Concentration', 'variable': 'Pollutants'}, color_discrete_sequence=px.colors.qualitative.Set2)
    bar_chart_fig.update_layout(barmode='group', height=600, showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

    return summary_cards, heatmap_fig, bar_chart_fig


# Callbacks for Tab 2
@app.callback(
    Output('city-graph-container', 'children'),
    [Input('city-dropdown', 'value'),
     Input('month-radio', 'value')]
)

# Callback for PM2.5 Trends (Sub-Tab 1)

def update_city_graph(selected_city, selected_month):
    # Fetch data for the selected city
    df = city_data[selected_city]

    if 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'])
        month_mapping = {'September': 9, 'October': 10, 'November': 11, 'December': 12}
        filtered_df = df[df['time'].dt.month == month_mapping[selected_month]]

        # Check if both PM2.5 and PM10 columns are available in the data
        if not filtered_df.empty and 'pm2_5 (μg/m³)' in filtered_df.columns and 'pm10 (μg/m³)' in filtered_df.columns:
            # Melt the DataFrame for dual-line plotting
            melted_df = filtered_df.melt(
                id_vars=['time'],
                value_vars=['pm2_5 (μg/m³)', 'pm10 (μg/m³)'],
                var_name='Particulate Matter',
                value_name='Concentration'
            )

            # Create a dual-line chart
            fig = px.line(
                melted_df,
                x='time',
                y='Concentration',
                color='Particulate Matter',
                title=f"PM2.5 and PM10 Levels in {selected_city} - {selected_month}",
                labels={'time': 'Date', 'Concentration': 'Concentration (μg/m³)', 'Particulate Matter': 'Type'}
            )
            fig.update_layout(legend_title_text='Particulate Matter Type')

            return dcc.Graph(figure=fig)
        else:
            return html.Div("No data available for PM2.5 or PM10 in the selected month.")
    else:
        return html.Div("Data not available for the selected city.")

@app.callback(
    Output('pollutant-bar-chart', 'figure'),
    [Input('pollutant-city-dropdown', 'value')]
)

# Pollutant Analysis (Sub-Tab 2

# Pollutant Bar Chart

def update_bar_chart(selected_city):
    if selected_city is None:
        return go.Figure()

    df = city_data[selected_city]

    df['time'] = pd.to_datetime(df['time'])

    df['month'] = df['time'].dt.strftime('%B')

    # Maximum recorded levels per month for each pollutant
    pollutants = ['carbon_monoxide (μg/m³)', 'carbon_dioxide (ppm)', 
                  'nitrogen_dioxide (μg/m³)', 'sulphur_dioxide (μg/m³)', 'dust (μg/m³)']
    max_data = df.groupby('month')[pollutants].max().reset_index()

    # Reorder months to calendar order
    months_order = ['September', 'October', 'November', 'December']
    max_data['month'] = pd.Categorical(max_data['month'], categories=months_order, ordered=True)
    max_data = max_data.sort_values('month')

    # Create the bar chart
    fig = go.Figure()
    for pollutant in pollutants:
        fig.add_trace(go.Bar(
            x=max_data['month'],
            y=max_data[pollutant],
            name=pollutant
        ))

    # Customize the layout
    fig.update_layout(
        title=f"Maximum Recorded Levels for Pollutants in {selected_city}",
        xaxis_title="Month",
        yaxis_title="Maximum Levels",
        barmode='group',  
        legend_title="Pollutants",
        xaxis=dict(tickangle=-45),
        template="plotly"
    )

    return fig

@app.callback(
    Output('seasonal-pie-chart', 'figure'),
    [Input('pollutant-city-dropdown', 'value')]
)

# Seasonal Pie Chart

def update_seasonal_pie_chart(selected_city):
    if selected_city is None:
        return go.Figure()

    df = city_data[selected_city]

    df['time'] = pd.to_datetime(df['time'])

    df['month'] = df['time'].dt.strftime('%B')

    pollutants = ['carbon_monoxide (μg/m³)', 'carbon_dioxide (ppm)', 
                  'nitrogen_dioxide (μg/m³)', 'sulphur_dioxide (μg/m³)', 'dust (μg/m³)']
    df['total_pollution'] = df[pollutants].sum(axis=1)
    monthly_totals = df.groupby('month')['total_pollution'].sum().reset_index()

    months_order = ['September', 'October', 'November', 'December']
    monthly_totals['month'] = pd.Categorical(monthly_totals['month'], categories=months_order, ordered=True)
    monthly_totals = monthly_totals.sort_values('month')

    # Create a pie chart
    fig = px.pie(
        monthly_totals,
        names='month',
        values='total_pollution',
        title=f"Seasonal Contribution of Pollution in {selected_city}",
        labels={'month': 'Month', 'total_pollution': 'Total Pollution'}
    )
    fig.update_traces(textinfo='percent+label')

    return fig


@app.callback(
    Output('uv-heatmap', 'figure'),
    [Input('pollutant-city-dropdown', 'value')]
)

def update_uv_heatmap(selected_city):
    if selected_city is None:
        return go.Figure()
    
    city_data = combined_uv_index[combined_uv_index['city'] == selected_city].copy()
    city_data['date'] = pd.to_datetime(city_data['date'])
    city_data['day_name'] = city_data['date'].dt.strftime('%A')
    
    min_date = city_data['date'].min()
    max_date = city_data['date'].max()
    
    # Find the first Monday
    days_to_monday = (0 - min_date.weekday()) % 7
    first_monday = min_date + pd.Timedelta(days=days_to_monday)
    
    # Generate all Mondays
    monday_dates = pd.date_range(start=first_monday, end=max_date, freq='W-MON')
    
    # Group data by week 
    city_data['week_monday'] = city_data['date'].apply(
        lambda x: x - pd.Timedelta(days=x.weekday())
    )
    
    # Create pivot table using week Monday as columns
    pivot_df = city_data.pivot_table(
        index='day_name',
        columns='week_monday',
        values='daily_mean_uv',
        aggfunc='mean'
    )
    
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_df = pivot_df.reindex(days_order)
    pivot_df = pivot_df.iloc[::-1]
    
    x_labels = [d.strftime('%b-%d') for d in pivot_df.columns] # Monday Dates as labels
    
    # Create hover text matrix
    hover_matrix = []
    for i in range(len(pivot_df.index)):
        hover_row = []
        for j in range(len(pivot_df.columns)):
            if not pd.isna(pivot_df.iloc[i, j]):
                # Get the actual date for this cell
                monday_date = pivot_df.columns[j]
                day_offset = days_order.index(pivot_df.index[i])
                actual_date = monday_date + pd.Timedelta(days=day_offset)
                date_str = actual_date.strftime('%Y-%m-%d')
                uv_value = pivot_df.iloc[i, j]
                hover_row.append(
                    f'Date: {date_str}<br>'
                    f'Day: {pivot_df.index[i]}<br>'
                    f'UV Index: {uv_value:.2f}'
                )
            else:
                hover_row.append('')
        hover_matrix.append(hover_row)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=x_labels,
        y=pivot_df.index,
        colorscale='YlOrRd',
        colorbar=dict(
            title='UV Index',
            titleside='right'
        ),
        hoverongaps=False,
        text=hover_matrix,
        hovertemplate="%{text}<extra></extra>"
    ))
    
    fig.update_layout(
        title=f'Weekly UV Index Patterns in {selected_city}',
        xaxis_title='Week Starting',
        yaxis_title='Day of Week',
        height=500,
        xaxis=dict(
            side='top',
            tickangle=45,
            showgrid=True
        ),
        yaxis=dict(
            tickmode='array',
            ticktext=days_order[::-1],
            tickvals=list(range(len(days_order)))
        )
    )
    
    return fig


# Callbacks for Tab 3
# Callbacks
@app.callback(
    Output("city_bar_chart", "figure"),
    Input("bar_x_axis", "value")
)
def update_bar_chart(x_axis):
    if x_axis:
        avg_data = combined_data.groupby("City")[x_axis].mean().reset_index()
        fig = px.bar(avg_data, x="City", y=x_axis, title=f"Average {x_axis} Levels Across Cities")
        return fig
    return {}


@app.callback(
    Output("scatter_plot", "figure"),
    [Input("scatter_x_axis", "value"),
     Input("scatter_y_axis", "value")]
)
def update_scatter_plot(x_axis, y_axis):
    if x_axis and y_axis:
        fig = px.scatter(combined_data, x=x_axis, y=y_axis, color="City",
                         title=f"Correlation between {x_axis} and {y_axis}")
        return fig
    return {}

@app.callback(
    Output("alerts_outliers", "figure"),
    [Input("threshold_checklist", "value")]
)

def update_alerts_outliers(thresholds):
    if thresholds:
        highlight_df = combined_data.copy()

        highlight_df['Alert'] = False

        # Update 'Alert' column based on thresholds
        for metric in thresholds:
            if metric == "pm2_5 (μg/m³)":
                highlight_df['Alert'] = highlight_df['Alert'] | (highlight_df["pm2_5 (μg/m³)"] > 100)
            elif metric == "pm10 (μg/m³)":
                highlight_df['Alert'] = highlight_df['Alert'] | (highlight_df["pm10 (μg/m³)"] > 150)
            elif metric == "carbon_monoxide (μg/m³)":
                highlight_df['Alert'] = highlight_df['Alert'] | (highlight_df["carbon_monoxide (μg/m³)"] > 10)
            elif metric == "nitrogen_dioxide (μg/m³)":
                highlight_df['Alert'] = highlight_df['Alert'] | (highlight_df["nitrogen_dioxide (μg/m³)"] > 80)


        fig = px.scatter(highlight_df, x="City", y="pm2_5 (μg/m³)", color="Alert",
                         title="Highlighted Alerts and Outliers",
                         labels={"Alert": "Exceeds Threshold"},
                         symbol="Alert")
        return fig
    return {}



if __name__ == '__main__':
    app.run_server(debug=True, port=8865)
