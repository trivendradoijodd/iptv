# python serve.py --file output.m3u --port 8000
from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse
from utils.driver import driver

class M3UHandler(BaseHTTPRequestHandler):
    def __init__(self, m3u_file, *args, **kwargs):
        self.m3u_file = m3u_file
        super().__init__(*args, **kwargs)

    def do_GET(self):
        try:
            if self.path == '/refresh':
                driver(True)
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.wfile.write(b'Refreshed the file!')
                self.end_headers()
            else:
                # Read the M3U file
                with open(self.m3u_file, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/x-mpegurl')
                self.send_header('Content-Disposition', f'attachment; filename="{self.m3u_file}"')
                self.end_headers()
                
                # Write content
                self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'File not found')
        except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))

        

def run_server(port, m3u_file):
    # Create handler class with the m3u_file parameter
    handler = lambda *args: M3UHandler(m3u_file, *args)
    
    # Create server
    server = HTTPServer(('', port), handler)
    print(f'Server started on port {port}')
    print(f'Serving M3U file: {m3u_file}')
    print(f'Access your playlist at: http://localhost:{port}')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down server...')
        server.server_close()

def main():
    parser = argparse.ArgumentParser(description='Start an HTTP server to serve an M3U file')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on (default: 8000)')
    parser.add_argument('--file', required=True, help='Path to the M3U file to serve')
    
    args = parser.parse_args()
    
    run_server(args.port, args.file)

if __name__ == '__main__':
    main()