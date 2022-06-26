from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.marketplace.routes import marketplace_route
from app.handlers import setup_exception_handlers


def make_app() -> FastAPI:
    load_dotenv()
    
    app = FastAPI()

    app.include_router(marketplace_route.router, prefix="")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_exception_handlers(app)

    return app

app = make_app()

import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)