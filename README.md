# Remote Controller

This is web app to start files from a different device.

## Usage

### Guide

On app start you are required to give two information.

1. A file dialog opens to select the folder with the files
2. A console window opens asking for the file ending to search for

The webapp is available at `localhost:80` and via ip adress within your local network.

The ip adresses are shown in the console as well.

To close the webapp press Ctrl + C within the Console or close the console window.

For each startable file with the correct file ending there will be a button with the filename as display text.

### Use code

Install poetry package

```bash
pip install poetry
```

Install poetry environment

```bash
poetry install
```

Start the app

```bash
poetry run python remote-control/app.py
```

### Use exe

You can find the latest exe in the releases.
