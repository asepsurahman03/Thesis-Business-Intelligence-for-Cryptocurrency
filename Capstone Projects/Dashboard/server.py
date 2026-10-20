# -*- coding: utf-8 -*-
"""
Python Web Server & API Service for CryptoPredict AI Dashboard
Magister Informatika Konsentrasi Data Science - Universitas Nusa Putra
Menjalankan local server dan REST API endpoint untuk Dashboard Business Intelligence.
"""

import http.server
import socketserver
import os
import json
import webbrowser

PORT = 8050
DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))

class DashboardAPIHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DASHBOARD_DIR, **kwargs)

    def do_GET(self):
        # REST API Endpoints
        if self.path == '/api/kpi':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            kpi_data = {
                "dataset": "Binance Spot BTC/USDT (2021-2026)",
                "total_records": 43786,
                "walk_forward_folds": 24,
                "best_point_loss": {
                    "model": "GRU",
                    "rmse": 0.1058,
                    "rmse_sd": 0.0034,
                    "mae": 0.0948,
                    "mape": "13.13%"
                },
                "best_trading_utility": {
                    "model": "LSTM",
                    "directional_accuracy": "72.3%",
                    "sharpe_ratio": 1.45,
                    "var_95": "-2.34%",
                    "max_drawdown": "-8.9%"
                },
                "statistical_significance": {
                    "diebold_mariano_p": 0.014,
                    "kruskal_wallis_h": 18.4,
                    "kruskal_wallis_p": "< 0.001"
                }
            }
            self.wfile.write(json.dumps(kpi_data).encode('utf-8'))
            return

        elif self.path == '/api/models':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            models_benchmark = [
                {"model": "GRU Mechanism", "rmse": 0.1058, "mae": 0.0948, "mape": "13.13%", "da": "69.8%", "sharpe": 1.32, "var_95": "-2.70%"},
                {"model": "LSTM Topography", "rmse": 0.1145, "mae": 0.1008, "mape": "13.96%", "da": "72.3%", "sharpe": 1.45, "var_95": "-2.34%"},
                {"model": "Informer Transformer", "rmse": 0.1321, "mae": 0.1119, "mape": "14.82%", "da": "64.1%", "sharpe": 1.12, "var_95": "-3.15%"},
                {"model": "XGBoost Baseline", "rmse": 0.1524, "mae": 0.1260, "mape": "16.50%", "da": "58.4%", "sharpe": 0.95, "var_95": "-4.10%"}
            ]
            self.wfile.write(json.dumps(models_benchmark).encode('utf-8'))
            return

        # Default serve static files (index.html, style.css, app.js)
        return super().do_GET()

def run_server():
    os.chdir(DASHBOARD_DIR)
    handler = DashboardAPIHandler
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=" * 70)
        print(" CRYPTOPREDICT AI - BUSINESS INTELLIGENCE DSS DASHBOARD SERVER")
        print(" Universitas Nusa Putra - Magister Informatika (Data Science)")
        print("=" * 70)
        print(f"[*] Dashboard aktif dan berjalan pada: {url}")
        print(f"[*] Folder root web: {DASHBOARD_DIR}")
        print(f"[*] Tekan Ctrl+C untuk menghentikan server.")
        print("=" * 70)
        
        # Otomatis buka browser default
        try:
            webbrowser.open(url)
        except Exception:
            pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Server dihentikan oleh pengguna.")
            httpd.server_close()

if __name__ == '__main__':
    run_server()
