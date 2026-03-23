from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db

router = APIRouter(prefix="/municipios", tags=["Municipios"])


@router.get("/{id_municipio}")
async def buscar(
    id_municipio: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        text("""
            SELECT a.id_afiliado, a.documento, a.nombre, a.apellido,
                   a.estado, m.nombre AS municipio
            FROM afiliado a
            JOIN municipio m ON m.id_municipio = a.id_municipio
            WHERE a.id_municipio = :id_municipio
            ORDER BY a.apellido, a.nombre
            LIMIT 30
        """),
        {"id_municipio": id_municipio},
    )
    rows = result.mappings().all()
    if not rows:
        raise HTTPException(status_code=404, detail="Sin afiliados para ese municipio")
    return list(rows)
