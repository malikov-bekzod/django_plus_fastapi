# myproject/asgi.py

import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django ASGI application
django_asgi_app = get_asgi_application()

# Import the FastAPI app
from api.main import app as fastapi_app

# Create a new ASGI application that mounts both Django and FastAPI
class CombinedASGIApp:
    def __init__(self, django_app, fastapi_app):
        self.django_app = django_app
        self.fastapi_app = fastapi_app

    async def __call__(self, scope, receive, send):
        if scope['type'] in {'http', 'websocket'}:
            if scope['path'].startswith('/api'):
                scope['path'] = scope['path'][4:]  # Remove '/api' prefix for FastAPI
                await self.fastapi_app(scope, receive, send)
            else:
                await self.django_app(scope, receive, send)
        else:
            raise NotImplementedError(f"Unknown scope type {scope['type']}")

application = CombinedASGIApp(django_asgi_app, fastapi_app)