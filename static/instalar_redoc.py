import urllib.request

urllib.request.urlretrieve(  # nosec
    "https://cdn.jsdelivr.net/npm/redoc@2.1.3/bundles/redoc.standalone.js",
    "api/static/redoc.standalone.js",
)
print("Descarga completada")
