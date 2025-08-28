# apps/multi.py
from flask import Flask
from dash import Dash
import apps.earningsLevelGap as level
import apps.earningsRankGap as rank

server = Flask(__name__)

# App A: earnings level gap → available at /level/
appLevel = Dash(
    __name__,
    server=server,
    url_base_pathname="/level/",
)
appLevel.layout = level.app.layout
appLevel.callback_map = level.app.callback_map  # carry over callbacks

# App B: earnings rank gap → available at /rank/
appRank = Dash(
    __name__,
    server=server,
    url_base_pathname="/rank/",
)
appRank.layout = rank.app.layout
appRank.callback_map = rank.app.callback_map

@server.route("/")
def index():
    return "Go to /level/ or /rank/"