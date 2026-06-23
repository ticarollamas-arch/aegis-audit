import re
import sqlite3
from datetime import datetime

class LogAnalyzer:
    def __init__(self, log_path):
        self.log_path = log_path
        self.sensitive_patterns = [
            r'\.env.*',
            r'\.git/.*',
            r'wp-config\.php',
            r'composer\.json',
            r'id_rsa',
            r'\.aws/credentials'
        ]
        self.db_path = 'audit_logs.db'
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                risk_score INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def _save_to_db(self, ip, endpoint, risk_score):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO security_logs (ip_address, endpoint, risk_score) VALUES (?, ?, ?)',
            (ip, endpoint, risk_score)
        )
        conn.commit()
        conn.close()

    def analyze(self):
        findings = []
        # Regex simplificada para logs combinados do Apache/Nginx
        log_pattern = re.compile(r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<time>.*?)\] "(?P<method>GET|POST|HEAD|PUT|DELETE|OPTIONS) (?P<path>.*?) HTTP/.*" (?P<status>\d+) .*')
        
        with open(self.log_path, 'r') as file:
            for line in file:
                match = log_pattern.search(line)
                if match:
                    data = match.groupdict()
                    path = data['path']
                    
                    for pattern in self.sensitive_patterns:
                        if re.search(pattern, path, re.IGNORECASE):
                            risk_score = 90
                            finding = {
                                'ip': data['ip'],
                                'endpoint': path,
                                'timestamp': data['time'],
                                'risk_score': risk_score
                            }
                            findings.append(finding)
                            self._save_to_db(data['ip'], path, risk_score)
                            break
                            
        return findings
