import os
from pathlib import Path
from dash import Dash, html, dcc, Input, Output, State, MATCH
import dash_bootstrap_components as dbc
import dash
from tkinter import filedialog
import pyautogui

# Select folder
FOLDER = Path(filedialog.askdirectory())

# Select file type
FILE_TYPE = 'fpl'
FILE_TYPE = input('Enter file type (defaults to "fpl"): ') or FILE_TYPE

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
              suppress_callback_exceptions=True)

def get_playlist_store_id(playlist:str):
    return {'type': 'playlist-data', 'playlist': playlist}

def get_playlist_button_id(playlist:str):
    return {'type': 'playlist-button', 'playlist': playlist}

def build_playlist_button(display_name:str, full_path:str):
    return html.Div([
        dbc.Button(display_name, id=get_playlist_button_id(display_name), n_clicks=0, style={'margin': '5px'}),
        dcc.Store(id=get_playlist_store_id(display_name), data=full_path)    
    ])

@app.callback(
    Output(get_playlist_button_id(MATCH), 'style'),
    [Input(get_playlist_button_id(MATCH), 'n_clicks'),
     State(get_playlist_store_id(MATCH), 'data')]
)
def start_file(n_clicks, playlist):
    if n_clicks:
        os.startfile(playlist)
    return dash.no_update

@app.callback(
    Output('play-pause', 'children'),
    [Input('play-pause', 'n_clicks')]
)
def play_pause(n_clicks):
    if n_clicks:
        pyautogui.press('playpause')
    return dash.no_update

playlists = []
for file in FOLDER.glob(f'*.{FILE_TYPE}'):
    display_name = file.stem.strip()
    playlists.append(build_playlist_button(display_name, str(file)))

app.title = 'Remote-Control'

app.layout = html.Div(id='full-body',
    children=[
        dbc.Row([html.H1('Remote Control', style={'textAlign': 'center'}),]),
        dbc.Row([
            dbc.Button('Play/Pause', id='play-pause', n_clicks=0, style={'margin': '5px'}),
        ]),
        dbc.Row([
            dbc.Col([html.Div(id='playlist-buttons',
            children=
        playlists)]),
        ])
], 
)


if __name__ == '__main__':
    app.run_server(debug=False, port=80, host='0.0.0.0')