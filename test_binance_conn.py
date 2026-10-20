"""
Test koneksi Binance API dengan berbagai cara
"""
import requests
import urllib.request
import socket

ENDPOINTS = [
    'https://api.binance.com',
    'https://api1.binance.com',
    'https://api2.binance.com',
    'https://api3.binance.com',
    'https://api4.binance.com',
    'https://data-api.binance.vision',  # alternative CDN endpoint
]

print("=== TEST KONEKSI BINANCE API ===")
print()

# Test 1: DNS resolve
print("[1] DNS Resolution Test:")
for ep in ENDPOINTS:
    host = ep.replace('https://', '')
    try:
        ip = socket.gethostbyname(host)
        print("  {} -> {}".format(host, ip))
    except Exception as e:
        print("  {} -> GAGAL DNS: {}".format(host, e))

print()

# Test 2: HTTP requests dengan berbagai timeout dan header
print("[2] HTTP Requests Test:")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
}

for ep in ENDPOINTS:
    try:
        resp = requests.get(ep + '/api/v3/ping', 
                           headers=headers, 
                           timeout=15,
                           verify=True)
        print("  {} -> Status: {} [OK]".format(ep, resp.status_code))
    except requests.exceptions.SSLError as e:
        print("  {} -> SSL ERROR: {}".format(ep, str(e)[:80]))
    except requests.exceptions.ConnectionError as e:
        print("  {} -> CONNECTION ERROR: {}".format(ep, str(e)[:80]))
    except requests.exceptions.Timeout:
        print("  {} -> TIMEOUT (>15s)".format(ep))
    except Exception as e:
        print("  {} -> ERROR: {}".format(ep, str(e)[:80]))

print()

# Test 3: Coba tanpa SSL verify
print("[3] HTTP Requests Test (verify=False / bypass SSL):")
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

for ep in ENDPOINTS[:3]:
    try:
        resp = requests.get(ep + '/api/v3/ping',
                           headers=headers,
                           timeout=15,
                           verify=False)
        print("  {} -> Status: {} [OK]".format(ep, resp.status_code))
    except requests.exceptions.ConnectionError as e:
        print("  {} -> CONNECTION ERROR: {}".format(ep, str(e)[:80]))
    except Exception as e:
        print("  {} -> ERROR: {}".format(ep, str(e)[:80]))

print()

# Test 4: Cek server time endpoint
print("[4] Cek Binance Server Time (api.binance.com/api/v3/time):")
try:
    resp = requests.get('https://api.binance.com/api/v3/time', 
                       headers=headers, timeout=15)
    print("  Status: " + str(resp.status_code))
    print("  Response: " + str(resp.text[:200]))
except Exception as e:
    print("  ERROR: " + str(e)[:150])

print()

# Test 5: cek apakah internet umum bisa
print("[5] Test internet umum (google.com):")
try:
    resp = requests.get('https://www.google.com', timeout=10)
    print("  google.com -> Status: {} [OK]".format(resp.status_code))
except Exception as e:
    print("  google.com -> ERROR: " + str(e)[:100])
