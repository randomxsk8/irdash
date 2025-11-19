import dash
from dash import dcc, html, Output, Input, State
import pandas as pd
import plotly.express as px

# === Caricamento dati ===
albo = pd.read_csv("meta/albo_geno.csv")

mutation_options = [
    {"label": "Mutation 1016", "value": "1016G Mutation Frequency"},
    {"label": "Mutation 1534", "value": "1534C Mutation Frequency"},
]

years = sorted(albo['Sampling Year'].dropna().unique())
dropdown_year_options = [{"label": "Tutti gli anni", "value": "all"}] + [
    {"label": str(year), "value": year} for year in years
]

region_options = [{"label": "Tutte le regioni", "value": "all"}] + [
    {"label": reg, "value": reg} for reg in sorted(albo['Region'].dropna().unique())
]

button_style = {
    'padding': '15px 25px',
    'margin': '10px',
    'border': '2px solid #822433',
    'borderRadius': '30px',
    'backgroundColor': '#f1f1f1',
    'fontWeight': 'bold',
    'fontSize': '18px',
    'cursor': 'pointer',
    'transition': '0.3s',
    'color': '#000',
}
selected_style = button_style.copy()
selected_style.update({
    'backgroundColor': '#822433',
    'color': '#fff',
})

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Store(id='selected-mutation-store', data=mutation_options[0]["value"]),

    html.Div([
        html.A(
            html.Img(src='https://www.mosquitoalertitalia.it/wp-content/uploads/2022/04/cropped-Italia-map-2048x333-1.png',
                     style={'height': '70px'}),
            href='https://www.mosquitoalertitalia.it/',
            target='_blank',
            style={'marginRight': '10px'}
        ),
        html.H1(
            "Aedes albopictus Italian Insecticide Resistance Map",
            style={
                'color': '#ffffff',
                'fontSize': '36px',
                'fontStyle': 'italic',
                'position': 'absolute',
                'left': '50%',
                'transform': 'translateX(-50%)',
                'margin': -55
            }
        ),
    ], style={
        'backgroundColor': '#822433',
        'padding': '20px',
        'position': 'relative',
        'height': '70px'
    }),

    html.Div(style={'height': '30px'}),

    html.Div([
        html.H4("Seleziona una mutazione genetica:", style={'textAlign': 'center'}),
        html.Div([
            html.Button(
                opt["label"],
                id=opt["value"],
                n_clicks=0,
                style=selected_style if i == 0 else button_style
            ) for i, opt in enumerate(mutation_options)
        ], id='button-container', style={'textAlign': 'center'}),
    ]),

    # Qui mettiamo i dropdown fuori dalla callback, fissi, affiancati al box info
    html.Div([
        html.Div([
            html.H4("Come leggere la mappa"),
            html.Ul([
                html.Li("Il colore indica la frequenza della mutazione genetica associata alla resistenza (dal giallo al rosso)."),
                html.Li("I punti neri indicano che la mutazione è stata cercata ma non trovata (frequenza zero)."),
                html.Li("La dimensione dei punti rappresenta il numero di individui genotipizzati."),
                html.Li("Passa il mouse sopra il punto per informazioni sul campione."),
                html.Li("Usa la rotella del mouse per zoomare."),
                html.Li("Puoi filtrare la mappa per anno e regione."),
            ], style={'fontSize': '14px', 'lineHeight': '2.0', 'color': '#333'})
        ], style={
            'backgroundColor': '#f9f9f9',
            'border': '1px solid #ccc',
            'padding': '10px 15px',
            'borderRadius': '8px',
            'maxWidth': '750px',
            'textAlign': 'left',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        }),

        html.Div([
            html.H4("Filtra per", style={'textAlign': 'center', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='year-dropdown-inline',
                options=dropdown_year_options,
                value='all',
                clearable=False,
                style={'width': '200px', 'marginBottom': '20px'}
            ),
            dcc.Dropdown(
                id='region-dropdown-inline',
                options=region_options,
                value='all',
                clearable=False,
                style={'width': '200px'}
            )
        ], style={
            'marginLeft': '30px',
            'display': 'flex',
            'flexDirection': 'column',
            'justifyContent': 'center',
            'alignItems': 'center'
        }),

    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'flex-start',
        'margin': '20px auto',
        'maxWidth': '900px',
    }),

    html.Div(id='output-layout', style={'padding': '20px', 'backgroundColor': '#ffffff', 'paddingBottom': '150px'}),

    html.Div(
        children=[html.P("© 2025 - RandomXSk8", style={'textAlign': 'center', 'color': '#ffffff'})],
        style={'backgroundColor': '#822433', 'padding': '10px', 'position': 'fixed', 'bottom': '0', 'width': '100%'}
    )
])


@app.callback(
    Output('selected-mutation-store', 'data'),
    [Input(opt["value"], "n_clicks") for opt in mutation_options],
    State('selected-mutation-store', 'data')
)
def update_selected_mutation(*args):
    n_clicks = args[:-1]
    current_mutation = args[-1]
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_mutation
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    return trigger_id if trigger_id in [opt["value"] for opt in mutation_options] else current_mutation


@app.callback(
    [Output("output-layout", "children")] +
    [Output(opt["value"], "style") for opt in mutation_options],
    Input('selected-mutation-store', 'data'),
    Input('year-dropdown-inline', 'value'),
    Input('region-dropdown-inline', 'value')
)
def update_map_and_buttons(selected_mutation, selected_year, selected_region):
    if selected_mutation not in albo.columns:
        map_content = html.P("Mutazione non trovata.")
    else:
        df_filtered = albo.dropna(subset=['lat', 'long', selected_mutation])

        if selected_year != "all":
            df_filtered = df_filtered[df_filtered['Sampling Year'] == selected_year]
        if selected_region != "all":
            df_filtered = df_filtered[df_filtered['Region'] == selected_region]

        if df_filtered.empty:
            map_content = html.P("Nessun dato disponibile per questa combinazione.")
        else:
            size_col = 'Number of Individuals Genotyped 1016' if selected_mutation == "1016G Mutation Frequency" else 'Number of Individuals Genotyped 1534'
            df_filtered = df_filtered.copy()
            df_filtered['size'] = df_filtered[size_col].fillna(1).clip(lower=7)

            df_nonzero = df_filtered[df_filtered[selected_mutation] > 0]
            fig = px.scatter_mapbox(
                df_nonzero,
                lat="lat",
                lon="long",
                color=selected_mutation,
                size='size',
                hover_name='Municipality',
                hover_data={
                    'Location': True,
                    'Sampling Year': True,
                    selected_mutation: True,
                    size_col: True,
                    'source/contributor': True,
                    'lat': False,
                    'long': False,
                    'size': False
                },
                color_continuous_scale='YlOrRd',
                range_color=(0, 0.7),
                size_max=20,
                zoom=5,
                center={"lat": 41.8719, "lon": 12.5674},
                mapbox_style="open-street-map"
            )

            df_zero = df_filtered[df_filtered[selected_mutation] == 0]
            if not df_zero.empty:
                fig.add_scattermapbox(
                    lat=df_zero['lat'],
                    lon=df_zero['long'],
                    mode='markers',
                    marker=dict(size=df_zero['size'].clip(upper=12), color='black'),
                    hovertext=df_zero.apply(
                        lambda row: (
                            f"<b>{row['Municipality'] or 'Località sconosciuta'}</b><br>"
                            f"Location: {row['Location']}<br>"
                            f"Sampling Year: {row['Sampling Year']}<br>"
                            f"{selected_mutation}: 0<br>"
                            f"{size_col}: {row.get(size_col, 'N/A')}<br>"
                            f"source/contributor: {row['source/contributor']}"
                        ), axis=1
                    ),
                    hoverinfo='text',
                    showlegend=False
                )

            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

            map_content = dcc.Graph(
                figure=fig,
                style={'width': '80vw', 'height': '65vh', 'margin': 'auto'},
                config={
                    'scrollZoom': True,
                    'modeBarButtonsToAdd': ['toImage'],
                    'toImageButtonOptions': {
                        'format': 'png',
                        'filename': 'insecticide_resistance_map',
                        'height': 600,
                        'width': 900,
                        'scale': 4
                    }
                }
            )

    styles = [selected_style if opt["value"] == selected_mutation else button_style for opt in mutation_options]
    return [map_content] + styles


if __name__ == "__main__":
    app.run(debug=False)

