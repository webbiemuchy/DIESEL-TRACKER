"""
Database operations for J-INVESTMENTS Fleet Management
"""

import sqlite3
import hashlib
import uuid
import json
from datetime import datetime
from flask import session

from config import DATABASE, ROLE_PERMISSIONS

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_uuid():
    """Generate unique ID"""
    return str(uuid.uuid4())

def log_audit(cursor, user_id, username, action, entity_type=None, entity_id=None, details=None):
    """Log audit trail"""
    cursor.execute('''
        INSERT INTO audit_log (user_id, username, action, entity_type, entity_id, details)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, username, action, entity_type, entity_id, details))

def check_permission(user_data, resource, permission):
    """Check if user has permission for resource"""
    if not user_data:
        return False
    
    role = user_data.get('role')
    if role == 'admin':
        return True
    
    # Check custom permissions first
    if user_data.get('permissions'):
        try:
            perms = json.loads(user_data['permissions'])
            return permission in perms.get(resource, [])
        except:
            pass
    
    # Fall back to role permissions
    return permission in ROLE_PERMISSIONS.get(role, {}).get(resource, [])

def verify_admin_password(password):
    """Verify admin password for delete operations"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) as count FROM users 
        WHERE role = 'admin' AND password_hash = ? AND active = 1
    ''', (hash_password(password),))
    result = cursor.fetchone()
    conn.close()
    return result['count'] > 0

def get_user_data():
    """Get current user data from session"""
    user_id = session.get('user_id')
    if not user_id:
        return None
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ? AND active = 1', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    return dict(user) if user else None

def init_db():
    """Initialize enterprise database"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            role TEXT NOT NULL,
            permissions TEXT,
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            last_login TIMESTAMP
        )
    ''')
    
    # Machines table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS machines (
            id TEXT PRIMARY KEY,
            model TEXT NOT NULL,
            rate REAL NOT NULL,
            capacity REAL NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')
    
    # Operators table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS operators (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            badge TEXT NOT NULL UNIQUE,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')
    
    # Refuels table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS refuels (
            id TEXT PRIMARY KEY,
            timestamp BIGINT NOT NULL,
            machine_id TEXT NOT NULL,
            operator_id TEXT NOT NULL,
            usage REAL NOT NULL,
            fuel REAL NOT NULL,
            notes TEXT,
            created_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (machine_id) REFERENCES machines(id),
            FOREIGN KEY (operator_id) REFERENCES operators(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')
    
    # Settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id TEXT PRIMARY KEY,
            tolerance REAL NOT NULL DEFAULT 10,
            company_name TEXT DEFAULT 'J-INVESTMENTS',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_by TEXT,
            FOREIGN KEY (updated_by) REFERENCES users(id)
        )
    ''')
    
    # Audit log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id TEXT NOT NULL,
            username TEXT NOT NULL,
            action TEXT NOT NULL,
            entity_type TEXT,
            entity_id TEXT,
            details TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Create indices for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_refuels_timestamp ON refuels(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_refuels_machine ON refuels(machine_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_refuels_operator ON refuels(operator_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp)')
    
    # Create default admin user if not exists
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        admin_id = generate_uuid()
        permissions = json.dumps({
            'machines': ['read', 'write', 'delete', 'admin'],
            'operators': ['read', 'write', 'delete', 'admin'],
            'refuels': ['read', 'write', 'delete', 'admin'],
            'settings': ['read', 'write', 'admin'],
            'users': ['read', 'write', 'delete', 'admin'],
            'reports': ['read', 'write', 'admin']
        })
        cursor.execute('''
            INSERT INTO users (id, username, password_hash, full_name, email, role, permissions)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (admin_id, 'admin', hash_password('admin123'), 'System Administrator', 
              'admin@j-investments.com', 'admin', permissions))
        
        log_audit(cursor, admin_id, 'admin', 'system_initialized', 'system', 'db', 
                 'Database initialized with default admin account')
    
    # Create default settings if not exists
    cursor.execute("SELECT COUNT(*) FROM settings")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO settings (id, tolerance, company_name) 
            VALUES ('current', 10, 'J-INVESTMENTS')
        ''')
    
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully")
