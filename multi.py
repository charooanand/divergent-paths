import os
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from apps.earningsRankGap import buildApp as buildEarningsRankGap
from apps.earningsLevelGap import buildApp as buildEarningsLevelGap

server = Flask(__name__)

# Health check for Render
@server.get("/healthz")
def healthz():
    return "ok", 200

# Build Dash apps with stable URL prefixes
rank_app = buildEarningsRankGap(basePath="/rank/")
level_app = buildEarningsLevelGap(basePath="/level/")

# Mount both Dash WSGI apps under the Flask server
server.wsgi_app = DispatcherMiddleware(
    server.wsgi_app,
    {
        "/rank": rank_app.server,
        "/level": level_app.server,
    },
)

@server.get("/")
def index():
    return (
        '<h3>Earnings Apps</h3>'
        '<ul>'
        '<li><a href="/rank/">Earnings Rank Gap</a></li>'
        '<li><a href="/level/">Earnings Level Gap</a></li>'
        "</ul>"
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    server.run(host="0.0.0.0", port=port, debug=True)
