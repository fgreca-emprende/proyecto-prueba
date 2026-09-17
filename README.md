# Proyecto Prueba - Supabase On-Premise Architecture

Arquitectura e infraestructura de integración para servicios backend, frontend (Vite) e inteligencia artificial, conectado a una instancia de **Supabase On-Premise** alojada en red local (`192.168.0.70`).

---

## 🏗️ Visión General de la Arquitectura

El sistema está diseñado bajo el principio de menor privilegio (*Principle of Least Privilege*) y separación estricta entre el cliente público y los servicios de backend:

```
                  ┌───────────────────────────────────────────────┐
                  │          Cliente Frontend (Vite)              │
                  │  - VITE_SUPABASE_URL                          │
                  │  - VITE_SUPABASE_ANON_KEY (Sujeto a RLS)      │
                  └───────────────────────┬───────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Supabase On-Premise Gateway (192.168.0.70)             │
│                                                                             │
│   Kong / Envoy Reverse Proxy (:8010 / :8000)                                │
│   ├── PostgREST (/rest/v1/) ─── PostgreSQL (Row Level Security activo)     │
│   ├── GoTrue    (/auth/v1/)                                                 │
│   └── Storage   (/storage/v1/)                                              │
└─────────────────────────────────────▲───────────────────────────────────────┘
                                      │
                  ┌───────────────────┴───────────────────────────┐
                  │         Servicios Backend / Workers           │
                  │  - SUPABASE_SERVICE_ROLE_KEY (Bypass RLS)     │
                  │  - GEMINI_API_KEY                             │
                  │  - Integraciones Gmail & HubSpot              │
                  └───────────────────────────────────────────────┘
```

---

## 📁 Estructura del Proyecto

```text
proyecto-prueba/
├── .env.example          # Plantilla sanitizada de variables de entorno para Git
├── .gitignore            # Exclusión de credenciales y artefactos de build
├── README.md             # Documentación técnica del proyecto
└── test_supabase.py      # Script de verificación de conectividad y endpoints
```

---

## 🔐 Configuración de Variables de Entorno

1. Copiar la plantilla de variables:
   ```bash
   cp .env.example .env
   ```
2. Completar las credenciales en el archivo `.env`:
   - `ANON_KEY` / `VITE_SUPABASE_ANON_KEY`: Clave pública para el cliente web (opera bajo RLS).
   - `SERVICE_ROLE_KEY` / `SUPABASE_SERVICE_ROLE_KEY`: Clave de administración exclusiva del backend. **Nunca debe exponerse al frontend.**
   - Integraciones externas: `GEMINI_API_KEY`, credenciales OAuth de Gmail y `HUBSPOT_CLIENT_SECRET`.

> [!WARNING]
> El archivo `.env` jamás debe versionarse en Git. Asegúrate de que permanezca listado en `.gitignore`.

---

## 🧪 Pruebas de Conectividad

Para verificar la comunicación directa contra la API de Supabase On-Premise:

```bash
python test_supabase.py <TU_SUPABASE_ANON_KEY_O_SERVICE_KEY>
```

El script validará:
1. Conectividad HTTP con el Gateway.
2. Endpoint de Storage API.
3. Health check de Auth (`/auth/v1/health`).
4. Esquema OpenAPI de PostgREST (`/rest/v1/`).
