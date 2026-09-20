# Portfolio API

API de visitas del portafolio interactivo ([sadielrojas.vercel.app](https://sadielrojas.vercel.app)).
Cuenta qué secciones abren los visitantes y alimenta el tablero de la plaza.

**Stack:** Python · FastAPI · SQLAlchemy · PostgreSQL (Neon) · pytest · desplegada en Vercel.

## Endpoints

| Método | Ruta | Qué hace |
| --- | --- | --- |
| `POST` | `/visits` | Registra la apertura de una sección. Una visita por sesión y sección. |
| `GET` | `/visits/stats` | Conteo por sección, ordenado. Acepta `?days=N`. |
| `GET` | `/health` | Estado del servicio. |

Documentación interactiva en `/docs`.

## Decisiones de diseño

- **Una fila por visita**, no un contador: permite sacar tendencias por periodo sin cambiar el modelo.
- **Sin cookies ni datos personales**: solo un identificador al azar que genera el navegador por pestaña.
- **La base de datos garantiza el conteo**: una restricción de unicidad `(session_id, section)` impide contar dos veces, incluso con peticiones simultáneas.
- **Lista blanca de secciones** con `Literal`, así una sección inventada se rechaza con 422 antes de tocar la base de datos.

## Correr en local

```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
pytest
fastapi dev app/main.py
```

Sin configuración usa SQLite en un archivo local. Con `DATABASE_URL` apunta a PostgreSQL.