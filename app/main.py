from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.tickets import router as tickets_router
from app.models.db import Base, engine


def create_app():
    app = FastAPI(title="Mesa de Ayuda API")

    # ✅ CORS (ESTO ES LO QUE FALTABA)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 🔹 CREA LAS TABLAS AL ARRANCAR
    Base.metadata.create_all(bind=engine)

    app.include_router(health_router)
    app.include_router(tickets_router)

    return app


app = create_app()
