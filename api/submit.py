from http.server import BaseHTTPRequestHandler
import json
from supabase import create_client, Client
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        SUPABASE_URL = os.environ.get("SUPABASE_URL")
        SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
        
        if not SUPABASE_URL or not SUPABASE_ANON_KEY:
            self._send_response(500, {"error": "Supabase credentials not configured"})
            return
        
        try:
            content_length = int(self.headers['Content-Length'])
            post_data_bytes = self.rfile.read(content_length)
            form_data = json.loads(post_data_bytes)

            supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
            
            insert_data = {
                "student_info": form_data.get("student_id", "Unknown"),
                "lesson_info": form_data.get("lesson_id", "Unknown"),
                "answers_json": form_data.get("responses", {}),
            }
            
            supabase.table('homework_results').insert(insert_data).execute()

            self._send_response(200, {"message": "Result saved successfully"})
            
        except Exception as e:
            self._send_response(500, {"error": str(e)})

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))