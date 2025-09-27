import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, db_path: str = "reports.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reports (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    tags TEXT NOT NULL,  -- JSON string
                    date TEXT NOT NULL   -- ISO format datetime string
                )
            ''')
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def create_report(self, report_id: str, title: str, content: str, tags: List[str], date: datetime) -> Dict[str, Any]:
        """Create a new report in the database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reports (id, title, content, tags, date)
                VALUES (?, ?, ?, ?, ?)
            ''', (report_id, title, content, json.dumps(tags), date.isoformat()))
            conn.commit()
        
        return {
            "id": report_id,
            "title": title,
            "content": content,
            "tags": tags,
            "date": date
        }
    
    def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific report by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, content, tags, date FROM reports WHERE id = ?', (report_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "id": row[0],
                    "title": row[1],
                    "content": row[2],
                    "tags": json.loads(row[3]),
                    "date": datetime.fromisoformat(row[4])
                }
            return None
    
    def get_reports(self, search_text: Optional[str] = None, tag: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get reports, optionally filtered by text and/or tag"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            reports = []

            # Base query
            base_query = 'SELECT id, title, content, tags, date FROM reports'
            params = []

            # Is text search required
            if search_text:
                base_query += ' WHERE title LIKE ? OR content LIKE ?'
                pattern = f'%{search_text}%'
                params.extend([pattern, pattern])

            cursor.execute(base_query, params)
            rows = cursor.fetchall()

            for row in rows:
                report_tags = json.loads(row[3])
                # If tag filtering is required
                if tag and tag not in report_tags:
                    continue
                reports.append({
                    "id": row[0],
                    "title": row[1],
                    "content": row[2],
                    "tags": report_tags,
                    "date": datetime.fromisoformat(row[4])
                })

            return reports

# Global database instance
db_manager = DatabaseManager()
