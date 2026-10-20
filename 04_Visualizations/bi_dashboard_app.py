# BUSINESS INTELLIGENCE DASHBOARD FOR BITCOIN TRADING
## Executive Dashboard Implementation

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Initialize Dash App
app = dash.Dash(__name__)
app.title = "Bitcoin Trading Intelligence Dashboard"

# Define Layout
app.layout = html.Div([
    html.Div([
        html.H1("Bitcoin Trading Intelligence Dashboard", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'fontFamily': 'Times New Roman'}),
        html.H3("Real-time Business Intelligence for Cryptocurrency Trading", 
                style={'textAlign': 'center', 'color': '#7f8c8d', 'marginBottom': '30px'})
    ]),
    
    # KPI Summary Cards
    html.Div([
        html.Div([
            html.H4("Current Price", style={'color': '#2c3e50', 'textAlign': 'center'}),
            html.H2(id='current-price', children="$45,234.56", 
                   style={'color': '#27ae60', 'textAlign': 'center', 'fontSize': '24px'})
        ], className='kpi-card', style={'width': '24%', 'display': 'inline-block', 'margin': '0.5%'}),
        
        html.Div([
            html.H4("24h Change", style={'color': '#2c3e50', 'textAlign': 'center'}),
            html.H2(id='daily-change', children="+2.34%", 
                   style={'color': '#27ae60', 'textAlign': 'center', 'fontSize': '24px'})
        ], className='kpi-card', style={'width': '24%', 'display': 'inline-block', 'margin': '0.5%'}),
        
        html.Div([
            html.H4("Prediction Accuracy", style={'color': '#2c3e50', 'textAlign': 'center'}),
            html.H2(id='accuracy', children="87.3%", 
                   style={'color': '#3498db', 'textAlign': 'center', 'fontSize': '24px'})
        ], className='kpi-card', style={'width': '24%', 'display': 'inline-block', 'margin': '0.5%'}),
        
        html.Div([
            html.H4("Sharpe Ratio", style={'color': '#2c3e50', 'textAlign': 'center'}),
            html.H2(id='sharpe-ratio', children="1.45", 
                   style={'color': '#9b59b6', 'textAlign': 'center', 'fontSize': '24px'})
        ], className='kpi-card', style={'width': '24%', 'display': 'inline-block', 'margin': '0.5%'})
    ], style={'backgroundColor': '#ecf0f1', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '30px'}),
    
    # Main Charts Row
    html.Div([
        # Price Chart with Predictions
        html.Div([
            dcc.Graph(id='price-chart')
        ], style={'width': '65%', 'display': 'inline-block', 'padding': '10px'}),
        
        # Technical Indicators
        html.Div([
            dcc.Graph(id='technical-indicators')
        ], style={'width': '34%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    
    # Second Row - Risk Analysis
    html.Div([
        # Risk Metrics
        html.Div([
            dcc.Graph(id='risk-metrics')
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        
        # Trading Signals
        html.Div([
            html.H4("Active Trading Signals", style={'color': '#2c3e50'}),
            html.Div(id='trading-signals', children=[
                html.Div([
                    html.Span("● ", style={'color': '#27ae60', 'fontSize': '20px'}),
                    html.Span("BUY Signal - Strong momentum detected", style={'marginLeft': '10px'})
                ], style={'margin': '10px', 'padding': '10px', 'backgroundColor': '#d5f4e6', 'borderRadius': '5px'}),
                html.Div([
                    html.Span("● ", style={'color': '#e74c3c', 'fontSize': '20px'}),
                    html.Span("HOLD - High volatility expected", style={'marginLeft': '10px'})
                ], style={'margin': '10px', 'padding': '10px', 'backgroundColor': '#fadbd8', 'borderRadius': '5px'})
            ])
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    
    # Model Performance Comparison
    html.Div([
        html.H4("Model Performance Comparison", style={'color': '#2c3e50', 'textAlign': 'center'}),
        dcc.Graph(id='model-comparison')
    ], style={'padding': '20px'}),
    
    # Auto-refresh component
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # Update every minute
        n_intervals=0
    )
])

# Callbacks for dynamic updates
@app.callback(
    [Output('current-price', 'children'),
     Output('daily-change', 'children'),
     Output('accuracy', 'children'),
     Output('sharpe-ratio', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_kpis(n):
    # Simulate real-time data updates
    current_price = f"${np.random.uniform(43000, 47000):.2f}"
    daily_change = f"{np.random.uniform(-5, 5):.2f}%"
    accuracy = f"{np.random.uniform(85, 92):.1f}%"
    sharpe_ratio = f"{np.random.uniform(1.2, 1.8):.2f}"
    
    return current_price, daily_change, accuracy, sharpe_ratio

@app.callback(
    Output('price-chart', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_price_chart(n):
    # Generate sample data
    dates = pd.date_range(end=datetime.now(), periods=100, freq='H')
    actual_prices = np.cumsum(np.random.randn(100) * 100) + 45000
    predicted_prices = actual_prices + np.random.randn(100) * 200
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates, y=actual_prices,
        mode='lines', name='Actual Price',
        line=dict(color='#2c3e50', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=dates, y=predicted_prices,
        mode='lines', name='Predicted Price',
        line=dict(color='#3498db', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title='Bitcoin Price Prediction (Last 100 Hours)',
        xaxis_title='Time',
        yaxis_title='Price (USD)',
        template='plotly_white',
        height=400
    )
    
    return fig

@app.callback(
    Output('technical-indicators', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_technical_indicators(n):
    # Generate RSI data
    dates = pd.date_range(end=datetime.now(), periods=50, freq='H')
    rsi = np.random.uniform(20, 80, 50)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates, y=rsi,
        mode='lines', name='RSI',
        line=dict(color='#e74c3c', width=2)
    ))
    
    # Add overbought/oversold lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
    
    fig.update_layout(
        title='RSI Technical Indicator',
        xaxis_title='Time',
        yaxis_title='RSI Value',
        template='plotly_white',
        height=400,
        yaxis=dict(range=[0, 100])
    )
    
    return fig

@app.callback(
    Output('risk-metrics', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_risk_metrics(n):
    # Risk metrics data
    metrics = ['VaR (95%)', 'Max Drawdown', 'Volatility', 'Beta']
    values = [2.3, 8.5, 4.2, 1.1]
    
    fig = go.Figure(data=[
        go.Bar(x=metrics, y=values, marker_color='#e67e22')
    ])
    
    fig.update_layout(
        title='Risk Metrics Dashboard',
        xaxis_title='Risk Metric',
        yaxis_title='Value (%)',
        template='plotly_white',
        height=400
    )
    
    return fig

@app.callback(
    Output('model-comparison', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_model_comparison(n):
    # Model comparison data
    models = ['LSTM', 'GRU', 'RandomForest', 'Ensemble']
    rmse = [0.023, 0.025, 0.028, 0.021]
    accuracy = [87.3, 86.1, 84.5, 88.2]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=models, y=rmse,
        name='RMSE',
        marker_color='#3498db',
        yaxis='y'
    ))
    
    fig.add_trace(go.Bar(
        x=models, y=accuracy,
        name='Accuracy (%)',
        marker_color='#27ae60',
        yaxis='y2'
    ))
    
    fig.update_layout(
        title='Model Performance Comparison',
        xaxis_title='Models',
        template='plotly_white',
        height=400,
        yaxis=dict(title='RMSE', side='left'),
        yaxis2=dict(title='Accuracy (%)', side='right', overlaying='y')
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
