import dash
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import math
import numpy as np
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from helpers import readData
from helpers import ordinal

dfAll, dfNonZero = readData()

# Your function (slightly adapted to work inside Dash)
def earningsGapHisto(df, y, xrange, binSize, percentile,
                     blackBarHex, blackLineHex,
                     whiteBarHex, whiteLineHex):
    dfYear = df[df['year'] == y]
    dfYearW = dfYear[dfYear['race'] == 1]
    dfYearB = dfYear[dfYear['race'] == 2]

    white_percentile = dfYearW["lrinc"].quantile(percentile / 100)
    black_percentile = dfYearB["lrinc"].quantile(percentile / 100)

    white_income = np.exp(white_percentile)
    black_income = np.exp(black_percentile)
    income_gap = white_income - black_income

    fig = make_subplots(rows=2, cols=1)

    fig.add_trace(
        go.Histogram(
            x=dfYearW["lrinc"],
            name="White",
            marker_color=whiteBarHex,
            xbins=dict(start=xrange[0], end=xrange[1], size=binSize),
            hoverinfo='none'
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Histogram(
            x=dfYearB["lrinc"],
            name="Black",
            marker_color=blackBarHex,
            xbins=dict(start=xrange[0], end=xrange[1], size=binSize),
            hoverinfo='none'
        ),
        row=2, col=1
    )

    shapes = []

    white_norm_pos = (white_percentile - xrange[0]) / (xrange[1] - xrange[0])
    shapes.append(dict(
        type="line", xref="paper", yref="paper",
        x0=white_norm_pos, y0=0, x1=white_norm_pos, y1=1,
        line=dict(color=whiteLineHex, width=4)
    ))

    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=white_norm_pos,
        y=.65,
        text = f"{ordinal(int(round(percentile)))}: ${white_income:,.0f}",
        showarrow=False,
        textangle=-90,
        xshift=18,
        font=dict(
            color=whiteLineHex,
            size=12
        )
    )

    black_norm_pos = (black_percentile - xrange[0]) / (xrange[1] - xrange[0])
    shapes.append(dict(
        type="line", xref="paper", yref="paper",
        x0=black_norm_pos, y0=0, x1=black_norm_pos, y1=1,
        line=dict(color=blackLineHex, width=4)
    ))

    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=black_norm_pos,
        y=.01,
        text = f"{ordinal(int(round(percentile)))}: ${black_income:,.0f}",
        showarrow=False,
        textangle=-90,
        xshift=-10,
        font=dict(
            color=blackLineHex,
            size=12
        )
    )

    fig.update_layout(shapes=shapes)

    real_income_ticks = [
        0,
        1000,
        5000,
        10000,
        25000,
        50000,
        100000,
        250000,
        500000,
        1000000,
        2000000
    ]

    log_income_ticks = [np.log(x) if x > 0 else 0 for x in real_income_ticks]

    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor=whiteLineHex,
        range=xrange,
        tickvals=log_income_ticks,
        ticktext=[f"${x:,}" for x in real_income_ticks],
        type="linear",
        tickangle=-90,
        row=1, col=1
    )
    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor=blackLineHex,
        range=xrange,
        tickvals=log_income_ticks,
        ticktext=[f"${x:,}" for x in real_income_ticks],
        type="linear",
        tickangle=90,
        row=2, col=1
    )

    fig.update_yaxes(title_text="White Men", row=1, col=1, tickvals=[])
    fig.update_yaxes(title_text="Black Men", row=2, col=1, tickvals=[])

    fig.update_layout(
        height=800,
        width=800,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig



# --- Initialize Dash app ---
app = Dash(__name__)
server = app.server


default_pct = 50
default_year = 1940
default_df = dfNonZero

blackLineHex = "#043f73"
whiteLineHex = "#666666"

app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='histo-graph',
            figure=earningsGapHisto(
                df=default_df,
                y=default_year,
                xrange=[0, 14],
                binSize=0.2,
                percentile=default_pct,
                whiteBarHex="#aaaaaa",
                whiteLineHex=whiteLineHex,
                blackBarHex="#4a7bb7",
                blackLineHex=blackLineHex
            ),
            config={
                'scrollZoom': False,
                'doubleClick': 'reset',
                'modeBarButtonsToRemove': [
                    'select2d', 'lasso2d', 'zoom2d', 'pan2d',
                    'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'
                ],
                'displayModeBar': False
            },
            style={'flex': '2', 'marginRight': '20px'}
        ),
        html.Div([
            dcc.Dropdown(
                id='select-year',
                options=[{'label': str(y), 'value': y} for y in range(1940, 2020, 10)],
                value=default_year,
                clearable=False,
                style={'width': '100px',
                       'marginBottom': '8px',
                       'marginTop': '200px'}
            ),
            dcc.RadioItems(
                id='select-df',
                options=[
                    {'label': 'Population', 'value': 'all'},
                    {'label': 'Workers', 'value': 'nonZero'},
                ],
                value='nonZero',
                labelStyle={'display': 'block', 'marginRight': '10px'},
                style={'marginBottom': '8px'}
            ),
            html.Div(
                id='side-text',
                children="Hover over the income distributions to see the levels earnings gap.",
                style={
                    'fontSize': '20px',
                    'lineHeight': '1.4',
                    'whiteSpace': 'pre-line',
                    'marginTop': '100px'
                }
            )
        ], style={'flex': '1'})
    ], style={
        'display': 'flex',
        'alignItems': 'flex-start',
        'justifyContent': 'center',
        'gap': '20px',
        'maxWidth': '1100px',
        'margin': '0 auto'
    })
])


# --- Callback ---
@app.callback(
    Output('histo-graph', 'figure'),
    Output('side-text', 'children'),
    Input('histo-graph', 'hoverData'),
    Input('select-year', 'value'),
    Input('select-df', 'value')
)
def update_on_hover_and_select(hoverData, selectedYear, selectedDf):
    if hoverData is None:
        raise dash.exceptions.PreventUpdate

    hover_x = hoverData['points'][0]['x']
    curve_num = hoverData['points'][0]['curveNumber']

    if selectedDf == 'all':
        df = dfAll
    elif selectedDf == 'nonZero':
        df = dfNonZero

    dfYear = df[df['year'] == selectedYear]
    dfWhite = dfYear[dfYear['race'] == 1]
    dfBlack = dfYear[dfYear['race'] == 2]

    if curve_num == 0:
        pct = (dfWhite['lrinc'] <= hover_x).mean() * 100
    elif curve_num == 1:
        pct = (dfBlack['lrinc'] <= hover_x).mean() * 100
    else:
        pct = 50

    pct = max(0.1, min(99.9, pct))

    white_percentile = dfWhite['lrinc'].quantile(pct / 100)
    black_percentile = dfBlack['lrinc'].quantile(pct / 100)
    white_income = np.exp(white_percentile)
    black_income = np.exp(black_percentile)
    income_gap = white_income - black_income

    text = (
        f"A White man at the {ordinal(int(round(pct)))} percentile "
        f"of the White income distribution earned "
        f"${white_income:,.0f}.\n\n\n"
        
        f"A Black man at the {ordinal(int(round(pct)))} percentile "
        f"of the Black income distribution earned "
        f"${black_income:,.0f}.\n\n\n"
        
        f"That's a ${income_gap:,.0f} gap."
    )

    fig = earningsGapHisto(
        df=df,
        y=selectedYear,
        xrange=[0, 14],
        binSize=0.2,
        percentile=pct,
        whiteBarHex="#aaaaaa",
        whiteLineHex=whiteLineHex,
        blackBarHex="#4a7bb7",
        blackLineHex=blackLineHex
    )

    return fig, text

# --- Run Server ---
if __name__ == '__main__':
    app.run_server(debug=False)

