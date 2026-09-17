"""
Script de verificación de conexión a Supabase en dev.lab
Uso:
    python test_supabase.py [TU_ANON_O_SERVICE_KEY]
"""

import sys
import urllib.request
import urllib.error
import json

SUPABASE_URL = "http://dev.lab:8000"

def test_connectivity():
    print(f"[*] Comprobando conexión básica con {SUPABASE_URL}...")
    try:
        req = urllib.request.Request(f"{SUPABASE_URL}/storage/v1/version")
        with urllib.request.urlopen(req, timeout=5) as resp:
            version = resp.read().decode('utf-8')
            print(f" [OK] Conectividad exitosa con el gateway Envoy de Supabase.")
            print(f"      Storage API Version: {version}")
    except Exception as e:
        print(f" [ERROR] No se pudo conectar al gateway: {e}")
        return False
    return True

def test_api_key(api_key):
    print(f"\n[*] Probando API Key contra REST (/rest/v1/) y Auth (/auth/v1/health)...")
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}"
    }

    # Test Auth
    try:
        req = urllib.request.Request(f"{SUPABASE_URL}/auth/v1/health", headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f" [OK] Auth API respondió con código {resp.status}")
    except urllib.error.HTTPError as e:
        print(f" [!] Auth API respondió HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f" [ERROR] Fallo al consultar Auth: {e}")

    # Test REST (PostgREST root schema)
    try:
        req = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/", headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode('utf-8')
            print(f" [OK] REST API respondió exitosamente con código {resp.status}")
            print(f"      Definición OpenAPI disponible (longitud: {len(data)} bytes)")
    except urllib.error.HTTPError as e:
        print(f" [!] REST API respondió HTTP {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f" [ERROR] Fallo al consultar REST: {e}")

if __name__ == "__main__":
    if test_connectivity():
        if len(sys.argv) > 1:
            key = sys.argv[1].strip()
            test_api_key(key)
        else:
            print("\n" + "="*60)
            print("Para probar la autenticación de datos o Auth:")
            print("Ejecuta: python test_supabase.py <TU_SUPABASE_ANON_KEY>")
            print("="*60)
