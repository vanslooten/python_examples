# Interactive Data Dashboard using Dash and Plotly
# This script creates an interactive dashboard using Dash and Plotly to visualize the Gapminder dataset
# See tutorial at https://www.youtube.com/watch?v=GD3iwnJrEZ4&ab_channel=DataGeekismyname

# Step 1: Install required Libraries
# In Visual Studio Code, run the command below in the terminal to install the necessary libraries
# pip install dash pandas plotly

# Step 2: Import Libraries
# Set up imports for data handling, dashboard creation, and visulization

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Step 3: Load the Dataset
# We will use a sample dataset (like gapminder) for this project

# Load the Gapminder dataset
url = "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
data = pd.read_csv(url)

def human_format(num):
    for unit in ['', 'k', 'M', 'B', 'T']:
        if abs(num) < 1000:
            return f"{num:.1f}{unit}" if unit else str(int(num))
        num /= 1000
    return f"{num:.1f}P"

# Create a column with formatted population numbers, e.g., 1.2M for 1200000
data['pop_formatted'] = data['pop'].apply(human_format)

# Display dataset preview
print("Dataset Preview: ")
print(data.head())

#Step 4: Create a Dash App
# Initialize the Dash app

app = dash.Dash(__name__)

#App title 
app.title = "Interactive Data Dashboard"

#Step 5: Build the Dashboard Layout
# Define the Layout
app.layout = html.Div([
    html.H1("Gapminder 2007: Interactive Data Dashboard", style={'textAlign': 'center'}),

    # Dropdown for country selection 
    html.Div([
        html.Label("Continent:"),
        dcc.Dropdown(
            id='continent-dropdown',
            options=[
                {'label': continent, 'value': continent}
                for continent in data['continent'].unique()
            ],
            value='Asia', # Default value
            style={'width': '50%'}
        )
    ],
              style={'margin': '20px'}),

    # Graph for displaying data
    dcc.Graph(id='scatter-plot'),

    # Slider for population filter
    html.Div([
        html.Label("Filter by Minimum Population:"),
        dcc.Slider(
            id='population-slider',
            min=data['pop'].min(),
            max=data['pop'].max(),
            step=1000000,
            value=data['pop'].min(),
            marks={int(data['pop'].min()): 'Min', int(data['pop'].max()): 'Max'}
        )
    ], style={'margin': '20px'})
])
            
                
#Step 6: Add interactivity

@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('population-slider', 'value')]
)
def update_graph(selected_continent, min_population):
    # Filter data based on user input
    filtered_data = data[(data['continent'] == selected_continent) & (data['pop'] >= min_population)].copy()
        
    # Create a scatter plot, passing pop_formatted as text
    # added custom_data to include human-friendly formatted population in hover box, see https://plotly.com/python/hover-text-and-formatting/
    fig = px.scatter(
        filtered_data,
        x='gdpPercap',
        y='lifeExp',
        size='pop',
        color='country',
        hover_name='country',
        title=f"Life Expectancy vs GDP in {selected_continent}",
        labels={'gdpPercap': 'GDP per Capita', 'lifeExp': 'Life Expectancy'},
        custom_data=['pop_formatted'],
    )

    # Use the formatted population in the hovertemplate via customdata
    fig.update_traces(
        hovertemplate='<b>%{hovertext}</b><br>'
                      'GDP per Capita: %{x:.2f}<br>'
                      'Life Expectancy: %{y:.2f}<br>'
                      'Population: %{customdata[0]}'
    )
    return fig

@app.callback(
    [Output('population-slider', 'min'),
     Output('population-slider', 'max'),
     Output('population-slider', 'marks'),
     Output('population-slider', 'value')],
    [Input('continent-dropdown', 'value')]
)
def update_slider(selected_continent):
    filtered = data[data['continent'] == selected_continent]
    min_pop = int(filtered['pop'].min())
    max_pop = int(filtered['pop'].max())
    marks = {min_pop: 'Min', max_pop: 'Max'}
    return min_pop, max_pop, marks, min_pop

#Step 7: Run the App
if __name__ == '__main__':
    app.run_server(debug=True)

# Step 8: Test the Dashboard
# Open a web browser and go to http://127.0.0.1:8050/
# to view the interactive dashboard.
