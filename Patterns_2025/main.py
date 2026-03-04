import sys

import connexion
from flask import request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.reference_api import router as reference_router
from Src.start_manager import start_manager
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
start_manager().start()

app = FastAPI(
    title="Учёт остатков и рецептур",
    description="Курсовой проект — справочники, остатки, рецепты",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роуты
app.include_router(reference_router)

@app.get("/")
async def root():
    return {"message": "API запущен! Документация: /docs"}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 8080)
