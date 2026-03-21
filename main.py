from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles

from routers import afiliados
import subprocess, os

app = FastAPI(
    title='EPS API - Sector Subsidiado',
    version='1.0.0',
    description='API de elegibilidad y autorizaciones medicas',
    docs_url='/docs',
    redoc_url=None,
)

app.add_middleware(CORSMiddleware,
    allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

app.include_router(afiliados.router)
app.mount('/static', StaticFiles(directory='static'), name='static')

@app.get('/health')
async def health():
    return {'status': 'ok', 'version': '1.0.0'}

"""
Este decorador fue necesario ya que hubo que instalar redoc localmente
"""
@app.get('/redoc', include_in_schema=False)
async def redoc_html():
    return HTMLResponse(content="""
<!DOCTYPE html>
<html>
  <head>
    <title>EPS API - Documentacion</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body { margin: 0; padding: 0; }</style>
  </head>
  <body>
    <redoc spec-url='/openapi.json'></redoc>
    <script src="/static/redoc.standalone.js"></script>
  </body>
</html>
""")