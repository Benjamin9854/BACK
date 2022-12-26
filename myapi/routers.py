from fastapi import APIRouter
from typing import Optional
from sqlmodel import Session
from myapi.db import engine

from myapi.app import (
    create_usuario,
    ingresar_usuario,
)

from myapi.models import (
    Usuario,
    UsuarioCreate,
)

router = APIRouter()


@router.post("/crear/", response_model=UsuarioCreate)
async def crear_usu(usu_c: UsuarioCreate):
    create_usuario(usu=usu_c)


    

