import dash
from dash import Dash, dcc, html, Input, Output
import pandas as pd
from scipy.stats import percentileofscore
import math
import numpy as np
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from apps.helpers import readData
from apps.helpers import ordinal

dfAll, dfNonZero = readData()

def earningsRankGapHisto(df, y, xrange, binSize,
                         whiteRank,
                         blackBarHex, whiteBarHex):

    dfYear = df[df['year'] == y]
    dfYearW = dfYear[dfYear['race'] == 1]
    dfYearB = dfYear[dfYear['race'] == 2]

    logIncome = dfYearW["lrinc"].quantile(whiteRank / 100)
    income = np.exp(logIncome)
    blackRank = percentileofscore(dfYearB["lrinc"], logIncome, kind='weak')

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

    white_norm_pos = (logIncome - xrange[0]) / (xrange[1] - xrange[0])

    shapes.append(dict(
        type="line", xref="paper", yref="paper",
        x0=white_norm_pos, y0=0, x1=white_norm_pos, y1=1,
        line=dict(color="black", width=4)
    ))

    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=white_norm_pos,
        y=.65,
        text = f"{ordinal(int(round(whiteRank)))}: ${income:,.0f}",
        showarrow=False,
        textangle=-90,
        xshift=18,
        font=dict(
            color="black",
            size=12
        )
    )

    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=white_norm_pos,
        y=.01,
        text=f"{ordinal(int(round(blackRank)))}: ${income:,.0f}",
        showarrow=False,
        textangle=-90,
        xshift=18,
        font=dict(
            color="black",
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
        linecolor=whiteBarHex,
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
        linecolor=blackBarHex,
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

default_whiteRank = 50
default_year = 1940
default_df = dfNonZero  # Assuming you have this pre-defined

app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='histo-graph',
            figure=earningsRankGapHisto(
                df=default_df,
                y=default_year,
                xrange=[0, 14],
                binSize=0.2,
                whiteRank=default_whiteRank,
                whiteBarHex="#aaaaaa",
                blackBarHex="#4a7bb7",
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
                style={'width': '100px', 'marginBottom': '8px', 'marginTop': '200px'}
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
                children="Hover over the income distributions to see the earnings rank gap.",
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

    df = dfAll if selectedDf == 'all' else dfNonZero
    dfYear = df[df['year'] == selectedYear]
    dfWhite = dfYear[dfYear['race'] == 1]
    dfBlack = dfYear[dfYear['race'] == 2]

    # Compute whiteRank based on hover_x regardless of curve
    whiteRank = percentileofscore(dfWhite['lrinc'], hover_x, kind='weak')
    # Income value at that percentile in White dist
    logIncome = np.percentile(dfWhite['lrinc'], whiteRank)
    income = np.exp(logIncome)
    # Where does that same log income lie in Black dist?
    blackRank = percentileofscore(dfBlack['lrinc'], logIncome, kind='weak')
    rankGap = round(blackRank) - round(whiteRank)

    text = (
        f"A Black man earning ${income:,.0f} is at the {ordinal(int(round(blackRank)))} percentile "
        f"of the Black income distribution.\n\n"
        f"A White man earning ${income:,.0f} is at the {ordinal(int(round(whiteRank)))} percentile "
        f"of the White income distribution.\n\n"
        f"That's a {rankGap:+} percentile point gap."
    )

    fig = earningsRankGapHisto(
        df=df,
        y=selectedYear,
        xrange=[0, 14],
        binSize=0.2,
        whiteRank=whiteRank,
        whiteBarHex="#aaaaaa",
        blackBarHex="#4a7bb7",
    )

    return fig, text

# --- Run Server ---
if __name__ == '__main__':
    app.run_server(debug=False)