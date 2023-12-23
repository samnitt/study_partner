import dash
import pandas as pd
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Sample data for button labels
button_labels = [f"Button {i}" for i in range(1, 21)]
elective = pd.read_excel('elective.xlsx')
global student_details
global repeat1
student_details = pd.read_excel('student_details.xlsx',index_col = 0)
repeat = pd.read_excel('repeat.xlsx',index_col = 0)
repeat1 = pd.read_excel('repeat.xlsx',index_col = 0)
button = student_details['Roll'].tolist()
electivefive = elective['Q5'].tolist()
electivesix = elective['Q6'].tolist()
electiveseven = elective['Q7'].tolist()


main = 'EPGP-15A-002'
l = repeat[repeat['Roll'] == main].index[0]
A = student_details.loc[l, :].values.flatten().tolist()
loop = repeat['Roll'].tolist()
y = 0
for x in loop:
    m = repeat[repeat['Roll'] == x].index[0]
    B = student_details.loc[m, :].values.flatten().tolist()
    C = (set(A).intersection(B))
    D = sorted(C)
    E = len(D) - 1
    if E < 0:
        E = 0
    repeat.iloc[y,1] = E 
    y = y+1
repeat1 = repeat[repeat['Common'] > 0]
repeat1.loc[repeat1[repeat1['Roll'] == main].index[0],'Common'] = 0        


app = dash.Dash(__name__)
app.run_server(debug=True, port=8051)


app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown1',
        options=[{'label': i, 'value': i} for i in button],
        multi=True,
        placeholder="Select Roll Number of yours"
    ),
    
    dcc.Dropdown(
        id='dropdown2',
        options=[{'label': i, 'value': i} for i in electivefive],
        multi=True,
        placeholder="Select Q5 electives"
    ),
    
    dcc.Dropdown(
        id='dropdown3',
        options=[{'label': i, 'value': i} for i in electivesix],
        multi=True,
        placeholder="Select Q6 electives"
    ),
    
    dcc.Dropdown(
        id='dropdown4',
        options=[{'label': i, 'value': i} for i in electiveseven],
        multi=True,
        placeholder="Select Q7 electives4"
    ),
    
    html.Button('Submit', id='submit-button', n_clicks=0),
    
    html.Div(id='output-container-button', children=[]),

    dcc.Graph('Histo')
    
    
])

@app.callback(
    [Output('output-container-button', 'children'),
    #Output('submit-button', 'n_clicks'),
    Output('Histo','figure')],
    [Input('submit-button', 'n_clicks'),
    Input('dropdown1', 'value'),
    Input('dropdown2', 'value'),
    Input('dropdown3', 'value'),
    Input('dropdown4', 'value')]
)
def display_output(n_clicks, dropdown1, dropdown2, dropdown3, dropdown4):
    # Process the selected buttons
    selected_buttons1 = []
    selected_buttons2 = []
    selected_buttons3 = []
    selected_buttons4 = []
    selected_buttons5 = []
    list = []
    repeat2 = repeat1
    figure=px.histogram(repeat2, x='Roll', y='Common')
    if dropdown1:
        selected_buttons1.extend(dropdown1)
    if dropdown2:
        selected_buttons2.extend(dropdown2)
    if dropdown3:
        selected_buttons3.extend(dropdown3)
    if dropdown4:
        selected_buttons4.extend(dropdown4)

    if len(selected_buttons1) > 1:
        return "Error: Please One Roll number alone.", figure
    if len(selected_buttons2) > 6:
        return "Error: Do not select more than 6 electives in Q5.", figure
    if len(selected_buttons3) > 6:
        return "Error: Do not select more than 6 in Q6.", figure
    if len(selected_buttons4) > 6:
        return "Error: Do not select more than 6 in Q7.", figure
    if len(selected_buttons2) < 6:
        return "Error: Select 6 electives in Q5 add dummy to make 6.", figure
    if len(selected_buttons3) < 6:
        return "Error: Select 6 electives in Q6 add dummy to make 6.", figure
    if len(selected_buttons4) < 6:
        return "Error: Select 6 electives in Q7 add dummy to make 6.", figure

    if n_clicks > 0:
        
        student_details.loc[student_details['Roll'] == selected_buttons1[0]] = selected_buttons1+selected_buttons1+selected_buttons2+selected_buttons3+selected_buttons4
        n_clicks = 0
        with pd.ExcelWriter('student_details.xlsx') as writer:
            student_details.to_excel(writer, sheet_name  = 'Sheet_1')
        
        main = selected_buttons1[0]
        l = repeat[repeat['Roll'] == main].index[0]
        A = student_details.loc[l, :].values.flatten().tolist()
        loop = repeat['Roll'].tolist()
        y = 0
        for x in loop:
            m = repeat[repeat['Roll'] == x].index[0]
            B = student_details.loc[m, :].values.flatten().tolist()
            C = (set(A).intersection(B))
            D = sorted(C)
            E = len(D) - 1
            if E < 0:
                E = 0
            repeat.iloc[y,1] = E 
            y = y+1
            
        repeat2 = repeat[repeat['Common'] > 0]
        repeat2.loc[repeat2[repeat2['Roll'] == main].index[0],'Common'] = 0
        figure=px.histogram(repeat2, x='Roll', y='Common')


    return f'Selected buttons: {selected_buttons1+selected_buttons1+selected_buttons2+selected_buttons3+selected_buttons4+selected_buttons5}', figure



if __name__ == '__main__':
    app.run_server(debug=True)
