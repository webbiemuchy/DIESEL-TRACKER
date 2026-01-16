"""

=================J-INVESTMENTS Fleet Management System========================

"""
import dash
from dash import dcc, html, Input, Output, State, dash_table, ctx, ALL, MATCH
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from io import BytesIO
import base64
from flask import session
import secrets

from config import *
from database import *

# ==================== APPLICATION INITIALIZATION ====================
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="J-INVESTMENTS Fleet Management",
    update_title=None
)

server = app.server

# Session configuration
server.config.update(
    SECRET_KEY=secrets.token_hex(32),
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(days=7)
)

# ==================== UTILITY FUNCTIONS ====================
def load_logo():
    """Load and encode J-INVESTMENTS logo"""
    try:
        with open('assets/J-INVESTMENTS-LOGO.svg', 'r') as f:
            svg_content = f.read()
        encoded = base64.b64encode(svg_content.encode()).decode()
        return f"data:image/svg+xml;base64,{encoded}"
    except Exception as e:
        print(f"Warning: Could not load logo - {e}")
        return None

def create_notification(message, color="success"):
    """Create notification alert"""
    return dbc.Alert(message, color=color, duration=4000, dismissable=True)

# ==================== LOGIN PAGE ====================
def create_login_page():
    logo_src = load_logo()
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    # Logo at top
                    html.Div([
                        html.Img(src=logo_src, style={
                            'width': '350px',
                            'marginBottom': '30px',
                            'filter': f'drop-shadow(0 0 30px rgba(255, 180, 0, 0.6))'
                        }) if logo_src else None,
                    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
                    
                    # Decorative geometric shapes
                    html.Div([
                        # Shape 1 - diagonal bar
                        html.Div(style={
                            'position': 'absolute',
                            'width': '200px',
                            'height': '8px',
                            'background': f'linear-gradient(90deg, {COLORS["cat_yellow"]}, rgba(255,180,0,0.5))',
                            'transform': 'rotate(-45deg)',
                            'borderRadius': '10px',
                            'top': '30%',
                            'left': '10%',
                            'boxShadow': f'0 4px 15px rgba(255,180,0,0.4)'
                        }),
                        # Shape 2 - diagonal bar
                        html.Div(style={
                            'position': 'absolute',
                            'width': '150px',
                            'height': '8px',
                            'background': f'linear-gradient(90deg, {COLORS["cat_yellow_dark"]}, rgba(204,144,0,0.5))',
                            'transform': 'rotate(-45deg)',
                            'borderRadius': '10px',
                            'top': '45%',
                            'left': '5%',
                            'boxShadow': f'0 4px 15px rgba(204,144,0,0.4)'
                        }),
                        # Shape 3 - diagonal bar
                        html.Div(style={
                            'position': 'absolute',
                            'width': '120px',
                            'height': '8px',
                            'background': f'linear-gradient(90deg, {COLORS["cat_yellow"]}, rgba(255,180,0,0.6))',
                            'transform': 'rotate(-45deg)',
                            'borderRadius': '10px',
                            'top': '60%',
                            'left': '15%',
                            'boxShadow': f'0 4px 15px rgba(255,180,0,0.4)'
                        }),
                        # Shape 4 - circle
                        html.Div(style={
                            'position': 'absolute',
                            'width': '180px',
                            'height': '180px',
                            'background': f'radial-gradient(circle, rgba(255,180,0,0.3), transparent)',
                            'borderRadius': '50%',
                            'bottom': '15%',
                            'right': '10%',
                            'boxShadow': f'0 8px 30px rgba(255,180,0,0.3)'
                        }),
                        # Shape 5 - small circle
                        html.Div(style={
                            'position': 'absolute',
                            'width': '100px',
                            'height': '100px',
                            'background': f'radial-gradient(circle, rgba(255,180,0,0.4), transparent)',
                            'borderRadius': '50%',
                            'bottom': '25%',
                            'right': '25%',
                            'boxShadow': f'0 6px 20px rgba(255,180,0,0.3)'
                        })
                    ], style={
                        'position': 'absolute',
                        'top': '0',
                        'left': '0',
                        'width': '100%',
                        'height': '100%',
                        'overflow': 'hidden',
                        'zIndex': '1'
                    })
                    
                ], style={
                    'height': '100vh',
                    'padding': '60px',
                    'display': 'flex',
                    'flexDirection': 'column',
                    'justifyContent': 'center',
                    'background': f'linear-gradient(135deg, {COLORS["bg_dark"]} 0%, {COLORS["carbon"]} 50%, {COLORS["steel"]} 100%)',
                    'position': 'relative',
                    'overflow': 'hidden'
                })
            ], md=6, style={'padding': '0'}),
            
            # Right side - Dark login panel
            dbc.Col([
                html.Div([
                    # Login title
                    html.H2("USER LOGIN", style={
                        'color': COLORS['cat_yellow'],
                        'fontSize': '1.5rem',
                        'fontWeight': '600',
                        'textAlign': 'center',
                        'marginBottom': '40px',
                        'letterSpacing': '2px',
                        'textTransform': 'uppercase'
                    }),
                    
                    # Login form
                    dbc.Form([
                        # Username field
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-user", style={
                                    'color': COLORS['cat_yellow'],
                                    'fontSize': '1.2rem'
                                }),
                            ], style={
                                'position': 'absolute',
                                'left': '15px',
                                'top': '50%',
                                'transform': 'translateY(-50%)',
                                'zIndex': '1'
                            }),
                            dbc.Input(
                                id="login-username",
                                type="text",
                                placeholder="Username",
                                style={
                                    'paddingLeft': '45px',
                                    'height': '50px',
                                    'border': f'2px solid #333',
                                    'borderRadius': '25px',
                                    'fontSize': '1rem',
                                    'backgroundColor': COLORS['carbon'],
                                    'color': COLORS['text_bright'],
                                    'transition': 'all 0.3s ease'
                                },
                                className="login-input-dark"
                            )
                        ], style={'position': 'relative', 'marginBottom': '25px'}),
                        
                        # Password field
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-lock", style={
                                    'color': COLORS['cat_yellow'],
                                    'fontSize': '1.2rem'
                                }),
                            ], style={
                                'position': 'absolute',
                                'left': '15px',
                                'top': '50%',
                                'transform': 'translateY(-50%)',
                                'zIndex': '1'
                            }),
                            dbc.Input(
                                id="login-password",
                                type="password",
                                placeholder="Password",
                                style={
                                    'paddingLeft': '45px',
                                    'height': '50px',
                                    'border': f'2px solid #333',
                                    'borderRadius': '25px',
                                    'fontSize': '1rem',
                                    'backgroundColor': COLORS['carbon'],
                                    'color': COLORS['text_bright'],
                                    'transition': 'all 0.3s ease'
                                },
                                className="login-input-dark"
                            )
                        ], style={'position': 'relative', 'marginBottom': '30px'}),
                        
                        # Login button
                        dbc.Button(
                            "LOGIN",
                            id="btn-login",
                            n_clicks=0,
                            style={
                                'width': '100%',
                                'height': '50px',
                                'borderRadius': '25px',
                                'fontSize': '1rem',
                                'fontWeight': '700',
                                'letterSpacing': '2px',
                                'background': f'linear-gradient(135deg, {COLORS["cat_yellow"]} 0%, {COLORS["cat_yellow_dark"]} 100%)',
                                'border': 'none',
                                'color': '#000',
                                'cursor': 'pointer',
                                'transition': 'all 0.3s ease',
                                'boxShadow': f'0 4px 15px rgba(255, 180, 0, 0.4)',
                                'textTransform': 'uppercase'
                            },
                            className="login-button-dark"
                        )
                    ]),
                    
                    html.Div(id="login-error", style={'marginTop': '20px'})
                    
                ], style={
                    'maxWidth': '400px',
                    'margin': '0 auto',
                    'padding': '40px'
                })
            ], md=6, style={
                'padding': '0',
                'backgroundColor': COLORS['bg_dark'],
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center',
                'minHeight': '100vh'
            })
        ], style={'margin': '0'}, className='g-0')
    ], style={
        'margin': '0',
        'padding': '0',
        'overflow': 'hidden'
    })

# ==================== HEADER COMPONENT ====================
def create_header(user_data):
    """Create application header with navigation"""
    logo_src = load_logo()
    
    # Determine which tabs to show based on permissions
    tabs = [
        dbc.Tab(label="Refueling", tab_id="refueling", 
                style={'color': COLORS['text_dim']}, 
                active_label_style={'color': COLORS['cat_yellow']}),
        dbc.Tab(label="Fleet Assets", tab_id="fleet",
                style={'color': COLORS['text_dim']}, 
                active_label_style={'color': COLORS['cat_yellow']}),
        dbc.Tab(label="Operators", tab_id="operators",
                style={'color': COLORS['text_dim']}, 
                active_label_style={'color': COLORS['cat_yellow']}),
        dbc.Tab(label="Analytics", tab_id="analytics",
                style={'color': COLORS['text_dim']}, 
                active_label_style={'color': COLORS['cat_yellow']}),
        dbc.Tab(label="Settings", tab_id="settings",
                style={'color': COLORS['text_dim']}, 
                active_label_style={'color': COLORS['cat_yellow']}),
    ]
    
    # Add user management tab for admins
    if check_permission(user_data, 'users', 'write'):
        tabs.append(
            dbc.Tab(label="Users", tab_id="users",
                    style={'color': COLORS['text_dim']}, 
                    active_label_style={'color': COLORS['cat_yellow']})
        )
    
    return html.Div([
        # Header bar
        dbc.Navbar([
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.Img(src=logo_src, height="45px", 
                                style={'marginRight': '15px'}) if logo_src else None,
                        html.Div([
                            html.H1("J-INVESTMENTS", style={
                                'color': COLORS['cat_yellow'],
                                'fontSize': '1.4rem',
                                'margin': '0',
                                'fontWeight': 'bold',
                                'letterSpacing': '2px'
                            }),
                            html.P("Fleet Management System", style={
                                'color': COLORS['text_dim'],
                                'fontSize': '0.75rem',
                                'margin': '0',
                                'letterSpacing': '0.5px'
                            })
                        ], style={'display': 'inline-block', 'verticalAlign': 'middle'})
                    ], width="auto", style={'display': 'flex', 'alignItems': 'center'}),
                ], className="g-0", style={'width': '100%'}),
                
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Span(f"Welcome, {user_data['full_name']}", style={
                                'color': COLORS['text_bright'],
                                'marginRight': '20px',
                                'fontWeight': '500'
                            }),
                            html.Span(f"Role: {user_data['role'].replace('_', ' ').title()}", style={
                                'color': COLORS['text_dim'],
                                'fontSize': '0.85rem',
                                'marginRight': '20px',
                                'padding': '4px 12px',
                                'background': 'rgba(255, 180, 0, 0.1)',
                                'borderRadius': '12px',
                                'border': f"1px solid {COLORS['cat_yellow']}"
                            }),
                            dbc.Button("🚪 Sign Out", id="btn-logout", n_clicks=0,
                                      size="sm", style={
                                          **BUTTON_PRIMARY,
                                          'fontSize': '0.85rem',
                                          'padding': '6px 18px'
                                      })
                        ], style={'display': 'flex', 'alignItems': 'center'})
                    ], width="auto")
                ], className="g-0", justify="end", style={'width': '100%'})
            ], fluid=True, style={'display': 'flex', 'justifyContent': 'space-between'})
        ], color="dark", dark=True, sticky="top", style={
            'borderBottom': f'3px solid {COLORS["cat_yellow"]}',
            'padding': '12px 0'
        }),
        
        # Navigation tabs
        dbc.Container([
            dbc.Tabs(
                tabs,
                id="main-tabs",
                active_tab="refueling",
                style={
                    'marginTop': '15px',
                    'marginBottom': '15px'
                }
            )
        ], fluid=True, style={'background': COLORS['bg_dark']})
    ])

# ==================== REFUELING TAB ====================
def create_refueling_tab(user_data):
    """Create refueling management tab"""
    can_write = check_permission(user_data, 'refuels', 'write')
    can_delete = check_permission(user_data, 'refuels', 'delete')
    
    # Get machines and operators for dropdowns
    conn = get_db()
    machines_df = pd.read_sql_query(
        'SELECT id, model FROM machines WHERE status="active" ORDER BY id', conn)
    operators_df = pd.read_sql_query(
        'SELECT id, name, badge FROM operators WHERE status="active" ORDER BY name', conn)
    conn.close()
    
    machine_options = [{'label': f"{row['id']} - {row['model']}", 'value': row['id']} 
                       for _, row in machines_df.iterrows()]
    operator_options = [{'label': f"{row['name']} ({row['badge']})", 'value': row['id']} 
                        for _, row in operators_df.iterrows()]
    
    if not machine_options or not operator_options:
        return dbc.Alert(
            "⚠️ Please add machines and operators before logging refuels.",
            color="warning",
            style={'margin': '20px'}
        )
    
    return html.Div([
        # Add refuel entry form
        dbc.Card([
            dbc.CardHeader(
                html.H4("⛽ New Refueling Entry", style={'color': COLORS['cat_yellow'], 'margin': '0'})
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Machine", style={'fontWeight': 'bold', 'color': COLORS['text_bright']}),
                        dcc.Dropdown(
                            id='refuel-machine',
                            options=machine_options,
                            placeholder="Select Machine",
                            style={'color': '#000'}
                        )
                    ], md=3),
                    dbc.Col([
                        dbc.Label("Operator", style={'fontWeight': 'bold', 'color': COLORS['text_bright']}),
                        dcc.Dropdown(
                            id='refuel-operator',
                            options=operator_options,
                            placeholder="Select Operator",
                            style={'color': '#000'}
                        )
                    ], md=3),
                    dbc.Col([
                        dbc.Label("Usage (hrs/km)", style={'fontWeight': 'bold', 'color': COLORS['text_bright']}),
                        dbc.Input(
                            id='refuel-usage',
                            type='number',
                            min=0,
                            step=0.1,
                            placeholder="0.0",
                            style=INPUT_STYLE
                        )
                    ], md=2),
                    dbc.Col([
                        dbc.Label("Fuel (L)", style={'fontWeight': 'bold', 'color': COLORS['text_bright']}),
                        dbc.Input(
                            id='refuel-fuel',
                            type='number',
                            min=0,
                            step=0.1,
                            placeholder="0.0",
                            style=INPUT_STYLE
                        )
                    ], md=2),
                    dbc.Col([
                        dbc.Label(" ", style={'visibility': 'hidden'}),
                        dbc.Button(
                            "LOG ENTRY",
                            id='btn-add-refuel',
                            n_clicks=0,
                            disabled=not can_write,
                            style={**BUTTON_PRIMARY, 'width': '100%'}
                        )
                    ], md=2)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Notes (optional)", style={
                            'fontWeight': 'bold',
                            'color': COLORS['text_bright'],
                            'marginTop': '15px'
                        }),
                        dbc.Textarea(
                            id='refuel-notes',
                            placeholder="Additional notes or comments...",
                            rows=2,
                            style=INPUT_STYLE
                        )
                    ])
                ], style={'marginTop': '10px'})
            ])
        ], style=CARD_STYLE),
        
        # Filter controls
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H4("📋 Activity History", style={'color': COLORS['cat_yellow'], 'margin': '0'})
                    ], md=6),
                    dbc.Col([
                        dbc.ButtonGroup([
                            dbc.Button("Today", id='btn-refuel-today', n_clicks=0, 
                                      color='warning', size='sm', style=BUTTON_PRIMARY),
                            dbc.Button("This Week", id='btn-refuel-week', n_clicks=0,
                                      color='secondary', size='sm'),
                            dbc.Button("All History", id='btn-refuel-all', n_clicks=0,
                                      color='secondary', size='sm')
                        ], style={'float': 'right'})
                    ], md=6)
                ])
            ])
        ], style=CARD_STYLE),
        
        # Refueling table
        html.Div(id='refueling-table-container'),
        
        # Notifications
        html.Div(id='refuel-notification')
    ])

# ==================== FLEET ASSETS TAB ====================
def create_fleet_tab(user_data):
    """Create fleet assets management tab"""
    can_write = check_permission(user_data, 'machines', 'write')
    can_delete = check_permission(user_data, 'machines', 'delete')
    
    return html.Div([
        # Add machine form
        dbc.Card([
            dbc.CardHeader(
                html.H4("🚜 Add Fleet Asset", style={'color': COLORS['cat_yellow'], 'margin': '0'})
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Machine ID", style={'fontWeight': 'bold', 'color': COLORS['text_bright']}),
                        dbc.Input(
                            id='machine-id',
                            placeholder="e.g., EX-001",
                            style=INPUT_STYLE
                        )
                    ], md=3),
                    dbc.Col([
                        dbc.Label("Model", style={'fontWeight': 'bold', 'color': COLORS['text_bright']}),
                        dbc.Input(
                            id='machine-model',
                            placeholder="e.g., CAT 320",
                            style=INPUT_STYLE
                        )
                    ], md=3),
                    dbc.Col([
                        dbc.Label("Rate (L/hr)", style={'fontWeight': 'bold', 'color': COLORS['text_bright']}),
                        dbc.Input(
                            id='machine-rate',
                            type='number',
                            min=0,
                            step=0.1,
                            placeholder="0.0",
                            style=INPUT_STYLE
                        )
                    ], md=2),
                    dbc.Col([
                        dbc.Label("Capacity (L)", style={'fontWeight': 'bold', 'color': COLORS['text_bright']}),
                        dbc.Input(
                            id='machine-capacity',
                            type='number',
                            min=0,
                            step=1,
                            placeholder="0",
                            style=INPUT_STYLE
                        )
                    ], md=2),
                    dbc.Col([
                        dbc.Label(" ", style={'visibility': 'hidden'}),
                        dbc.Button(
                            "ADD MACHINE",
                            id='btn-add-machine',
                            n_clicks=0,
                            disabled=not can_write,
                            style={**BUTTON_PRIMARY, 'width': '100%'}
                        )
                    ], md=2)
                ])
            ])
        ], style=CARD_STYLE),
        
        # Machines table
        html.Div(id='machines-table-container'),
        
        # Notifications
        html.Div(id='machine-notification')
    ])

# ==================== OPERATORS TAB ====================
def create_operators_tab(user_data):
    """Create operators management tab"""
    can_write = check_permission(user_data, 'operators', 'write')
    can_delete = check_permission(user_data, 'operators', 'delete')
    
    return html.Div([
        # Add operator form
        dbc.Card([
            dbc.CardHeader(
                html.H4("👥 Add Operator", style={'color': COLORS['cat_yellow'], 'margin': '0'})
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Full Name", style={'fontWeight': 'bold', 'color': COLORS['text_bright']}),
                        dbc.Input(
                            id='operator-name',
                            placeholder="e.g., John Doe",
                            style=INPUT_STYLE
                        )
                    ], md=5),
                    dbc.Col([
                        dbc.Label("Badge Number", style={'fontWeight': 'bold', 'color': COLORS['text_bright']}),
                        dbc.Input(
                            id='operator-badge',
                            placeholder="e.g., OP-001",
                            style=INPUT_STYLE
                        )
                    ], md=5),
                    dbc.Col([
                        dbc.Label(" ", style={'visibility': 'hidden'}),
                        dbc.Button(
                            "ADD OPERATOR",
                            id='btn-add-operator',
                            n_clicks=0,
                            disabled=not can_write,
                            style={**BUTTON_PRIMARY, 'width': '100%'}
                        )
                    ], md=2)
                ])
            ])
        ], style=CARD_STYLE),
        
        # Operators table
        html.Div(id='operators-table-container'),
        
        # Notifications
        html.Div(id='operator-notification')
    ])

# ==================== ANALYTICS TAB ====================
def create_analytics_tab(user_data):
    """Create analytics dashboard tab"""
    return html.Div([
        # Date filter
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H4("📊 Analytics Dashboard", style={'color': COLORS['cat_yellow'], 'margin': '0'})
                    ], md=4),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("From:", style={'fontWeight': 'bold', 'marginRight': '10px', 
                                                         'color': COLORS['text_bright']}),
                                
                                dcc.DatePickerSingle(
                                    id='date-from',
                                    date=(datetime.now() - timedelta(days=30)).date(),
                                    display_format='YYYY-MM-DD'
                                 ), 
                                     
                            ], width="auto"),
                            dbc.Col([
                                dbc.Label("To:", style={'fontWeight': 'bold', 'marginRight': '10px',
                                                       'color': COLORS['text_bright']}),
                                
                                dcc.DatePickerSingle(
                                    id='date-to',
                                    date=datetime.now().date(),
                                    display_format='YYYY-MM-DD'
                                ),
                            ], width="auto"),
                            dbc.Col([
                                dbc.Button("Apply", id='btn-apply-dates', n_clicks=0,
                                          size='sm', style=BUTTON_PRIMARY)
                            ], width="auto")
                        ], align="center", className="g-2")
                    ], md=8, style={'textAlign': 'right'})
                ], align="center")
            ])
        ], style=CARD_STYLE),
        
        # KPI cards
        html.Div(id='kpi-cards'),
        
        # Charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("📈 Fuel Usage Trend", style={'color': COLORS['cat_yellow']}),
                        dcc.Graph(id='fuel-trend-chart', config={'displayModeBar': False})
                    ])
                ], style=CARD_STYLE)
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("🔧 Machine Performance", style={'color': COLORS['cat_yellow']}),
                        dcc.Graph(id='machine-performance-chart', config={'displayModeBar': False})
                    ])
                ], style=CARD_STYLE)
            ], md=6)
        ]),
        
        # Operator performance table
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("👤 Operator Performance", style={'color': COLORS['cat_yellow']}),
                        html.Div(id='operator-performance-table')
                    ])
                ], style=CARD_STYLE)
            ])
        ])
    ])

# ==================== SETTINGS TAB ====================
def create_settings_tab(user_data):
    """Create settings management tab"""
    can_write = check_permission(user_data, 'settings', 'write')
    
    # Get current settings
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT tolerance, company_name FROM settings WHERE id = ?', ('current',))
    settings = cursor.fetchone()
    conn.close()
    
    tolerance = settings['tolerance'] if settings else 10
    company_name = settings['company_name'] if settings else 'J-INVESTMENTS'
    
    return html.Div([
        # System configuration
        dbc.Card([
            dbc.CardHeader(
                html.H4("⚙️ System Configuration", style={'color': COLORS['cat_yellow'], 'margin': '0'})
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Anomaly Detection Threshold (%)", 
                                 style={'fontWeight': 'bold', 'color': COLORS['text_bright']}),
                        dbc.Input(
                            id='setting-tolerance',
                            type='number',
                            value=tolerance,
                            min=0,
                            max=50,
                            step=1,
                            style=INPUT_STYLE
                        ),
                        html.Small("Alert when fuel usage exceeds expected consumption by this percentage",
                                 style={'color': COLORS['text_dim'], 'fontStyle': 'italic'})
                    ], md=6),
                    dbc.Col([
                        dbc.Label("Company Name", 
                                 style={'fontWeight': 'bold', 'color': COLORS['text_bright']}),
                        dbc.Input(
                            id='setting-company',
                            value=company_name,
                            style=INPUT_STYLE,
                            disabled=True
                        )
                    ], md=6)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("SAVE SETTINGS", id='btn-save-settings', n_clicks=0,
                                  disabled=not can_write, style=BUTTON_PRIMARY, className='mt-3')
                    ])
                ])
            ])
        ], style=CARD_STYLE),
        
        # Data management
        dbc.Card([
            dbc.CardHeader(
                html.H4("📦 Data Management", style={'color': COLORS['cat_yellow'], 'margin': '0'})
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H5("Export Data", style={'color': COLORS['text_bright']}),
                        dbc.Button("📤 Export Analytics", id='btn-export-analytics', n_clicks=0, size='sm',
                                  color='success', className='me-2 mb-2'),
                        dbc.Button("📦 Create Backup (JSON)", id='btn-backup', n_clicks=0,
                                  color='info', className='mb-2')
                    ], md=6),
                    dbc.Col([
                        html.H5("Import Data", style={'color': COLORS['text_bright']}),
                        dcc.Upload(
                            id='upload-excel',
                            children=dbc.Button("📥 Import Excel", color='secondary'),
                            multiple=False
                        )
                    ], md=6)
                ])
            ])
        ], style=CARD_STYLE),
        
        # System info
        html.Div(id='system-info'),
        
        # Download components
        dcc.Download(id='download-excel'),
        dcc.Download(id='download-backup'),
        
        # Notifications
        html.Div(id='settings-notification')
    ])

# ==================== USERS TAB ====================
def create_users_tab(user_data):
    """Create user management tab (admin only)"""
    if not check_permission(user_data, 'users', 'write'):
        return dbc.Alert("You don't have permission to manage users.", color="danger", style={'margin': '20px'})
    
    return html.Div([
        # Add user form
        dbc.Card([
            dbc.CardHeader(
                html.H4("👤 Create New User", style={'color': COLORS['cat_yellow'], 'margin': '0'})
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Username", style={'fontWeight': 'bold', 'color': COLORS['text_bright']}),
                        dbc.Input(id='user-username', placeholder="username", style=INPUT_STYLE)
                    ], md=3),
                    dbc.Col([
                        dbc.Label("Full Name", style={'fontWeight': 'bold', 'color': COLORS['text_bright']}),
                        dbc.Input(id='user-fullname', placeholder="John Doe", style=INPUT_STYLE)
                    ], md=3),
                    dbc.Col([
                        dbc.Label("Email", style={'fontWeight': 'bold', 'color': COLORS['text_bright']}),
                        dbc.Input(id='user-email', type='email', placeholder="user@email.com", style=INPUT_STYLE)
                    ], md=3),
                    dbc.Col([
                        dbc.Label("Password", style={'fontWeight': 'bold', 'color': COLORS['text_bright']}),
                        dbc.Input(id='user-password', type='password', placeholder="Password", style=INPUT_STYLE)
                    ], md=3)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Role", style={'fontWeight': 'bold', 'color': COLORS['text_bright']}),
                        dcc.Dropdown(
                            id='user-role',
                            options=[
                                {'label': '🔑 Admin - Full Access', 'value': 'admin'},
                                {'label': '👔 Manager - Read/Write/Delete (Limited)', 'value': 'manager'},
                                {'label': '✍️ Data Entry - Add Only (No Delete)', 'value': 'data_entry'},
                                {'label': '👁️ Viewer - Read Only', 'value': 'viewer'}
                            ],
                            placeholder="Select Role",
                            style={'color': '#000'}
                        )
                    ], md=10),
                    dbc.Col([
                        dbc.Label(" ", style={'visibility': 'hidden'}),
                        dbc.Button("CREATE USER", id='btn-create-user', n_clicks=0,
                                  style={**BUTTON_PRIMARY, 'width': '100%'})
                    ], md=2)
                ], style={'marginTop': '15px'})
            ])
        ], style=CARD_STYLE),
        
        # Users table
        html.Div(id='users-table-container'),
        
        # Audit log
        dbc.Card([
            dbc.CardHeader(
                html.H4("📋 Audit Log (Recent Activity)", style={'color': COLORS['cat_yellow'], 'margin': '0'})
            ),
            dbc.CardBody([
                html.Div(id='audit-log-container')
            ])
        ], style=CARD_STYLE),
        
        # Notifications
        html.Div(id='user-notification')
    ])

# ==================== DELETE CONFIRMATION MODAL ====================
delete_modal = dbc.Modal([
    dbc.ModalHeader("⚠️ Confirm Deletion"),
    dbc.ModalBody([
        html.P(id="delete-modal-text", style={'color': COLORS['text_bright'], 'fontSize': '1.1rem'}),
        html.Hr(),
        html.P("For security, enter an admin password to confirm:", 
               style={'color': COLORS['cat_yellow'], 'fontWeight': 'bold', 'marginTop': '20px'}),
        dbc.Input(
            id="admin-password-input",
            type="password",
            placeholder="Admin password required",
            style={**INPUT_STYLE, 'fontSize': '1rem'}
        ),
        html.Div(id="delete-error", style={'marginTop': '10px'})
    ]),
    dbc.ModalFooter([
        dbc.Button("Cancel", id="cancel-delete-btn", color="secondary", n_clicks=0),
        dbc.Button("Delete", id="confirm-delete-btn", n_clicks=0, style=BUTTON_DANGER)
    ])
], id="delete-modal", is_open=False, backdrop="static")

# ==================== MAIN APP LAYOUT ====================
def create_main_app(user_data):
    """Create main application layout"""
    return html.Div([
        create_header(user_data),
        
        dbc.Container([
            html.Div(id="tab-content")
        ], fluid=True, style={
            'background': COLORS['bg_dark'],
            'minHeight': '100vh',
            'paddingBottom': '50px'
        }),
        
        # Modals
        delete_modal,
        
        # Hidden stores
        dcc.Store(id='user-store'),
        dcc.Store(id='delete-confirmation-store'),
        dcc.Interval(id='refresh-interval', interval=30000, n_intervals=0)
    ], style={'background': COLORS['bg_dark']})

# ==================== ROOT LAYOUT ====================
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# ==================== CALLBACKS ====================

# Page routing
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    """Route pages based on authentication"""
    init_db()
    user_data = get_user_data()
    
    if user_data:
        return create_main_app(user_data)
    else:
        return create_login_page()

# Login
@app.callback(
    [Output('url', 'pathname', allow_duplicate=True),
     Output('login-error', 'children')],
    Input('btn-login', 'n_clicks'),
    [State('login-username', 'value'),
     State('login-password', 'value')],
    prevent_initial_call=True
)
def login(n_clicks, username, password):
    """Handle login"""
    if not n_clicks or not username or not password:
        raise PreventUpdate
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, username, full_name, email, role, permissions, active 
        FROM users 
        WHERE username = ? AND password_hash = ?
    ''', (username, hash_password(password)))
    user = cursor.fetchone()
    
    if user and user['active']:
        session['user_id'] = user['id']
        session['username'] = user['username']
        session.permanent = True
        
        cursor.execute('UPDATE users SET last_login = ? WHERE id = ?', 
                      (datetime.now(), user['id']))
        log_audit(cursor, user['id'], user['username'], 'login')
        conn.commit()
        conn.close()
        
        return '/', ""
    
    conn.close()
    return dash.no_update, create_notification(
        "❌ Invalid username or password", "danger")

# Logout
@app.callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input('btn-logout', 'n_clicks'),
    prevent_initial_call=True
)
def logout(n_clicks):
    """Handle logout"""
    if n_clicks:
        user_data = get_user_data()
        if user_data:
            conn = get_db()
            cursor = conn.cursor()
            log_audit(cursor, user_data['id'], user_data['username'], 'logout')
            conn.commit()
            conn.close()
        
        session.clear()
        return '/'
    raise PreventUpdate

# Tab content rendering
@app.callback(
    Output('tab-content', 'children'),
    [Input('main-tabs', 'active_tab'),
     Input('refresh-interval', 'n_intervals')]
)
def render_tab_content(active_tab, n):
    """Render content based on active tab"""
    user_data = get_user_data()
    if not user_data:
        raise PreventUpdate
    
    if active_tab == "refueling":
        return create_refueling_tab(user_data)
    elif active_tab == "fleet":
        return create_fleet_tab(user_data)
    elif active_tab == "operators":
        return create_operators_tab(user_data)
    elif active_tab == "analytics":
        return create_analytics_tab(user_data)
    elif active_tab == "settings":
        return create_settings_tab(user_data)
    elif active_tab == "users":
        return create_users_tab(user_data)
    
    return html.Div()

# ==================== REFUELING CALLBACKS ====================

# Add refuel entry
@app.callback(
    [Output('refueling-table-container', 'children', allow_duplicate=True),
     Output('refuel-notification', 'children'),
     Output('refuel-machine', 'value'),
     Output('refuel-operator', 'value'),
     Output('refuel-usage', 'value'),
     Output('refuel-fuel', 'value'),
     Output('refuel-notes', 'value')],
    Input('btn-add-refuel', 'n_clicks'),
    [State('refuel-machine', 'value'),
     State('refuel-operator', 'value'),
     State('refuel-usage', 'value'),
     State('refuel-fuel', 'value'),
     State('refuel-notes', 'value')],
    prevent_initial_call=True
)
def add_refuel(n_clicks, machine_id, operator_id, usage, fuel, notes):
    """Add new refuel entry"""
    if not n_clicks:
        raise PreventUpdate
    
    user_data = get_user_data()
    if not user_data or not check_permission(user_data, 'refuels', 'write'):
        return dash.no_update, create_notification("❌ Permission denied", "danger"), *[dash.no_update]*5
    
    if not all([machine_id, operator_id, usage, fuel]):
        return dash.no_update, create_notification("❌ Please fill all required fields", "warning"), *[dash.no_update]*5
    
    if float(usage) <= 0 or float(fuel) <= 0:
        return dash.no_update, create_notification("❌ Usage and fuel must be greater than 0", "warning"), *[dash.no_update]*5
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        refuel_id = generate_uuid()
        timestamp = int(datetime.now().timestamp() * 1000)
        
        cursor.execute('''
            INSERT INTO refuels (id, timestamp, machine_id, operator_id, usage, fuel, notes, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (refuel_id, timestamp, machine_id, operator_id, float(usage), float(fuel), 
              notes or '', user_data['id']))
        
        log_audit(cursor, user_data['id'], user_data['username'], 'create', 'refuels', refuel_id,
                 f"Added refuel: {machine_id}, {usage}hrs, {fuel}L")
        
        conn.commit()
        conn.close()
        
        return (render_refueling_table('all'), 
                create_notification("✅ Refuel entry logged successfully!"), 
                None, None, None, None, '')
    except Exception as e:
        return dash.no_update, create_notification(f"❌ Error: {str(e)}", "danger"), *[dash.no_update]*5

# Render refueling table
@app.callback(
    Output('refueling-table-container', 'children'),
    [Input('btn-refuel-today', 'n_clicks'),
     Input('btn-refuel-week', 'n_clicks'),
     Input('btn-refuel-all', 'n_clicks')],
    prevent_initial_call=False
)
def update_refueling_table(btn_today, btn_week, btn_all):
    """Update refueling table based on filter"""
    triggered_id = ctx.triggered_id if ctx.triggered_id else 'btn-refuel-today'
    
    if triggered_id == 'btn-refuel-today':
        filter_type = 'today'
    elif triggered_id == 'btn-refuel-week':
        filter_type = 'week'
    else:
        filter_type = 'all'
    
    return render_refueling_table(filter_type)

def render_refueling_table(filter_type='today'):
    """Render refueling data table"""
    user_data = get_user_data()
    if not user_data:
        return html.Div()
    
    can_delete = check_permission(user_data, 'refuels', 'delete')
    
    conn = get_db()
    query = '''
        SELECT r.id, r.timestamp, r.machine_id, m.model as machine_model, m.rate,
               o.name as operator_name, r.usage, r.fuel, r.notes
        FROM refuels r
        JOIN machines m ON r.machine_id = m.id
        JOIN operators o ON r.operator_id = o.id
        ORDER BY r.timestamp DESC
    '''
    
    df = pd.read_sql_query(query, conn)
    
    # Get settings for threshold
    cursor = conn.cursor()
    cursor.execute('SELECT tolerance FROM settings WHERE id = ?', ('current',))
    settings = cursor.fetchone()
    tolerance = settings['tolerance'] if settings else 10
    conn.close()
    
    if df.empty:
        return dbc.Card([
            dbc.CardBody([
                html.P("No refuel entries found. Add your first entry above!", 
                      style={'color': COLORS['text_dim'], 'textAlign': 'center', 'padding': '40px'})
            ])
        ], style=CARD_STYLE)
    
    # Calculate expected fuel and variance
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['expected_fuel'] = df['usage'] * df['rate']
    df['variance'] = df['fuel'] - df['expected_fuel']
    df['variance_pct'] = (df['variance'] / df['expected_fuel'] * 100).round(2)
    
    # Apply filter
    if filter_type == 'today':
        today = datetime.now().date()
        df = df[df['datetime'].dt.date == today]
    elif filter_type == 'week':
        week_ago = datetime.now() - timedelta(days=7)
        df = df[df['datetime'] >= week_ago]
    
    if df.empty:
        return dbc.Card([
            dbc.CardBody([
                html.P(f"No entries found for '{filter_type}' filter.", 
                      style={'color': COLORS['text_dim'], 'textAlign': 'center', 'padding': '40px'})
            ])
        ], style=CARD_STYLE)
    
    # Prepare display data
    display_df = df.copy()
    display_df['datetime_str'] = display_df['datetime'].dt.strftime('%Y-%m-%d %H:%M')
    
    # Create status column
    def get_status(row):
        if abs(row['variance_pct']) > tolerance:
            return f"⚠️ ANOMALY ({row['variance_pct']:+.1f}%)"
        return f"✅ NORMAL ({row['variance_pct']:+.1f}%)"
    
    display_df['status'] = display_df.apply(get_status, axis=1)
    
    # Create table columns
    columns = [
        {'name': 'Date/Time', 'id': 'datetime_str'},
        {'name': 'Machine', 'id': 'machine_id'},
        {'name': 'Model', 'id': 'machine_model'},
        {'name': 'Operator', 'id': 'operator_name'},
        {'name': 'Usage', 'id': 'usage', 'type': 'numeric', 'format': {'specifier': '.1f'}},
        {'name': 'Fuel (L)', 'id': 'fuel', 'type': 'numeric', 'format': {'specifier': '.1f'}},
        {'name': 'Expected (L)', 'id': 'expected_fuel', 'type': 'numeric', 'format': {'specifier': '.1f'}},
        {'name': 'Variance (L)', 'id': 'variance', 'type': 'numeric', 'format': {'specifier': '+.1f'}},
        {'name': 'Status', 'id': 'status'},
    ]
    
    if can_delete:
        columns.append({'name': 'Actions', 'id': 'actions', 'presentation': 'markdown'})
        display_df['actions'] = display_df['id'].apply(
            lambda x: f'<button id="{{"type": "delete-refuel", "index": "{x}"}}" style="background: {COLORS["danger"]}; color: white; border: none; padding: 4px 12px; border-radius: 3px; cursor: pointer;">Delete</button>'
        )
    
    # Create custom style_data_conditional for refueling table
    refuel_style_conditional = [
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#1a1a1a'
        },
        {
            'if': {
                'filter_query': '{variance_pct} > ' + str(tolerance) + ' || {variance_pct} < -' + str(tolerance),
                'column_id': 'status'
            },
            'backgroundColor': 'rgba(255, 77, 77, 0.2)',
            'color': COLORS['danger'],
            'fontWeight': 'bold'
        }
    ]
    
    table = dash_table.DataTable(
        data=display_df.to_dict('records'),
        columns=columns,
        style_table=TABLE_STYLE['style_table'],
        style_header=TABLE_STYLE['style_header'],
        style_cell=TABLE_STYLE['style_cell'],
        style_data_conditional=refuel_style_conditional,
        page_size=20,
        sort_action='native'
    )
    
    # Summary stats with improved styling
    summary = html.Div([
        html.Hr(style={'borderColor': '#333', 'margin': '20px 0'}),
        html.H5("📊 Summary Statistics", style={'color': COLORS['cat_yellow'], 'marginBottom': '15px'}),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Strong("Total Entries", style={'color': COLORS['text_dim'], 'fontSize': '0.85rem', 'display': 'block'}),
                    html.Span(str(len(df)), style={'color': COLORS['cat_yellow'], 'fontSize': '1.8rem', 'fontWeight': 'bold'})
                ], style={'textAlign': 'center', 'padding': '20px', 'background': '#0a0a0a', 'borderRadius': '4px', 'border': f"1px solid {COLORS['cat_yellow']}"})
            ], md=2),
            dbc.Col([
                html.Div([
                    html.Strong("Total Fuel Used", style={'color': COLORS['text_dim'], 'fontSize': '0.85rem', 'display': 'block'}),
                    html.Span(f"{df['fuel'].sum():.1f} L", style={'color': COLORS['cat_yellow'], 'fontSize': '1.8rem', 'fontWeight': 'bold'})
                ], style={'textAlign': 'center', 'padding': '20px', 'background': '#0a0a0a', 'borderRadius': '4px', 'border': f"1px solid {COLORS['cat_yellow']}"})
            ], md=2),
            dbc.Col([
                html.Div([
                    html.Strong("Total Machine Hours", style={'color': COLORS['text_dim'], 'fontSize': '0.85rem', 'display': 'block'}),
                    html.Span(f"{df['usage'].sum():.1f} hrs", style={'color': COLORS['cat_yellow'], 'fontSize': '1.8rem', 'fontWeight': 'bold'})
                ], style={'textAlign': 'center', 'padding': '20px', 'background': '#0a0a0a', 'borderRadius': '4px', 'border': f"1px solid {COLORS['cat_yellow']}"})
            ], md=3),
            dbc.Col([
                html.Div([
                    html.Strong("Expected Fuel", style={'color': COLORS['text_dim'], 'fontSize': '0.85rem', 'display': 'block'}),
                    html.Span(f"{df['expected_fuel'].sum():.1f} L", style={'color': COLORS['info'], 'fontSize': '1.8rem', 'fontWeight': 'bold'})
                ], style={'textAlign': 'center', 'padding': '20px', 'background': '#0a0a0a', 'borderRadius': '4px', 'border': f"1px solid {COLORS['info']}"})
            ], md=3),
            dbc.Col([
                html.Div([
                    html.Strong("Anomalies Detected", style={'color': COLORS['text_dim'], 'fontSize': '0.85rem', 'display': 'block'}),
                    html.Span(str((df['variance_pct'].abs() > tolerance).sum()), 
                             style={'color': COLORS['danger'], 'fontSize': '1.8rem', 'fontWeight': 'bold'})
                ], style={'textAlign': 'center', 'padding': '20px', 'background': '#0a0a0a', 'borderRadius': '4px', 'border': f"1px solid {COLORS['danger']}"})
            ], md=2)
        ], style={'padding': '0px'}, className="g-2")
    ], style={'marginTop': '20px'})
    
    return dbc.Card([
        dbc.CardBody([table, summary])
    ], style=CARD_STYLE)

# ==================== FLEET CALLBACKS ====================

# Add machine
@app.callback(
    [Output('machines-table-container', 'children', allow_duplicate=True),
     Output('machine-notification', 'children'),
     Output('machine-id', 'value'),
     Output('machine-model', 'value'),
     Output('machine-rate', 'value'),
     Output('machine-capacity', 'value')],
    Input('btn-add-machine', 'n_clicks'),
    [State('machine-id', 'value'),
     State('machine-model', 'value'),
     State('machine-rate', 'value'),
     State('machine-capacity', 'value')],
    prevent_initial_call=True
)
def add_machine(n_clicks, machine_id, model, rate, capacity):
    """Add new machine"""
    if not n_clicks:
        raise PreventUpdate
    
    user_data = get_user_data()
    if not user_data or not check_permission(user_data, 'machines', 'write'):
        return dash.no_update, create_notification("❌ Permission denied", "danger"), *[dash.no_update]*4
    
    if not all([machine_id, model, rate, capacity]):
        return dash.no_update, create_notification("❌ Please fill all fields", "warning"), *[dash.no_update]*4
    
    if float(rate) <= 0 or int(capacity) <= 0:
        return dash.no_update, create_notification("❌ Rate and capacity must be greater than 0", "warning"), *[dash.no_update]*4
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        machine_id = machine_id.upper().strip()
        
        cursor.execute('''
            INSERT INTO machines (id, model, rate, capacity, created_by)
            VALUES (?, ?, ?, ?, ?)
        ''', (machine_id, model, float(rate), int(capacity), user_data['id']))
        
        log_audit(cursor, user_data['id'], user_data['username'], 'create', 'machines', machine_id,
                 f"Added machine: {model}")
        
        conn.commit()
        conn.close()
        
        return (render_machines_table(), 
                create_notification(f"✅ Machine {machine_id} added successfully!"), 
                '', '', None, None)
    except sqlite3.IntegrityError:
        return dash.no_update, create_notification(f"❌ Machine ID {machine_id} already exists", "danger"), *[dash.no_update]*4
    except Exception as e:
        return dash.no_update, create_notification(f"❌ Error: {str(e)}", "danger"), *[dash.no_update]*4

# Render machines table
@app.callback(
    Output('machines-table-container', 'children'),
    Input('btn-add-machine', 'n_clicks'),
    prevent_initial_call=False
)
def update_machines_table(n):
    """Update machines table"""
    return render_machines_table()

def render_machines_table():
    """Render machines data table"""
    user_data = get_user_data()
    if not user_data:
        return html.Div()
    
    can_delete = check_permission(user_data, 'machines', 'delete')
    
    conn = get_db()
    df = pd.read_sql_query(
        'SELECT id, model, rate, capacity, status FROM machines WHERE status="active" ORDER BY id', 
        conn
    )
    conn.close()
    
    if df.empty:
        return dbc.Card([
            dbc.CardBody([
                html.P("No machines found. Add your first machine above!", 
                      style={'color': COLORS['text_dim'], 'textAlign': 'center', 'padding': '40px'})
            ])
        ], style=CARD_STYLE)
    
    columns = [
        {'name': 'Machine ID', 'id': 'id'},
        {'name': 'Model', 'id': 'model'},
        {'name': 'Rate (L/hr)', 'id': 'rate', 'type': 'numeric', 'format': {'specifier': '.1f'}},
        {'name': 'Capacity (L)', 'id': 'capacity', 'type': 'numeric', 'format': {'specifier': 'd'}},
    ]
    
    display_df = df.copy()
    
    if can_delete:
        columns.append({'name': 'Actions', 'id': 'actions'})
        display_df['actions'] = ''  # Will be handled by pattern-matching callbacks
    
    table = dash_table.DataTable(
        data=display_df.to_dict('records'),
        columns=columns,
        **TABLE_STYLE,
        page_size=20,
        id='machines-table'
    )
    
    # Add delete buttons if user has permission
    if can_delete:
        delete_buttons = html.Div([
            dbc.Button(
                "🗑️ Delete",
                id={'type': 'delete-machine', 'index': row['id']},
                size='sm',
                style=BUTTON_DANGER,
                className='me-2'
            ) for _, row in df.iterrows()
        ])
    else:
        delete_buttons = html.Div()
    
    return dbc.Card([
        dbc.CardBody([
            table,
            html.Hr(),
            html.Div([
                html.Strong("Total Machines: ", style={'color': COLORS['text_dim']}),
                html.Span(str(len(df)), style={'color': COLORS['cat_yellow'], 'fontSize': '1.2rem', 'fontWeight': 'bold'})
            ], style={'padding': '15px', 'background': '#0a0a0a', 'borderRadius': '4px'})
        ])
    ], style=CARD_STYLE)

# ==================== OPERATORS CALLBACKS ====================

# Add operator
@app.callback(
    [Output('operators-table-container', 'children', allow_duplicate=True),
     Output('operator-notification', 'children'),
     Output('operator-name', 'value'),
     Output('operator-badge', 'value')],
    Input('btn-add-operator', 'n_clicks'),
    [State('operator-name', 'value'),
     State('operator-badge', 'value')],
    prevent_initial_call=True
)
def add_operator(n_clicks, name, badge):
    """Add new operator"""
    if not n_clicks:
        raise PreventUpdate
    
    user_data = get_user_data()
    if not user_data or not check_permission(user_data, 'operators', 'write'):
        return dash.no_update, create_notification("❌ Permission denied", "danger"), dash.no_update, dash.no_update
    
    if not all([name, badge]):
        return dash.no_update, create_notification("❌ Please fill all fields", "warning"), dash.no_update, dash.no_update
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        operator_id = generate_uuid()
        
        cursor.execute('''
            INSERT INTO operators (id, name, badge, created_by)
            VALUES (?, ?, ?, ?)
        ''', (operator_id, name, badge, user_data['id']))
        
        log_audit(cursor, user_data['id'], user_data['username'], 'create', 'operators', operator_id,
                 f"Added operator: {name}")
        
        conn.commit()
        conn.close()
        
        return render_operators_table(), create_notification(f"✅ Operator {name} added successfully!"), '', ''
    except sqlite3.IntegrityError:
        return dash.no_update, create_notification(f"❌ Badge number {badge} already exists", "danger"), dash.no_update, dash.no_update
    except Exception as e:
        return dash.no_update, create_notification(f"❌ Error: {str(e)}", "danger"), dash.no_update, dash.no_update

# Render operators table
@app.callback(
    Output('operators-table-container', 'children'),
    Input('btn-add-operator', 'n_clicks'),
    prevent_initial_call=False
)
def update_operators_table(n):
    """Update operators table"""
    return render_operators_table()

def render_operators_table():
    """Render operators data table"""
    user_data = get_user_data()
    if not user_data:
        return html.Div()
    
    can_delete = check_permission(user_data, 'operators', 'delete')
    
    conn = get_db()
    df = pd.read_sql_query(
        'SELECT id, name, badge, status FROM operators WHERE status="active" ORDER BY name', 
        conn
    )
    conn.close()
    
    if df.empty:
        return dbc.Card([
            dbc.CardBody([
                html.P("No operators found. Add your first operator above!", 
                      style={'color': COLORS['text_dim'], 'textAlign': 'center', 'padding': '40px'})
            ])
        ], style=CARD_STYLE)
    
    columns = [
        {'name': 'Name', 'id': 'name'},
        {'name': 'Badge Number', 'id': 'badge'},
    ]
    
    table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=columns,
        **TABLE_STYLE,
        page_size=20
    )
    
    return dbc.Card([
        dbc.CardBody([
            table,
            html.Hr(),
            html.Div([
                html.Strong("Total Operators: ", style={'color': COLORS['text_dim']}),
                html.Span(str(len(df)), style={'color': COLORS['cat_yellow'], 'fontSize': '1.2rem', 'fontWeight': 'bold'})
            ], style={'padding': '15px', 'background': '#0a0a0a', 'borderRadius': '4px'})
        ])
    ], style=CARD_STYLE)

# ==================== ANALYTICS CALLBACKS ====================

# Update analytics
@app.callback(
    [Output('kpi-cards', 'children'),
     Output('fuel-trend-chart', 'figure'),
     Output('machine-performance-chart', 'figure'),
     Output('operator-performance-table', 'children')],
    Input('btn-apply-dates', 'n_clicks'),
    [State('date-from', 'date'),
     State('date-to', 'date')],
    prevent_initial_call=False
)
def update_analytics(n_clicks, date_from, date_to):
    """Update analytics dashboard"""
    user_data = get_user_data()
    if not user_data:
        raise PreventUpdate
    
    # Default dates if not provided
    if not date_from:
        date_from = (datetime.now() - timedelta(days=30)).date()
    if not date_to:
        date_to = datetime.now().date()
    
    # Get data
    conn = get_db()
    query = '''
        SELECT r.*, m.model, m.rate, o.name as operator_name
        FROM refuels r
        JOIN machines m ON r.machine_id = m.id
        JOIN operators o ON r.operator_id = o.id
        ORDER BY r.timestamp DESC
    '''
    df = pd.read_sql_query(query, conn)
    
    # Get settings
    cursor = conn.cursor()
    cursor.execute('SELECT tolerance FROM settings WHERE id = ?', ('current',))
    settings = cursor.fetchone()
    tolerance = settings['tolerance'] if settings else 10
    conn.close()
    
    if df.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            paper_bgcolor=COLORS['carbon'],
            plot_bgcolor=COLORS['carbon'],
            font_color=COLORS['text_dim'],
            annotations=[{'text': 'No data available', 'showarrow': False, 'font': {'size': 20}}]
        )
        return (
            html.P("No data available. Import data or add refueling entries to see analytics.", 
                  style={'color': COLORS['text_dim'], 'padding': '20px', 'textAlign': 'center'}),
            empty_fig, empty_fig,
            html.P("No data available", style={'color': COLORS['text_dim']})
        )
    
    # Process data
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['expected_fuel'] = df['usage'] * df['rate']
    df['variance'] = df['fuel'] - df['expected_fuel']
    df['variance_pct'] = (df['variance'] / df['expected_fuel'] * 100).round(2)
    df['efficiency'] = (df['expected_fuel'] / df['fuel'] * 100).round(2)
    
    # Filter by date
    filtered_df = df[(df['datetime'].dt.date >= pd.to_datetime(date_from).date()) & 
                     (df['datetime'].dt.date <= pd.to_datetime(date_to).date())]
    
    if filtered_df.empty:
        filtered_df = df  # Fallback to all data
    
    # Calculate KPI values
    total_fuel = filtered_df['fuel'].sum()
    expected_fuel = filtered_df['expected_fuel'].sum()
    total_usage = filtered_df['usage'].sum()
    anomalies = (filtered_df['variance_pct'].abs() > tolerance).sum()
    avg_efficiency = filtered_df['efficiency'].mean()
    
    # KPI Cards with improved styling
    kpi_cards = dbc.Row([
        dbc.Col([
            html.Div([
                html.H6("Used Fuel", style={'color': COLORS['text_dim'], 'marginBottom': '5px'}),
                html.H3(f"{total_fuel:.1f} L", style={'color': COLORS['cat_yellow'], 'fontWeight': 'bold', 'margin': '0'})
            ], style={
                'textAlign': 'center', 
                'padding': '25px 20px',
                'background': 'linear-gradient(135deg, rgba(255, 180, 0, 0.1) 0%, rgba(255, 180, 0, 0.05) 100%)',
                'height': '110px',
                'borderRadius': '8px',
                'border': f"2px solid {COLORS['cat_yellow']}",
                'boxShadow': f"0 4px 15px rgba(255, 180, 0, 0.2)"
            })
        ], md=3),
        dbc.Col([
            html.Div([
                html.H6("Expected Fuel", style={'color': COLORS['text_dim'], 'marginBottom': '5px'}),
                html.H3(f"{expected_fuel:.1f} L", style={'color': COLORS['info'], 'fontWeight': 'bold', 'margin': '0'})
            ], style={
                'textAlign': 'center', 
                'padding': '25px 20px',
                'background': 'linear-gradient(135deg, rgba(52, 152, 219, 0.1) 0%, rgba(52, 152, 219, 0.05) 100%)',
                'height': '110px',
                'borderRadius': '8px',
                'border': f"2px solid {COLORS['info']}",
                'boxShadow': f"0 4px 15px rgba(52, 152, 219, 0.2)"
            })
        ], md=3),
        dbc.Col([
            html.Div([
                html.H6("Total Machine Hours", style={'color': COLORS['text_dim'], 'marginBottom': '5px'}),
                html.H3(f"{total_usage:.1f} hrs", style={'color': COLORS['success'], 'fontWeight': 'bold', 'margin': '0'})
            ], style={
                'textAlign': 'center', 
                'padding': '25px 20px',
                'background': 'linear-gradient(135deg, rgba(46, 204, 113, 0.1) 0%, rgba(46, 204, 113, 0.05) 100%)',
                'height': '110px',
                'borderRadius': '8px',
                'border': f"2px solid {COLORS['success']}",
                'boxShadow': f"0 4px 15px rgba(46, 204, 113, 0.2)"
            })
        ], md=3),
        dbc.Col([
            html.Div([
                html.H6("Anomalies", style={'color': COLORS['text_dim'], 'marginBottom': '5px'}),
                html.H3(str(anomalies), style={'color': COLORS['danger'], 'fontWeight': 'bold', 'margin': '0'})
            ], style={
                'textAlign': 'center', 
                'padding': '25px 20px',
                'background': 'linear-gradient(135deg, rgba(255, 77, 77, 0.1) 0%, rgba(255, 77, 77, 0.05) 100%)',
                'height': '110px',
                'borderRadius': '8px',
                'border': f"2px solid {COLORS['danger']}",
                'boxShadow': f"0 4px 15px rgba(255, 77, 77, 0.2)"
            })
        ], md=3)
    ], className="g-3", style={'marginBottom': '20px'})
    
    # Expected vs Delivered Fuel Chart (Improved styling)
    daily_data = filtered_df.groupby(filtered_df['datetime'].dt.date).agg({
        'fuel': 'sum',
        'expected_fuel': 'sum'
    }).reset_index()
    
    fuel_trend_fig = go.Figure()
    
    # Add Expected Fuel as area
    fuel_trend_fig.add_trace(go.Scatter(
        x=daily_data['datetime'], 
        y=daily_data['expected_fuel'],
        mode='lines',
        name='Expected Fuel',
        line=dict(color=COLORS['info'], width=2, dash='dash'),
        fill='tozeroy',
        fillcolor='rgba(52, 152, 219, 0.1)'
    ))
    
    # Add Actual Fuel as solid line
    fuel_trend_fig.add_trace(go.Scatter(
        x=daily_data['datetime'], 
        y=daily_data['fuel'],
        mode='lines+markers', 
        name='Actual Fuel',
        line=dict(color=COLORS['cat_yellow'], width=3),
        marker=dict(size=8, symbol='circle', line=dict(width=2, color='#000'))
    ))
    
    fuel_trend_fig.update_layout(
        paper_bgcolor=COLORS['carbon'],
        plot_bgcolor=COLORS['steel'],
        font=dict(color=COLORS['text_bright'], family='Arial'),
        legend=dict(
            orientation='h',
            y=1.15,
            x=0.5,
            xanchor='center',
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor=COLORS['cat_yellow'],
            borderwidth=1
        ),
        margin=dict(l=40, r=20, t=40, b=40),
        hovermode='x unified',
        xaxis=dict(
            gridcolor='#333',
            showgrid=True,
            title='Date',
            title_font=dict(color=COLORS['text_dim'])
        ),
        yaxis=dict(
            gridcolor='#333',
            showgrid=True,
            title='Fuel (Liters)',
            title_font=dict(color=COLORS['text_dim'])
        )
    )
    
    # Machine Performance Chart (Improved with gradient colors)
    machine_data = filtered_df.groupby('machine_id').agg({
        'fuel': 'sum',
        'usage': 'sum',
        'model': 'first',
        'expected_fuel': 'sum'
    }).reset_index()
    machine_data['efficiency'] = (machine_data['expected_fuel'] / machine_data['fuel'] * 100).round(1)
    
    # Create color scale based on efficiency
    colors_list = []
    for eff in machine_data['efficiency']:
        if eff >= 95:
            colors_list.append(COLORS['success'])
        elif eff >= 85:
            colors_list.append(COLORS['cat_yellow'])
        else:
            colors_list.append(COLORS['danger'])
    
    machine_perf_fig = go.Figure()
    
    machine_perf_fig.add_trace(go.Bar(
        x=machine_data['machine_id'],
        y=machine_data['fuel'],
        name='Actual Fuel',
        marker=dict(
            color=colors_list,
            line=dict(color='#000', width=1.5)
        ),
        text=machine_data['efficiency'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside',
        textfont=dict(color=COLORS['text_bright'], size=11),
        hovertemplate='<b>%{x}</b><br>Fuel: %{y:.1f}L<br>Efficiency: %{text}<extra></extra>'
    ))
    
    machine_perf_fig.update_layout(
        paper_bgcolor=COLORS['carbon'],
        plot_bgcolor=COLORS['steel'],
        font=dict(color=COLORS['text_bright'], family='Arial'),
        margin=dict(l=40, r=20, t=40, b=40),
        xaxis=dict(
            gridcolor='#333',
            title='Machine ID',
            title_font=dict(color=COLORS['text_dim'])
        ),
        yaxis=dict(
            gridcolor='#333',
            showgrid=True,
            title='Total Fuel (Liters)',
            title_font=dict(color=COLORS['text_dim'])
        ),
        showlegend=False
    )
    
    # Operator Performance Table with improved styling
    operator_data = filtered_df.groupby('operator_name').agg({
        'fuel': 'sum',
        'usage': 'sum',
        'expected_fuel': 'sum',
        'id': 'count'
    }).reset_index()
    operator_data['efficiency'] = (operator_data['expected_fuel'] / operator_data['fuel'] * 100).round(1)
    operator_data.columns = ['Operator', 'Total Fuel (L)', 'Total Usage (hrs)', 'Expected Fuel (L)', 'Entries', 'Efficiency (%)']
    operator_data = operator_data.sort_values('Total Fuel (L)', ascending=False)
    
    operator_table = dash_table.DataTable(
        data=operator_data.to_dict('records'),
        columns=[
            {'name': col, 'id': col, 'type': 'numeric' if col != 'Operator' else 'text',
             'format': {'specifier': '.1f'} if '(L)' in col or '(hrs)' in col or '(%)' in col else {}}
            for col in operator_data.columns
        ],
        style_table=TABLE_STYLE['style_table'],
        style_header={
            **TABLE_STYLE['style_header'],
            'backgroundColor': '#000',
            'borderBottom': f"2px solid {COLORS['cat_yellow']}"
        },
        style_cell=TABLE_STYLE['style_cell'],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#1a1a1a'
            },
            {
                'if': {
                    'filter_query': '{Efficiency (%)} >= 95',
                    'column_id': 'Efficiency (%)'
                },
                'color': COLORS['success'],
                'fontWeight': 'bold'
            },
            {
                'if': {
                    'filter_query': '{Efficiency (%)} < 85',
                    'column_id': 'Efficiency (%)'
                },
                'color': COLORS['danger'],
                'fontWeight': 'bold'
            }
        ],
        page_size=10,
        sort_action='native'
    )
    
    return kpi_cards, fuel_trend_fig, machine_perf_fig, operator_table

# ==================== SETTINGS CALLBACKS ====================

# Save settings
@app.callback(
    [Output('system-info', 'children'),
     Output('settings-notification', 'children')],
    Input('btn-save-settings', 'n_clicks'),
    State('setting-tolerance', 'value'),
    prevent_initial_call=True
)
def save_settings(n_clicks, tolerance):
    """Save system settings"""
    if not n_clicks:
        raise PreventUpdate
    
    user_data = get_user_data()
    if not user_data or not check_permission(user_data, 'settings', 'write'):
        return dash.no_update, create_notification("❌ Permission denied", "danger")
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE settings SET tolerance = ?, updated_at = ?, updated_by = ? WHERE id = ?',
                      (float(tolerance), datetime.now(), user_data['id'], 'current'))
        
        log_audit(cursor, user_data['id'], user_data['username'], 'update', 'settings', 'current',
                 f"Updated tolerance to {tolerance}%")
        
        conn.commit()
        conn.close()
        
        return render_system_info(), create_notification("✅ Settings saved successfully!")
    except Exception as e:
        return dash.no_update, create_notification(f"❌ Error: {str(e)}", "danger")

# Render system info
@app.callback(
    Output('system-info', 'children', allow_duplicate=True),
    Input('url', 'pathname'),
    prevent_initial_call=True
)
def update_system_info(pathname):
    """Update system info"""
    return render_system_info()

def render_system_info():
    """Render system information"""
    conn = get_db()
    
    machines_count = pd.read_sql_query('SELECT COUNT(*) as count FROM machines WHERE status="active"', conn).iloc[0]['count']
    operators_count = pd.read_sql_query('SELECT COUNT(*) as count FROM operators WHERE status="active"', conn).iloc[0]['count']
    refuels_count = pd.read_sql_query('SELECT COUNT(*) as count FROM refuels', conn).iloc[0]['count']
    users_count = pd.read_sql_query('SELECT COUNT(*) as count FROM users WHERE active=1', conn).iloc[0]['count']
    
    conn.close()
    
    return dbc.Card([
        dbc.CardHeader(
            html.H4("ℹ️ System Information", style={'color': COLORS['cat_yellow'], 'margin': '0'})
        ),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6("Total Machines", style={'color': COLORS['text_dim']}),
                        html.H4(str(machines_count), style={'color': COLORS['cat_yellow']})
                    ], style={'textAlign': 'center', 'padding': '20px', 'background': '#0a0a0a', 'borderRadius': '4px'})
                ], md=3),
                dbc.Col([
                    html.Div([
                        html.H6("Total Operators", style={'color': COLORS['text_dim']}),
                        html.H4(str(operators_count), style={'color': COLORS['cat_yellow']})
                    ], style={'textAlign': 'center', 'padding': '20px', 'background': '#0a0a0a', 'borderRadius': '4px'})
                ], md=3),
                dbc.Col([
                    html.Div([
                        html.H6("Total Refuel Logs", style={'color': COLORS['text_dim']}),
                        html.H4(str(refuels_count), style={'color': COLORS['cat_yellow']})
                    ], style={'textAlign': 'center', 'padding': '20px', 'background': '#0a0a0a', 'borderRadius': '4px'})
                ], md=3),
                dbc.Col([
                    html.Div([
                        html.H6("Active Users", style={'color': COLORS['text_dim']}),
                        html.H4(str(users_count), style={'color': COLORS['cat_yellow']})
                    ], style={'textAlign': 'center', 'padding': '20px', 'background': '#0a0a0a', 'borderRadius': '4px'})
                ], md=3)
            ])
        ])
    ], style=CARD_STYLE)

# Export Excel
@app.callback(
    Output('download-analytics', 'data'),
    Input('btn-export-analytics', 'n_clicks'),
    State('date-from', 'date'),
    State('date-to', 'date'),
    prevent_initial_call=True
)
def export_analytics(n_clicks, date_from, date_to):
    if not n_clicks:
        raise PreventUpdate
    
    conn = get_db()
    df = pd.read_sql_query('''
        SELECT r.timestamp, r.machine_id, m.model, o.name AS operator,
               r.usage, r.fuel, m.rate,
               (r.usage * m.rate) AS expected_fuel,
               (r.fuel - (r.usage * m.rate)) AS variance
        FROM refuels r
        JOIN machines m ON r.machine_id = m.id
        JOIN operators o ON r.operator_id = o.id
    ''', conn)

    conn.close()

    df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date

    if date_from:
        df = df[df['date'] >= pd.to_datetime(date_from).date()]
    if date_to:
        df = df[df['date'] <= pd.to_datetime(date_to).date()]

    summary = df.groupby('machine_id').agg({
        'fuel': 'sum',
        'expected_fuel': 'sum',
        'variance': 'sum'
    }).reset_index()

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Detailed Logs', index=False)
        summary.to_excel(writer, sheet_name='Machine Summary', index=False)

    return dcc.send_bytes(
        output.getvalue(),
        f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    )
    

# Import Excel
@app.callback(
    Output('settings-notification', 'children', allow_duplicate=True),
    Input('upload-excel', 'contents'),
    State('upload-excel', 'filename'),
    prevent_initial_call=True
)
def import_excel(contents, filename):
    """Import data from Excel file"""
    if not contents:
        raise PreventUpdate
    
    user_data = get_user_data()
    if not user_data or not check_permission(user_data, 'machines', 'write'):
        return create_notification("❌ Permission denied", "danger")
    
    try:
        # Decode the file
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # Read Excel file
        excel_data = BytesIO(decoded)
        xls = pd.ExcelFile(excel_data)
        
        conn = get_db()
        cursor = conn.cursor()
        
        imported_counts = {'operators': 0, 'machines': 0, 'refuels': 0}
        errors = []
        
        # Import Operators (sheet: "Operators")
        if 'Operators' in xls.sheet_names:
            operators_df = pd.read_excel(excel_data, sheet_name='Operators')
            
            for idx, row in operators_df.iterrows():
                try:
                    operator_name = str(row.get('Operator', '')).strip()
                    badge = str(row.get('Badge Number', '')).strip()
                    
                    if not operator_name or not badge:
                        continue
                    
                    # Check if operator already exists
                    cursor.execute('SELECT id FROM operators WHERE badge = ?', (badge,))
                    if cursor.fetchone():
                        continue  # Skip if exists
                    
                    operator_id = generate_uuid()
                    cursor.execute('''
                        INSERT INTO operators (id, name, badge, created_by)
                        VALUES (?, ?, ?, ?)
                    ''', (operator_id, operator_name, badge, user_data['id']))
                    
                    imported_counts['operators'] += 1
                except Exception as e:
                    errors.append(f"Operator row {idx+1}: {str(e)}")
        
        # Import Machines (sheet: "Assets")
        if 'Assets' in xls.sheet_names:
            machines_df = pd.read_excel(excel_data, sheet_name='Assets')
            
            for idx, row in machines_df.iterrows():
                try:
                    machine_id = str(row.get('Machine ID', '')).strip().upper()
                    model = str(row.get('Model', '')).strip()
                    rate = float(row.get('Rate', 0))
                    capacity = int(row.get('Capacity', 0))
                    
                    if not machine_id or not model or rate <= 0 or capacity <= 0:
                        continue
                    
                    # Check if machine already exists
                    cursor.execute('SELECT id FROM machines WHERE id = ?', (machine_id,))
                    if cursor.fetchone():
                        continue  # Skip if exists
                    
                    cursor.execute('''
                        INSERT INTO machines (id, model, rate, capacity, created_by)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (machine_id, model, rate, capacity, user_data['id']))
                    
                    imported_counts['machines'] += 1
                except Exception as e:
                    errors.append(f"Machine row {idx+1}: {str(e)}")
        
        # Import Refueling (sheet: "Refueling")
        if 'Refueling' in xls.sheet_names:
            refuels_df = pd.read_excel(excel_data, sheet_name='Refueling')
            
            for idx, row in refuels_df.iterrows():
                try:
                    # Parse time
                    time_val = row.get('Time')
                    if pd.isna(time_val):
                        continue
                    
                    if isinstance(time_val, str):
                        dt = pd.to_datetime(time_val)
                    else:
                        dt = time_val
                    
                    timestamp = int(dt.timestamp() * 1000)
                    
                    # Get machine and operator
                    machine_id = str(row.get('Machine', '')).strip().upper()
                    operator_name = str(row.get('Operator', '')).strip()
                    usage = float(row.get('Hours worked', 0))
                    fuel = float(row.get('Fuel issued', 0))
                    
                    if not machine_id or not operator_name or usage <= 0 or fuel <= 0:
                        continue
                    
                    # Find machine
                    cursor.execute('SELECT id FROM machines WHERE id = ?', (machine_id,))
                    machine = cursor.fetchone()
                    if not machine:
                        errors.append(f"Refuel row {idx+1}: Machine {machine_id} not found")
                        continue
                    
                    # Find operator by name
                    cursor.execute('SELECT id FROM operators WHERE name = ?', (operator_name,))
                    operator = cursor.fetchone()
                    if not operator:
                        errors.append(f"Refuel row {idx+1}: Operator {operator_name} not found")
                        continue
                    
                    refuel_id = generate_uuid()
                    cursor.execute('''
                        INSERT INTO refuels (id, timestamp, machine_id, operator_id, usage, fuel, notes, created_by)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (refuel_id, timestamp, machine_id, operator['id'], usage, fuel, '', user_data['id']))
                    
                    imported_counts['refuels'] += 1
                except Exception as e:
                    errors.append(f"Refuel row {idx+1}: {str(e)}")
        
        # Log audit
        log_audit(cursor, user_data['id'], user_data['username'], 'import_excel', 'system', filename,
                 f"Imported: {imported_counts}")
        
        conn.commit()
        conn.close()
        
        # Create success message
        message = f"✅ Import completed!\n"
        message += f"Operators: {imported_counts['operators']}, "
        message += f"Machines: {imported_counts['machines']}, "
        message += f"Refuels: {imported_counts['refuels']}"
        
        if errors:
            message += f"\n⚠️ {len(errors)} errors (check console for details)"
            print("\n".join(errors[:10]))  # Print first 10 errors
        
        return create_notification(message, "success" if not errors else "warning")
        
    except Exception as e:
        return create_notification(f"❌ Import failed: {str(e)}", "danger")

# Create backup
@app.callback(
    Output('download-backup', 'data'),
    Input('btn-backup', 'n_clicks'),
    prevent_initial_call=True
)
def create_backup(n_clicks):
    """Create JSON backup"""
    if not n_clicks:
        raise PreventUpdate
    
    conn = get_db()
    
    backup = {
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'company': 'J-INVESTMENTS',
        'machines': pd.read_sql_query('SELECT * FROM machines', conn).to_dict('records'),
        'operators': pd.read_sql_query('SELECT * FROM operators', conn).to_dict('records'),
        'refuels': pd.read_sql_query('SELECT * FROM refuels', conn).to_dict('records'),
        'settings': pd.read_sql_query('SELECT * FROM settings', conn).to_dict('records')
    }
    
    conn.close()
    
    backup_json = json.dumps(backup, indent=2)
    return dcc.send_string(backup_json, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

# ==================== USERS CALLBACKS ====================

# Create user
@app.callback(
    [Output('users-table-container', 'children', allow_duplicate=True),
     Output('user-notification', 'children'),
     Output('user-username', 'value'),
     Output('user-fullname', 'value'),
     Output('user-email', 'value'),
     Output('user-password', 'value'),
     Output('user-role', 'value')],
    Input('btn-create-user', 'n_clicks'),
    [State('user-username', 'value'),
     State('user-fullname', 'value'),
     State('user-email', 'value'),
     State('user-password', 'value'),
     State('user-role', 'value')],
    prevent_initial_call=True
)
def create_user(n_clicks, username, fullname, email, password, role):
    """Create new user"""
    if not n_clicks:
        raise PreventUpdate
    
    user_data = get_user_data()
    if not user_data or not check_permission(user_data, 'users', 'write'):
        return dash.no_update, create_notification("❌ Permission denied", "danger"), *[dash.no_update]*5
    
    if not all([username, fullname, password, role]):
        return dash.no_update, create_notification("❌ Please fill all required fields", "warning"), *[dash.no_update]*5
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        user_id = generate_uuid()
        permissions = json.dumps(ROLE_PERMISSIONS.get(role, {}))
        
        cursor.execute('''
            INSERT INTO users (id, username, password_hash, full_name, email, role, permissions, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, username, hash_password(password), fullname, email or '', role, permissions, user_data['id']))
        
        log_audit(cursor, user_data['id'], user_data['username'], 'create', 'users', user_id,
                 f"Created user: {username} ({role})")
        
        conn.commit()
        conn.close()
        
        return (render_users_table(), 
                create_notification(f"✅ User {username} created successfully!"), 
                '', '', '', '', None)
    except sqlite3.IntegrityError:
        return dash.no_update, create_notification(f"❌ Username {username} already exists", "danger"), *[dash.no_update]*5
    except Exception as e:
        return dash.no_update, create_notification(f"❌ Error: {str(e)}", "danger"), *[dash.no_update]*5

# Render users table
@app.callback(
    [Output('users-table-container', 'children'),
     Output('audit-log-container', 'children')],
    Input('btn-create-user', 'n_clicks'),
    prevent_initial_call=False
)
def update_users_tables(n):
    """Update users and audit log tables"""
    return render_users_table(), render_audit_log()

def render_users_table():
    """Render users table"""
    conn = get_db()
    df = pd.read_sql_query('''
        SELECT id, username, full_name, email, role, 
               CASE WHEN active=1 THEN 'Active' ELSE 'Inactive' END as status,
               last_login
        FROM users 
        ORDER BY created_at DESC
    ''', conn)
    conn.close()
    
    if df.empty:
        return html.P("No users found", style={'color': COLORS['text_dim']})
    
    # Format last login
    df['last_login'] = pd.to_datetime(df['last_login']).dt.strftime('%Y-%m-%d %H:%M')
    df['last_login'] = df['last_login'].fillna('Never')
    
    columns = [
        {'name': 'Username', 'id': 'username'},
        {'name': 'Full Name', 'id': 'full_name'},
        {'name': 'Email', 'id': 'email'},
        {'name': 'Role', 'id': 'role'},
        {'name': 'Status', 'id': 'status'},
        {'name': 'Last Login', 'id': 'last_login'}
    ]
    
    # Create custom style_data_conditional for users table
    users_style_conditional = [
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#1a1a1a'
        },
        {
            'if': {'filter_query': '{status} = "Inactive"', 'column_id': 'status'},
            'color': COLORS['danger']
        },
        {
            'if': {'filter_query': '{status} = "Active"', 'column_id': 'status'},
            'color': COLORS['success']
        }
    ]
    
    table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=columns,
        style_table=TABLE_STYLE['style_table'],
        style_header=TABLE_STYLE['style_header'],
        style_cell=TABLE_STYLE['style_cell'],
        style_data_conditional=users_style_conditional,
        page_size=10,
        sort_action='native'
    )
    
    return dbc.Card([
        dbc.CardHeader(
            html.H4("👥 User Accounts", style={'color': COLORS['cat_yellow'], 'margin': '0'})
        ),
        dbc.CardBody([table])
    ], style=CARD_STYLE)

def render_audit_log():
    """Render audit log"""
    conn = get_db()
    df = pd.read_sql_query('''
        SELECT timestamp, username, action, entity_type, details
        FROM audit_log
        ORDER BY timestamp DESC
        LIMIT 50
    ''', conn)
    conn.close()
    
    if df.empty:
        return html.P("No audit entries", style={'color': COLORS['text_dim']})
    
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in df.columns],
        **TABLE_STYLE,
        page_size=20
    )
    
    return table

# ==================== DELETE MODAL CALLBACKS ====================

# Open delete modal (pattern matching for all delete buttons)
@app.callback(
    [Output('delete-modal', 'is_open', allow_duplicate=True),
     Output('delete-modal-text', 'children', allow_duplicate=True),
     Output('delete-confirmation-store', 'data', allow_duplicate=True)],
    [Input({'type': 'delete-machine', 'index': ALL}, 'n_clicks'),
     Input({'type': 'delete-operator', 'index': ALL}, 'n_clicks'),
     Input({'type': 'delete-refuel', 'index': ALL}, 'n_clicks')],
    prevent_initial_call=True
)
def open_delete_modal(machine_clicks, operator_clicks, refuel_clicks):
    """Open delete confirmation modal"""
    triggered = ctx.triggered_id
    if not triggered:
        raise PreventUpdate
    
    entity_type = triggered['type'].replace('delete-', '')
    entity_id = triggered['index']
    
    messages = {
        'machine': f"Are you sure you want to delete machine {entity_id}?",
        'operator': f"Are you sure you want to delete this operator?",
        'refuel': f"Are you sure you want to delete this refuel entry?"
    }
    
    return True, messages.get(entity_type, "Confirm deletion"), {'type': entity_type, 'id': entity_id}

# Confirm delete
@app.callback(
    [Output('delete-modal', 'is_open', allow_duplicate=True),
     Output('delete-error', 'children'),
     Output('admin-password-input', 'value'),
     Output('machines-table-container', 'children', allow_duplicate=True),
     Output('operators-table-container', 'children', allow_duplicate=True),
     Output('refueling-table-container', 'children', allow_duplicate=True)],
    Input('confirm-delete-btn', 'n_clicks'),
    [State('admin-password-input', 'value'),
     State('delete-confirmation-store', 'data')],
    prevent_initial_call=True
)
def confirm_delete(n_clicks, admin_password, delete_data):
    """Confirm and execute deletion"""
    if not n_clicks or not delete_data:
        raise PreventUpdate
    
    user_data = get_user_data()
    if not user_data:
        return True, create_notification("❌ Not authenticated", "danger"), '', *[dash.no_update]*3
    
    # Verify admin password
    if not verify_admin_password(admin_password):
        return True, create_notification("❌ Invalid admin password", "danger"), '', *[dash.no_update]*3
    
    entity_type = delete_data['type']
    entity_id = delete_data['id']
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        if entity_type == 'machine':
            cursor.execute('UPDATE machines SET status = ? WHERE id = ?', ('inactive', entity_id))
            log_audit(cursor, user_data['id'], user_data['username'], 'delete', 'machines', entity_id,
                     f"Deleted machine {entity_id}")
        elif entity_type == 'operator':
            cursor.execute('UPDATE operators SET status = ? WHERE id = ?', ('inactive', entity_id))
            log_audit(cursor, user_data['id'], user_data['username'], 'delete', 'operators', entity_id,
                     "Deleted operator")
        elif entity_type == 'refuel':
            cursor.execute('DELETE FROM refuels WHERE id = ?', (entity_id,))
            log_audit(cursor, user_data['id'], user_data['username'], 'delete', 'refuels', entity_id,
                     "Deleted refuel entry")
        
        conn.commit()
        conn.close()
        
        # Return updated tables
        return (False, '', '', 
                render_machines_table() if entity_type == 'machine' else dash.no_update,
                render_operators_table() if entity_type == 'operator' else dash.no_update,
                render_refueling_table('all') if entity_type == 'refuel' else dash.no_update)
    except Exception as e:
        return True, create_notification(f"❌ Error: {str(e)}", "danger"), '', *[dash.no_update]*3

# Cancel delete
@app.callback(
    [Output('delete-modal', 'is_open', allow_duplicate=True),
     Output('admin-password-input', 'value', allow_duplicate=True)],
    Input('cancel-delete-btn', 'n_clicks'),
    prevent_initial_call=True
)
def cancel_delete(n_clicks):
    """Cancel deletion"""
    if n_clicks:
        return False, ''
    raise PreventUpdate

# ==================== RUN APPLICATION ====================
if __name__ == '__main__':
    init_db()
    print("=" * 60)
    print("J-INVESTMENTS FLEET MANAGEMENT SYSTEM")
    print("Dash Framework")
    print("=" * 60)
    print("✓ Database initialized")
    print("✓ Security enabled (RBAC + Admin password protection)")
    print("✓ Audit logging active")
    print("✓ CAT yellow branding applied")
    print("=" * 60)
    print("Starting server on http://localhost:8050")
    print("Default login: admin / admin123")
    print("⚠️  CHANGE DEFAULT PASSWORD IMMEDIATELY!")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=8050)