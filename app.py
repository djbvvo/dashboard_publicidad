import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os

# 1. Cargar y preparar los datos
df = pd.read_csv("Advertising.csv", index_col=0)
df['Sinergia_TV_Radio'] = df['TV'] * df['Radio']

# 2. Inicializar la aplicación adaptada para el proxy de Binder
# Esto detecta automáticamente la URL generada por Binder para cargar los gráficos
prefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX', '')
if prefix:
    app = dash.Dash(__name__, requests_pathname_prefix=f"{prefix}proxy/8050/")
else:
    app = dash.Dash(__name__)

server = app.server

# 3. Colores y estilos
colores = {
    'fondo': '#F8F9FA',
    'texto_principal': '#2C3E50',
    'acento': '#2980B9'
}

estilo_tarjeta = {
    'backgroundColor': 'white', 
    'padding': '20px', 
    'borderRadius': '10px', 
    'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.1)',
    'marginBottom': '20px'
}

# 4. Diseño de la interfaz
app.layout = html.Div(style={'fontFamily': 'Segoe UI, Arial, sans-serif', 'maxWidth': '1100px', 'margin': '0 auto', 'padding': '20px', 'backgroundColor': colores['fondo']}, children=[
    
    html.H1("Dashboard: Impacto de la Inversión Publicitaria", style={'color': colores['texto_principal'], 'textAlign': 'center', 'marginBottom': '30px'}),
    
    html.Div(style=estilo_tarjeta, children=[
        dcc.Markdown('''
        ### Contexto y Descubrimientos del Modelo
        A lo largo del proyecto, analizamos cómo la inversión en distintos medios afecta las ventas. Nuestro modelo de regresión lineal múltiple inicial identificó que la **Televisión** y la **Radio** tienen una fuerte asociación positiva con las ventas, mientras que los periódicos aportan muy poco.
        
        **La mejora iterativa:** Al detectar que el modelo inicial no capturaba toda la complejidad de los datos, creamos una nueva característica llamada **Sinergia TV-Radio** (la multiplicación de ambas inversiones). Al aplicar este cambio junto con una regularización Ridge (Alpha = 1), logramos un modelo altamente predictivo, **elevando el R² a 0.965**.
        ''', style={'color': colores['texto_principal'], 'lineHeight': '1.6'})
    ]),

    html.Div(style=estilo_tarjeta, children=[
        html.Label("Selecciona la métrica publicitaria para analizar su relación directa con las ventas:", style={'fontWeight': 'bold', 'color': colores['texto_principal']}),
        dcc.Dropdown(
            id='selector-variable',
            options=[
                {'label': 'Televisión (TV)', 'value': 'TV'},
                {'label': 'Radio', 'value': 'Radio'},
                {'label': 'Periódico (Newspaper)', 'value': 'Newspaper'},
                {'label': 'Sinergia (TV x Radio)', 'value': 'Sinergia_TV_Radio'}
            ],
            value='Sinergia_TV_Radio',
            clearable=False,
            style={'marginTop': '10px', 'width': '50%'}
        )
    ]),

    html.Div(style=estilo_tarjeta, children=[
        dcc.Graph(id='grafico-principal')
    ])
])

# 5. Interactividad
@app.callback(
    Output('grafico-principal', 'figure'),
    [Input('selector-variable', 'value')]
)
def actualizar_grafico(variable_seleccionada):
    nombres_legibles = {
        'TV': 'Inversión en Televisión',
        'Radio': 'Inversión en Radio',
        'Newspaper': 'Inversión en Periódicos',
        'Sinergia_TV_Radio': 'Sinergia (TV x Radio)'
    }
    
    fig = px.scatter(
        df, 
        x=variable_seleccionada, 
        y='Sales', 
        trendline='ols',
        title=f'Análisis: {nombres_legibles[variable_seleccionada]} vs Ventas',
        labels={variable_seleccionada: nombres_legibles[variable_seleccionada], 'Sales': 'Ventas (Miles)'},
        color_discrete_sequence=[colores['acento']],
        template='plotly_white'
    )
    
    fig.update_layout(
        title_x=0.5, 
        font=dict(family="Segoe UI, Arial, sans-serif"),
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# 6. Ejecutar la aplicación (Configurado para Binder)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=False)
