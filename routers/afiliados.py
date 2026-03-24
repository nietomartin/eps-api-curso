from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db
from schemas import AfiliadoResponse, ElegibilidadResponse

router = APIRouter(prefix="/afiliados", tags=["Afiliados"])


@router.get(
    "/{documento}/elegibilidad",
    response_model=ElegibilidadResponse,
    summary="Verificar elegibilidad de un afiliado",
)
async def verificar_elegibilidad(documento: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("""
            SELECT id_afiliado, documento, nombre, apellido,
                   regimen, estado, fecha_afil AS fecha_afiliacion
            FROM afiliado
            WHERE documento = :doc
        """),
        {"doc": documento},
    )
    row = result.mappings().first()
    if not row:
        raise HTTPException(404, detail="Afiliado no encontrado")
    afiliado = AfiliadoResponse(**row)
    es_elegible = afiliado.estado == "ACTIVO"
    return ElegibilidadResponse(
        afiliado=afiliado,
        es_elegible=es_elegible,
        mensaje="Activo y elegible para servicios"
        if es_elegible
        else f"Afiliado en estado: {afiliado.estado}",
    )


@router.get("/", response_model=list[AfiliadoResponse], summary="Listar afiliados")
async def listar_afiliados(limite: int = 20, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text(
            "SELECT id_afiliado, documento, nombre, apellido, regimen, estado, fecha_afil AS fecha_afiliacion FROM afiliado LIMIT :lim"
        ),
        {"lim": min(limite, 100)},
    )
    return [AfiliadoResponse(**r) for r in result.mappings().all()]
