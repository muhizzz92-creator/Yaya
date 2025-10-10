from http.server import BaseHTTPRequestHandler
import json
from supabase import create_client, Client
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        SUPABASE_URL = os.environ.get("SUPABASE_URL")
        SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")
        
        # Проверяем секретный ключ авторизации от нашей программы
        auth_header = self.headers.get('Authorization')
        if not auth_header or auth_header != f'Bearer {SUPABASE_SERVICE_KEY}':
            self._send_response(401, {"error": "Unauthorized"})
            return

        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            self._send_response(500, {"error": "Supabase service credentials not configured"})
            return

        try:
            supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
            
            response = supabase.table('homework_results').select('*').eq('is_checked', False).execute()
            results = response.data
            
            if results:
                ids_to_update = [item['id'] for item in results]
                supabase.table('homework_results').update({'is_checked': True}).in_('id', ids_to_update).execute()

            self._send_response(200, results)
            
        except Exception as e:
            self._send_response(500, {"error": str(e)})

    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))