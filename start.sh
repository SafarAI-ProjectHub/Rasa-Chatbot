#!/bin/bash

export TITLE="Rasa api"
gnome-terminal -- bash -c "echo -ne \"\033]0;${TITLE}\007\"; source venv/bin/activate; rasa run --enable-api --cors '*' --debug; exec bash"

export TITLE="action server"
gnome-terminal -- bash -c "echo -ne \"\033]0;${TITLE}\007\"; source venv/bin/activate; rasa run actions; exec bash"