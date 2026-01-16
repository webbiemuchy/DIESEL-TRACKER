"""
Configuration for J-INVESTMENTS Fleet Management
"""

# Color scheme from CAT branding
COLORS = {
    'cat_yellow': '#FFB400',
    'cat_yellow_dark': '#cc9000',
    'carbon': '#1a1a1a',
    'steel': '#2d2d2d',
    'text_bright': '#f0f0f0',
    'text_dim': '#a0a0a0',
    'danger': '#ff4d4d',
    'success': '#2ecc71',
    'bg_dark': '#0a0a0a',
    'warning': '#f39c12',
    'info': '#3498db'
}

# Styles
HEADER_STYLE = {
    'background': '#000',
    'borderBottom': f'2px solid {COLORS["cat_yellow"]}',
    'padding': '0.5rem 1.5rem',
    'position': 'sticky',
    'top': '0',
    'zIndex': '100'
}

CARD_STYLE = {
    'background': '#151515',
    'border': '1px solid #333',
    'borderRadius': '4px',
    'padding': '1.5rem',
    'marginBottom': '1rem'
}

BUTTON_PRIMARY = {
    'background': COLORS['cat_yellow'],
    'color': '#000',
    'border': 'none',
    'fontWeight': 'bold',
    'textTransform': 'uppercase',
    'borderRadius': '3px'
}

BUTTON_DANGER = {
    'background': COLORS['danger'],
    'color': 'white',
    'border': 'none',
    'fontWeight': 'bold',
    'textTransform': 'uppercase',
    'borderRadius': '3px'
}

INPUT_STYLE = {
    'background': '#222',
    'border': '1px solid #444',
    'color': 'white',
    'borderRadius': '3px'
}

TABLE_STYLE = {
    'style_table': {
        'overflowX': 'auto',
        'backgroundColor': '#151515'
    },
    'style_header': {
        'backgroundColor': '#000',
        'color': COLORS['text_dim'],
        'fontWeight': 'bold',
        'textTransform': 'uppercase',
        'fontSize': '0.8rem',
        'border': '1px solid #333'
    },
    'style_cell': {
        'backgroundColor': '#151515',
        'color': COLORS['text_bright'],
        'border': '1px solid #222',
        'textAlign': 'left',
        'padding': '12px'
    },
    'style_data_conditional': [
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#1a1a1a'
        }
    ]
}

# Role-based permissions
ROLE_PERMISSIONS = {
    'admin': {
        'machines': ['read', 'write', 'delete', 'admin'],
        'operators': ['read', 'write', 'delete', 'admin'],
        'refuels': ['read', 'write', 'delete', 'admin'],
        'settings': ['read', 'write', 'admin'],
        'users': ['read', 'write', 'delete', 'admin'],
        'reports': ['read', 'write', 'admin']
    },
    'manager': {
        'machines': ['read', 'write', 'delete'],
        'operators': ['read', 'write', 'delete'],
        'refuels': ['read', 'write', 'delete'],
        'settings': ['read'],
        'users': ['read'],
        'reports': ['read', 'write']
    },
    'data_entry': {
        'machines': ['read', 'write'],
        'operators': ['read', 'write'],
        'refuels': ['read', 'write'],
        'settings': ['read'],
        'users': [],
        'reports': ['read']
    },
    'viewer': {
        'machines': ['read'],
        'operators': ['read'],
        'refuels': ['read'],
        'settings': ['read'],
        'users': [],
        'reports': ['read']
    }
}

DATABASE = 'j_investments_fleet.db'
