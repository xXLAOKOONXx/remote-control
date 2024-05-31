import os
from pathlib import Path
from dash import Dash, html, dcc, Input, Output, State, MATCH
import dash_bootstrap_components as dbc
import dash
from tkinter import filedialog
import pyautogui
import pygame

# Select folder
FOLDER = Path(filedialog.askdirectory())

# Select file type
FILE_TYPES = ['fpl', 'm3u']
file_types_input = input('Enter file types seperated by ";" (defaults to "fpl" andd "m3u"): ')
if file_types_input:
    FILE_TYPES = [filetype.strip() for filetype in file_types_input.split(';')]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
              suppress_callback_exceptions=True)

def get_playlist_store_id(playlist:str):
    return {'type': 'playlist-data', 'playlist': playlist}

def get_playlist_button_id(playlist:str):
    return {'type': 'playlist-button', 'playlist': playlist}

def get_effect_store_id(effect:str):
    return {'type': 'effect-data', 'effect': effect}

def get_effect_button_id(effect:str):
    return {'type': 'effect-button', 'effect': effect}

def build_playlist_button(display_name:str, full_path:str):
    return html.Div([
        dbc.Button(display_name, id=get_playlist_button_id(display_name), n_clicks=0, style={'margin': '5px'}),
        dcc.Store(id=get_playlist_store_id(display_name), data=full_path)    
    ])

def build_effect_button(display_name:str, full_path:str):
    return html.Div([
        dbc.Button(display_name, id=get_effect_button_id(display_name), n_clicks=0, style={'margin': '5px'}),
        dcc.Store(id=get_effect_store_id(display_name), data=full_path)    
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

pygame.mixer.init()

@app.callback(
    Output(get_effect_button_id(MATCH), 'style'),
    [Input(get_effect_button_id(MATCH), 'n_clicks'),
     State(get_effect_store_id(MATCH), 'data')]
)
def start_file(n_clicks, effect):
    if n_clicks:
        pygame.mixer.music.load(effect)
        pygame.mixer.music.play()
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
for file_type in FILE_TYPES:
    for file in FOLDER.glob(f'*.{file_type}'):
        display_name = file.stem.strip()
        playlists.append(build_playlist_button(display_name, str(file)))

effects = []

for file in FOLDER.glob('*.mp3'):
    display_name = file.stem.strip()
    effects.append(build_effect_button(display_name, str(file)))
for file in FOLDER.glob('*.wav'):
    display_name = file.stem.strip()
    effects.append(build_effect_button(display_name, str(file)))

app.title = 'Remote-Control'

app.layout = html.Div(id='full-body',
    children=[
        dbc.Row([html.H1('Remote Control', style={'textAlign': 'center'}),]),
        dbc.Row([
            dbc.Button('Play/Pause', id='play-pause', n_clicks=0, style={'margin': '5px'}),
        ]),
        dbc.Row([
            dbc.Col([html.Div('Playlists', style={'textAlign': 'center', 'fontSize': '2rem'})])]),
        dbc.Row([
            dbc.Col([html.Div(id='playlist-buttons',
            children=
        playlists)]),
        ]),
        dbc.Row([dbc.Col([html.Div('Effects')])]),
        dbc.Row([dbc.Col([html.Div(id='effect-buttons',children=effects)])]),
], 
)


if __name__ == '__main__':
    app.run_server(debug=False, port=80, host='0.0.0.0')