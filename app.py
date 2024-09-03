import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from dash import dash_table
import textwrap

df = pd.read_excel('Data/disabilitycensus2021_cleaned.xlsx')
df_sen = pd.read_excel('Data/sen_school_level_ud.xls')
df_sen_grpby_la = pd.read_csv('Data/sen_school_grpby_la.csv')
df_sen_school = pd.read_csv('Data/sen_school_wise.csv')
df_dis_type = pd.read_csv('Data/sen_disability_type.csv')

#Summarized data
df_summ = pd.read_excel('Data/summarised_population.xlsx')
df_summ['Percentage'] = df_summ['Percentage'].round(2)

# Calculate the average percentage for each age group
average_percentage_by_age_group = df_summ.groupby('Age')['Percentage'].mean().reset_index()

# Initialize an empty list for conditional styles
style_data_conditional = []

# Generate conditional styles for each age group
for index, row in average_percentage_by_age_group.iterrows():
    style_data_conditional.append({
        'if': {
            'filter_query': '{{Age}} = "{}" && {{Percentage}} > {}'.format(row['Age'], row['Percentage']),
            'column_id': 'Percentage'
        },
        'backgroundColor': 'tomato',
        'color': 'white'
    }),

# Define the columns with logical display names
columns_sen_school = [
    {"name": "Local Authority", "id": "la_name"},
    {"name": "School Name", "id": "school_name"},
    {"name": "Total Strenght", "id": "Total pupils"},
    {"name": "SEN Support", "id": "SEN support"},
    {"name": "EHC Plan", "id": "EHC plan"},
    {"name": "Total SEN & EHC", "id": "Total Sen"}
]

# Define the style for each column
style_cell_conditional_sen_school = [
    {'if': {'column_id': 'school_name'}, 'width': '45%'},  # Largest width
    {'if': {'column_id': 'la_name'}, 'width': '25%'},      # Second largest width
    {'if': {'column_id': 'Total pupils'}, 'width': '10%'},
    {'if': {'column_id': 'SEN support'}, 'width': '10%'},
    {'if': {'column_id': 'EHC plan'}, 'width': '10%'},
    {'if': {'column_id': 'Total Sen'}, 'width': '10%'}
]

# Define the style for the header to wrap text, center-align, and bold
style_header = {
    'whiteSpace': 'normal',
    'overflow': 'hidden',
    'textOverflow': 'ellipsis',
    'maxWidth': '100%',
    'textAlign': 'center',  # Center-align the text
    'fontWeight': 'bold'    # Make the text bold
}

# Define the columns with logical display names
columns_dis_type = [
    {"name": "Local Authority", "id": "la_name"},
    {"name": "Affiliation", "id": "phase_type_grouping"},
    {"name": "Disability Type", "id": "primary_need"},
    {"name": "Total Count (All Ages)", "id": "number_of_pupils"},
    {"name": "Male", "id": "pupil_gender_boys"},
    {"name": "Female", "id": "pupil_gender_girls"}
]

# Define the style for each column
style_cell_conditional_dis_type = [
    {'if': {'column_id': 'primary_need'}, 'width': '40%'},  # Most space
    {'if': {'column_id': 'phase_type_grouping'}, 'width': '25%'},  # Second most space
    {'if': {'column_id': 'la_name'}, 'width': '20%'},  # Third most space
    {'if': {'column_id': 'number_of_pupils'}, 'width': '5%'},
    {'if': {'column_id': 'pupil_gender_boys'}, 'width': '5%'},
    {'if': {'column_id': 'pupil_gender_girls'}, 'width': '5%'}
]
app = dash.Dash( external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div([
    html.Div("NYT Dashboard", style={'fontSize': 50, 'textAlign': 'center', 'color': 'white', 'backgroundColor': 'Green'}),
    dcc.Tabs([
        dcc.Tab(label='Census 2021', children=[
            html.Div([
                html.Div([
                    html.Label('Select Local Authority', style={'fontWeight': 'bold'}),
                    dcc.Dropdown([la for la in df['Local Authority'].unique()], id='la-choice',
                                 style={'width':'100%'}, multi=True, value=['Brent']),
                        ],
                        style={'width':'48%', 'display': 'inline-block'}
                        ),
                html.Div([
                    html.Label('Select Age', style={'fontWeight': 'bold'}),
                    dcc.Dropdown([ag for ag in df['Age'].unique()], id='ag-choice', multi=True, value=['15 to 19'],
                                     style={'width':'100%'}),
                    ],
                    style={'width':'48%', 'display': 'inline-block', 'marginLeft': '4%'}
                    ),
            ],
            style={'display': 'flex'}),
        
        # Card to display total population
        html.Div([
            # Card to display total population
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Population", className="card-title"),
                    # Placeholder for dynamic total population
                    html.P(id="total-population-placeholder", className="card-text"),
                    ]),
                ],
                style={"width": "18rem", "marginTop": "20px", "marginRight": "10px", "border": "5px solid #000 !important"},  # Adjust styling as needed
            ),
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H4("Disabled Population", className="card-title"),
                             # Placeholder for dynamic total population
                            html.P(id="disabled-population-placeholder", className="card-text"),
                        ]
                    ),
                ],
                style={"width": "18rem", "marginTop": "20px","border": "5px solid #000 !important"},  # Adjust styling as needed
            )], 
            style={"display":"flex"}
            ),
            # Inside your layout definition
html.Div([
    dbc.Row([  # This Row wraps all three charts
        dbc.Col([  # First column for the pie chart
            dcc.Graph(id='disability-by-sex-chart')
        ], width=4),  # Adjust 'width' as needed to size the pie chart column
        dbc.Col([  # Second column for another chart
            dcc.Graph(id='disability-by-category-chart')  # Placeholder ID, replace with actual
        ], width=4),  # Adjust 'width' as needed
        dbc.Col([  # Third column for another chart
            dcc.Graph(id='population-bar-chart')  # Placeholder ID, replace with actual
        ], width=4),  # Adjust 'width' as needed
    ], style={"display": "flex", "justify-content": "center"}),  # Adjust styling as needed
    # Other components can follow here
]),
html.Div([
    dbc.Row([  # This Row wraps all three charts
        dbc.Col([  # First column for the pie chart
            dcc.Graph(id='agegroup-scatter-plot', style={'height': '500px'}),
            html.Div(style={'height': '50px'})
        ], width=6),  # Adjust 'width' as needed to size the pie chart column
        dbc.Col([  # Second column for Data Table
            html.H3('Data Table for Disabled Population by Age Group', style={'textAlign': 'center'}),
            dash_table.DataTable(
                id='datatable-agegroup',
    style_data_conditional=style_data_conditional,
    sort_action='native',
    filter_action="native",
    filter_options={"placeholder_text": "Filter column..."},
    style_data={
        'color': 'black',
        'whiteSpace': 'normal',
        'height': 'auto',
    },
    columns=[{"name": i, "id": i} for i in df_summ.columns],
    page_size=10)

        ], width=6),  # Adjust 'width' as needed
    ], style={"display": "flex", "justify-content": "center"}),  # Adjust styling as needed
    # Other components can follow here
]
),
# Empty Div added at the bottom with a height of 50px (adjust as needed)
    html.Div(style={'height': '50px'})

        ],style={'margin': '10px', 'border': '1px solid #d6d6d6'}, selected_style={
            'margin': '10px', 
            'border': '1px solid #a1a1a1',
            'background': 'linear-gradient(to right, #a8e063, #56ab2f)'  # Gradient background for selected tab
        }),

        dcc.Tab(label='SEN', children=[
             html.Div([
                    html.Label('Select Local Authority', style={'fontWeight': 'bold'}),
                    dcc.Dropdown([la for la in df_sen['la_name'].unique()], id='la-choice-sen',
                                 style={'width':'100%'}, multi=True, value=['Brent']),
                        ],
                        style={'width':'48%', 'display': 'inline-block'}
                        ),

                    html.Div([
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("Total Schools", className="card-title"),
                                html.P(id="total-sen-schools", className="card-text"),
                            ]),
                        ],
                        style={"width": "18rem", "marginTop": "20px", "marginRight": "10px", "border": "5px solid #000 !important", "display": "inline-block"},  # Adjust styling as needed
                        ),
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("Total Students", className="card-title"),
                                html.P(id="total-school-strength", className="card-text"),
                            ]),
                        ],
                        style={"width": "18rem", "marginTop": "20px", "marginRight": "10px", "border": "5px solid #000 !important", "display": "inline-block"},  # Adjust styling as needed
                        ),
                        dbc.Card([
                            dbc.CardBody([
                                html.H4("SEN Student's Count", className="card-title"),
                                html.P(id="total-sen_ehc-strength", className="card-text"),
                            ]),
                        ],
                        style={"width": "18rem", "marginTop": "20px", "marginRight": "10px", "border": "5px solid #000 !important", "display": "inline-block"},  # Adjust styling as needed
                        ),
                    ]),

        # Add an empty div for spacing
html.Div(style={"height": "50px"}),  # Adjust 'height' as needed for spacing     
            html.Div([
    dbc.Row([
        dbc.Col(html.H3("Local Authority wise SEN Strenght", style={'textAlign': 'center'}), width=4),
        dbc.Col(html.H3("Disability Type Treemap", style={'textAlign': 'center'}), width=4),
        dbc.Col(html.H3("Phase Type Bar Chart", style={'textAlign': 'center'}), width=4),
    ], style={"display": "flex", "justify-content": "center"}),  # Row for titles

    dbc.Row([
        dbc.Col(dcc.Graph(id='scatter-plot-sen'), width=4),  # First column for the scatter plot
        dbc.Col(dcc.Graph(id='disability-type-treemap'), width=4),  # Second column for the treemap
        dbc.Col(dcc.Graph(id='phase-type-bar-chart'), width=4),  # Third column for the bar chart

    ], style={"display": "flex", "justify-content": "center"},
    justify="center"),  # Center the columns
]),

html.Div([
    dbc.Row([  # This Row wraps all two charts
        dbc.Col([  html.H3('School Wise Strenght', style={'textAlign': 'center'}),
            dash_table.DataTable(
                id='datatable-school',
                #style_data_conditional=style_data_conditional,
                sort_action='native',
                filter_action="native",
                filter_options={"placeholder_text": "Filter column..."},
                style_data={
                    'color': 'black',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                columns=columns_sen_school,
                style_cell_conditional=style_cell_conditional_sen_school,  # Apply the style here
                style_header=style_header, 
                page_size=10),

                dbc.Col([html.Button("Download Data to CSV", id="btn_shool-wise-csv"),
        dcc.Download(id="download-school-wise-csv"),], width=6)
        ], width=6),  # Adjust 'width' as needed to size the pie chart column
        
               dbc.Col([  # Second column for another chart
            html.H3('Datatable on Disability Type', style={'textAlign': 'center'}),
            dash_table.DataTable(
                id='datatable-disability-type',
                #style_data_conditional=style_data_conditional,
                sort_action='native',
                filter_action="native",
                filter_options={"placeholder_text": "Filter column..."},
                style_data={
                    'color': 'black',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                columns=columns_dis_type,
                style_header=style_header,  # Apply the header style here
                style_cell_conditional=style_cell_conditional_dis_type,  # Apply the style here
                page_size=10
            ),
            html.Button("Download Data to CSV", id="btn_dis-type-csv"),
            dcc.Download(id="download-disability-type-csv")
        ], width=6)  # Adjust 'width' as needed

    ], style={"display": "flex", "justify-content": "center"}),  # Adjust styling as needed
    # Other components can follow here
]),

            # Add other components or figures for this tab
        ],style={'margin': '10px', 'border': '1px solid #d6d6d6'}, selected_style={
            'margin': '10px', 
            'border': '1px solid #a1a1a1',
            'background': 'linear-gradient(to right,#a8e063, #56ab2f)'  # Gradient background for selected tab
        }),
            
    ])

],
style={'marginTop': '0', 'marginLeft': '0', 'marginRight': '0'}
)

## Callbacks for Census 2021

@app.callback(
    Output('total-population-placeholder', 'children'),
    [
        Input('la-choice', 'value'),
        Input('ag-choice', 'value'),
    ]
)
def update_total_population(selected_la, selected_ag):
    if selected_la is None:
        # If no region is selected, calculate total population of all regions
        total_population = df['Population'].sum()
    else:
        # Calculate total population for selected regions
         filtered_df = df[(df['Local Authority'].isin(selected_la))
                          & (df['Age'].isin(selected_ag))
                          & (df['Sex'].isin(['Male','Female']))
                          & (df['Disability Status'].isin(['Disabled; limited a lot']))]
         total_population = filtered_df['Population'].sum()
        

    return  f'{total_population}'

@app.callback(
    
     Output('disabled-population-placeholder', 'children'),
    [
        Input('la-choice', 'value'),
        Input('ag-choice', 'value'),
    ]
)
def update_total_population(selected_la, selected_ag):
    
    disabled_population_df = df[(df['Local Authority'].isin(selected_la))
                          & (df['Age'].isin(selected_ag))
                          & (df['Category'] == 'Four category')
                          & (df['Sex'].isin(['Male','Female']))
                          & (df['Disability Status'].isin(['Disabled; limited a lot','Disabled; limited a little']))]
    disabled_population = disabled_population_df['Count'].sum()

    return  f'{disabled_population}'

@app.callback(
    Output('disability-by-sex-chart', 'figure'),
    [Input('la-choice', 'value'),
    Input('ag-choice', 'value'),]
)
def update_pie_chart(selected_la, selected_ag):
    # Example data update based on selected category
    
    disabled_population_df = df[(df['Local Authority'].isin(selected_la))
                          & (df['Age'].isin(selected_ag))
                          & (df['Category'] == 'Four category')
                          & (df['Sex'].isin(['Male','Female']))
                          & (df['Disability Status'].isin(['Disabled; limited a lot','Disabled; limited a little']))]
    
    # Group by 'Sex' and sum 'Count'
    grouped_data = disabled_population_df.groupby('Sex')['Count'].sum()
    
    
    labels = grouped_data.index.tolist()  # Convert index to list for labels
    values = grouped_data.values.tolist()  # Convert values to list
    
    # Update the pie chart
    new_figure = {
        'data': [
            go.Pie(labels=labels, 
                   values=values, 
                   hole=.3,
                   hoverinfo='label+percent+value')
        ],
        'layout': {
            'title': 'Disability by Sex for '
        }
    }
    return new_figure
@app.callback(
    Output('disability-by-category-chart', 'figure'),
    [Input('la-choice', 'value'),
    Input('ag-choice', 'value'),]
)
def update_pie_chart_by_category(selected_la, selected_ag):
    # Example data update based on selected category
    
    poulation_grpby_category = df[(df['Local Authority'].isin(selected_la))
                          & (df['Age'].isin(selected_ag))
                          & (df['Category'] == 'Four category')
                          & (df['Sex'].isin(['Male','Female']))
                          ]
    data = poulation_grpby_category.groupby('Disability Status')['Count'].sum().reset_index()
    
    
    labels = data['Disability Status'].tolist()  # Convert index to list for labels
    values = data['Count'].tolist()  # Convert values to list
    
    # Update the pie chart
    new_figure = {
        'data': [
            go.Pie(labels=labels, 
                   values=values, 
                   hole=.3,
                   hoverinfo='label+percent+value')
        ],
        'layout': {
            'title': {
                'text': 'Disability by Status',
                  'x': 0.3,  # Centers the title
                  'xanchor': 'Left'  # Ensures the center is the anchor point
                    },
            'width':650,
            'height':500
        }
    }
    return new_figure
@app.callback(
    Output('population-bar-chart', 'figure'),  # Assume there's an element with ID 'population-bar-chart' to display the bar chart
    [Input('la-choice', 'value'),  # Assuming these are the dropdowns or inputs that determine the selection
     Input('ag-choice', 'value')]
)
def update_population_bar_chart(selected_la, selected_ag):
    
    filtered_df = df[(df['Local Authority'].isin(selected_la))
                          & (df['Age'].isin(selected_ag))
                          & (df['Sex'].isin(['Male','Female']))
                          & (df['Disability Status'].isin(['Disabled; limited a lot']))]
    total_population = filtered_df['Population'].sum()

    disabled_population_df = df[(df['Local Authority'].isin(selected_la))
                          & (df['Age'].isin(selected_ag))
                          & (df['Category'] == 'Four category')
                          & (df['Sex'].isin(['Male','Female']))
                          & (df['Disability Status'].isin(['Disabled; limited a lot','Disabled; limited a little']))]
    disabled_population = disabled_population_df['Count'].sum()
    
    # Data for the bar plot
    categories = ['Total Population', 'Disabled Population']
    values = [total_population, disabled_population]
    
    # Create the bar plot
    figure = {
        'data': [
            {'type': 'bar',
             'x': categories,
             'y': values,
             'marker': {'color': ['blue', 'orange']}}  # Optional: Use different colors for the bars
        ],
        'layout': {
            'title': 'Total vs Disabled Population',
            'xaxis': {'title': 'Category'},
            'yaxis': {'title': 'Population Count'}
        }
    }
    
    return figure

@app.callback(
    [Output('agegroup-scatter-plot', 'figure'),
     Output('datatable-agegroup', 'data')],
    [Input('la-choice', 'value'),
        Input('ag-choice', 'value')]
)
def update_scatter_and_datatable(selected_la, selected_ag):
    # Filter the DataFrame for the selected age group
    filtered_df = df[(df['Age'].isin(selected_ag))
                     & (df['Sex'].isin(['Male', 'Female']))
                     & (df['Disability Status'].isin(['Disabled; limited a lot']))]
    
    selected_borough = selected_la
    # Group by 'Local Authority' and sum the populations and the disabled count
    grouped_df = filtered_df.groupby('Local Authority', as_index=False).agg({'Population': 'sum', 'Count': 'sum'})
    
    # Create the scatter plot figure with marker size based on the disabled population count
    fig = {
        'data': [{
            'x': grouped_df['Local Authority'],
            'y': grouped_df['Population'],
            'type': 'scatter',
            'mode': 'markers',
            # Adjust marker size based on the 'Count' column, possibly scaled for better visualization
            'marker': {'size': grouped_df['Count'] / grouped_df['Count'].max() * 50,
                       'color': ['red' if la in selected_la else 'blue' for la in grouped_df['Local Authority']]
                       }  # Example scaling
            
        }],
        'layout': {
            'title': 'Population vs. Disabled Population Count by Local Authority',
            'margin': {'l': 60, 'r': 40, 't': 40, 'b': 170},  # Adjust 'b' (bottom) as needed
            'xaxis': {'title': 'Local Authority',
                     'title_standoff': 150,
                     },
            'yaxis': {'title': 'Total Population'},
             'font': {
            'family': "Arial, sans-serif",
            'size': 14,  # Typical <h3> font size, adjust as needed
            'color': "black"
        },
            'plot_bgcolor': 'lightgrey'
        }
    }

    data = df_summ[df_summ['Age'].isin(selected_ag)].to_dict('records')
    
    return fig, data

## Callbacks for SEN

@app.callback(
    [Output('total-sen-schools', 'children'),
     Output('total-school-strength', 'children'),
     Output('total-sen_ehc-strength', 'children'),
     ],
    [
        Input('la-choice-sen', 'value')
        
    ]
)
def update_total_population(selected_la):
    if selected_la is None:
        # If no region is selected, calculate total population of all regions
        total_schools = df_sen['school_name'].nunique()
        total_strenght = df_sen['Total pupils'].sum()
        total_sen_strength = df_sen['SEN support'].sum() + df_sen['EHC plan'].sum()
    else:
        # Calculate total population for selected regions
         total_schools = df_sen[df_sen['la_name'].isin(selected_la)]['school_name'].nunique()

         total_strenght = df_sen[df_sen['la_name'].isin(selected_la)]['Total pupils'].sum()

         total_sen_strength = df_sen[df_sen['la_name'].isin(selected_la)]['SEN support'].sum() + df_sen[df_sen['la_name'].isin(selected_la)]['EHC plan'].sum()

        

    return  f'{total_schools}', f'{total_strenght}', f'{total_sen_strength}'

@app.callback(
    [Output('scatter-plot-sen', 'figure'),
     Output('datatable-school', 'data'),
     Output('datatable-disability-type', 'data'),
     Output('disability-type-treemap', 'figure'),
     Output('phase-type-bar-chart', 'figure')
     ],
    [Input('la-choice-sen', 'value')]
)
def update_sen_scatter_plot(la_value):

    global selected_la # Make the selected region(s) available globally
    selected_la = la_value

    
    #Scatter plot for SEN data
    fig = {
        'data': [{
            'x': df_sen_grpby_la['la_name'],
            'y': df_sen_grpby_la['Total pupils'],
            'type': 'scatter',
            'mode': 'markers',
            # Adjust marker size based on the 'Count' column, possibly scaled for better visualization
            'marker': {
                'size': df_sen_grpby_la['Total Sen'] / df_sen_grpby_la['Total Sen'].max() * 50,
                'color': ['red' if la in selected_la else 'blue' for la in df_sen_grpby_la['la_name']]
            },  # Example scaling

            'text': [
            f"Local Authority: {la}<br>Total Students: {pupils}<br>Total SEN Students: {sen}"
            for la, pupils, sen in zip(df_sen_grpby_la['la_name'], df_sen_grpby_la['Total pupils'], df_sen_grpby_la['Total Sen'])
        ],
        'hoverinfo': 'text'
        }],
        'layout': {
            
            'margin': {'l': 60, 'r': 40, 't': 40, 'b': 170},  # Adjust 'b' (bottom) as needed
            'xaxis': {
                'title': 'Local Authority',
                'title_standoff': 150,
                'tickangle': 45  # Rotate the x-tick labels by 45 degrees
            },
            'yaxis': {
                'title': 'Total Strength'
            },
            'font': {
                'family': "Arial, sans-serif",
                'size': 14,  # Typical <h3> font size, adjust as needed
                'color': "black"
            },
            'plot_bgcolor': 'lightgrey'
        }
    }

    data = df_sen_school[df_sen_school['la_name'].isin(selected_la)].to_dict('records')
    data_dis_type = df_dis_type[df_dis_type['la_name'].isin(selected_la)].to_dict('records')

    # Group by 'primary_need' and sum the counts
    grouped_df = df_dis_type[df_dis_type['la_name'].isin(selected_la)].groupby('primary_need').sum().reset_index()

    treemap = go.Figure(
    data=[
        go.Treemap(
            labels=grouped_df['primary_need'],
            parents=[''] * len(grouped_df),  # No parents since this is a single-level treemap
            values=grouped_df['number_of_pupils'],
            textinfo='label + value',
            text=[f'<br>'.join(textwrap.wrap(label, width=10)) for label in grouped_df['primary_need']]  # Wrap text
        )
    ],
    layout=go.Layout(
        
        width=600,  # Set the width of the treemap
        height=600 # Set the height of the treemap
    )
)
    
    phase_type_grouped_df = df_dis_type[df_dis_type['la_name'].isin(selected_la)].groupby('phase_type_grouping').sum().reset_index()


    barchart = go.Figure(
    data=[
        go.Bar(
            x=phase_type_grouped_df['phase_type_grouping'],
            y=phase_type_grouped_df['number_of_pupils'],
            text=phase_type_grouped_df['number_of_pupils'],
            textposition='auto'
        )
    ],
    layout=go.Layout(
        
        xaxis=dict(title='Phase Type Grouping'),
        yaxis=dict(title='Number of Pupils'),
        width=600,  # Set the width of the barchart
        height=600  # Set the height of the barchart
     )
    )
    return fig, data, data_dis_type, treemap, barchart    

@app.callback(
    Output("download-school-wise-csv", "data"),
    [Input("btn_shool-wise-csv", "n_clicks")],
    prevent_initial_call=True
)
def download_school_wise_csv(n_clicks):
    if n_clicks is None:
        return dash.no_update
    data = df_sen_school[df_sen_school['la_name'].isin(selected_la)]
    return dcc.send_data_frame(data.to_csv, "school_wise.csv", index=False)

@app.callback(
    Output("download-disability-type-csv", "data"),
    [Input("btn_dis-type-csv", "n_clicks")],
    prevent_initial_call=True
)
def download_disability_type_csv(n_clicks):
    if n_clicks is None:
        return dash.no_update
    data = df_dis_type[df_dis_type['la_name'].isin(selected_la)]
    return dcc.send_data_frame(data.to_csv, "disability_type.csv", index=False)

if __name__ == '__main__':
    app.run_server(debug=True)
