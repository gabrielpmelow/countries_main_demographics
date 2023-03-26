from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import requests


app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
                html.Div([
                    html.H5("Countries' main demographics (World Bank 1960 - 2015)"),
                    dcc.Graph(id='flag',
                    style={'margin-left' : '55px', 'margin-bottom' : '10px'})
                ], style={'display' : 'flex'}),
                dcc.Dropdown(options = list(requests.get('https://countries--data-default-rtdb.firebaseio.com/.json').json().keys()), id='countries', 
                                    placeholder='select the country', value='Afghanistan'),
                dcc.Dropdown(options = list(range(1960, 2016)), id='years', value='1960', placeholder='select the year'),
                dcc.Graph(id='map'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                    html.Span(f'Literacy rate, youth total (% of people ages 15-24)'),
                                    html.H3(style={"color" : '#add8e6'}, id="literacy-rate")
                            ], style={"box-shadow" : "0 1px 1px 0", "color" : "#FFFFFF", 'text-align' : 'center'})
                        
                        ]),

                        dbc.Card([
                            dbc.CardBody([
                                    html.Span(f'Unemployment, total (% of total labor force)'),
                                    html.H3(style={"color" : "#B22222"}, id="unemployment")
                            ], style={"box-shadow" : "0 1px 1px 0", "color" : "#FFFFFF", 'text-align' : 'center'})
                          ], style={'margin-top' : '15px'}),

                        dbc.Card([
                            dbc.CardBody([
                                    html.Span('Mortality rate, infant (per 1,000 live births)'),
                                    html.H3(style={"color" : "#32CD32"}, id="infant-mortality")
                            ], style={"box-shadow" : "0 1px 1px 0", "color" : "#FFFFFF", 'text-align' : 'center'})
                        
                        ], style={'margin-top' : '15px'})

                        ], md=4),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                    html.Span(f'Improved sanitation facilities (% of population with access)'),
                                    html.H3(style={"color" : "#32CD32"}, id="sanitation-facilities")
                            ], style={"box-shadow" : "0 1px 1px 0", "color" : "#FFFFFF", 'text-align' : 'center'})
                        
                        ]),

                        dbc.Card([
                            dbc.CardBody([
                                    html.Span(f'Improved water source (% of population with access)'),
                                    html.H3(style={"color" : '#add8e6'}, id="water-source")
                            ], style={"box-shadow" : "0 1px 1px 0", "color" : "#FFFFFF", 'text-align' : 'center'})
                          ], style={'margin-top' : '15px'}),

                        dbc.Card([
                            dbc.CardBody([
                                    html.Span('Fertility rate, total (births per woman)'),
                                    html.H3(style={"color" : '#add8e6'}, id="fertility-rate")
                            ], style={"box-shadow" : "0 1px 1px 0", "color" : "#FFFFFF", 'text-align' : 'center'})
                        ], style={'margin-top' : '15px'})
                    ], md=4),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                    html.Span(f'GNI per capita, Atlas method (current US$)'),
                                    html.H3(style={"color" : "#32CD32"}, id="gni-percapita")
                            ], style={"box-shadow" : "0 1px 1px 0", "color" : "#FFFFFF", 'text-align' : 'center'})
                        
                        ]),

                        dbc.Card([
                            dbc.CardBody([
                                    html.Span('Population, total'),
                                    html.H3(style={"color" : '#add8e6'}, id="population-total")
                            ], style={"box-shadow" : "0 1px 1px 0", "color" : "#FFFFFF", 'text-align' : 'center'})
                          ], style={'margin-top' : '15px'}),

                        dbc.Card([
                            dbc.CardBody([
                                    html.Span('Death rate, crude (per 1,000 people)'),
                                    html.H3(style={"color" : "#B22222"}, id="death-rate")
                            ], style={"box-shadow" : "0 1px 1px 0", "color" : "#FFFFFF", 'text-align' : 'center'})
                        ], style={'margin-top' : '15px'})
                    ], md=4)
                ], style={'margin-top' : '5px'}),            
        ], md=6),

        dbc.Col([
                dcc.Graph(id='pyramid',
                style={"width" : "100vw"}),
                dcc.Graph(id='line-chart'), dcc.Store(id='store-data', data=requests.get('https://countries--data-default-rtdb.firebaseio.com/.json').json(), storage_type='memory'), 
        ], md=6)])], fluid=True, style={"padding" : "15px"})

app.clientside_callback(    
        """
        function(country, year, data) {
            let dic_pcountry = {};
            let array_data = [];
            let dic = {};
            dic_pcountry = data[country];
            array_data = [dic_pcountry['flag'], dic_pcountry['inmap'], dic_pcountry['population_growth']];
            dic = dic_pcountry['data_per_year'][year];
            array_data.push(dic['pyramid'], dic['literacy_rate'], dic['unemployment'], dic['sanitation_facilities'], dic['water_source'], dic['gni_per_capita'],
                            dic['total_population'], dic['death_rate'], dic['infant_mortality'], dic['fertility_rate']);
            return array_data;
        }

        """,
    [Output('flag', 'figure'),
     Output('map', 'figure'),
     Output('line-chart', 'figure'),
     Output('pyramid', 'figure'),
     Output('literacy-rate', 'children'),
     Output('unemployment', 'children'),
     Output('sanitation-facilities', 'children'),
     Output('water-source', 'children'),
     Output('gni-percapita', 'children'),
     Output('population-total', 'children'),
     Output('death-rate', 'children'),
     Output('infant-mortality', 'children'),
     Output('fertility-rate', 'children')],
     [
      Input('countries', 'value'),  
      Input('years', 'value'),
      Input('store-data', 'data')])



if __name__ == '__main__':
    app.run_server(debug=True)