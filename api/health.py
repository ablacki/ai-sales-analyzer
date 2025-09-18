"""
Simple health check endpoint to verify Vercel environment variables
"""

import os
import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Health check endpoint"""
        try:
            # Get API key from environment
            api_key = os.environ.get('ANTHROPIC_API_KEY')

            health_data = {
                'status': 'healthy',
                'timestamp': '2024-01-01T00:00:00Z',
                'environment': {
                    'total_env_vars': len(os.environ),
                    'has_anthropic_key': 'ANTHROPIC_API_KEY' in os.environ,
                    'api_key_length': len(api_key) if api_key else 0,
                    'api_key_prefix': api_key[:15] + '...' if api_key and len(api_key) > 15 else 'NOT_FOUND',
                    'all_api_keys': [k for k in os.environ.keys() if 'API' in k.upper()],
                    'anthropic_vars': [k for k in os.environ.keys() if 'ANTHROP' in k.upper()],
                    'vercel_vars': [k for k in os.environ.keys() if 'VERCEL' in k.upper()]
                }
            }

            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(health_data, indent=2).encode('utf-8'))

        except Exception as e:
            error_data = {
                'status': 'error',
                'error': str(e),
                'environment': {
                    'total_env_vars': len(os.environ),
                    'env_var_keys': list(os.environ.keys())[:10]  # First 10 only
                }
            }

            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_data, indent=2).encode('utf-8'))