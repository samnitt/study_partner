import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Initialize the Dash app
app = dash.Dash(__name__)
app.run_server(debug=True, port=8051)

# Sample options for the dropdown
dropdown_options = [
    {'label': 'Option 1', 'value': 'opt1'},
    {'label': 'Option 2', 'value': 'opt2'},
    {'label': 'Option 3', 'value': 'opt3'}
]

# Layout of the web page
app.layout = html.Div([
    html.H1("Dash Dropdown Example"),
    
    # Dropdown component
    dcc.Dropdown(
        id='my-dropdown',         # Component ID
        options=dropdown_options, # Dropdown options
        value='opt1'              # Default selected value
    ),
    
    # Output div to display selected value
    html.Div(id='output-div')
])

# Callback to update the output based on dropdown selection
@app.callback(
    Output('output-div', 'children'),
    [Input('my-dropdown', 'value')]
)
def update_output(selected_option):
    return f"You selected: {selected_option}"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
