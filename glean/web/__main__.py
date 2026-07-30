"""Entry point for running the Paper-Glean web server."""

from __future__ import annotations

import argparse
import os

import uvicorn

from glean.web.main import create_app

app = create_app()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Paper-Glean web server")
    parser.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"), help="Host to bind to")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")), help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    args = parser.parse_args()
    
    uvicorn.run("glean.web.__main__:app", host=args.host, port=args.port, reload=args.reload)
