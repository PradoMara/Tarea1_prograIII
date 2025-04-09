from fastapi import APIRouter, HTTPException
from database import database
from models import personajes, misiones
from schemas import PersonajeIn, MisionIn
from cola import ColaMisiones

router = APIRouter()
colas_personajes = {}  # Para almacenar colas FIFO por personaje

# Crear nuevo personaje
@router.post("/personajes")
async def crear_personaje(p: PersonajeIn):
    # Verificar si ya existe un personaje con ese nombre
    query = personajes.select().where(personajes.c.nombre == p.nombre)
    existing_personaje = await database.fetch_one(query)
    if existing_personaje:
        raise HTTPException(status_code=400, detail="El personaje ya existe.")

    # Si no existe, insertar el nuevo personaje
    query = personajes.insert().values(nombre=p.nombre)
    personaje_id = await database.execute(query)
    colas_personajes[personaje_id] = ColaMisiones()
    return {"id": personaje_id, **p.dict()}


# Crear nueva misión
@router.post("/misiones")
async def crear_mision(m: MisionIn):
    query = misiones.insert().values(descripcion=m.descripcion, xp=m.xp)
    mision_id = await database.execute(query)
    return {"id": mision_id, **m.dict()}

# Aceptar misión (encolar)
@router.post("/personajes/{personaje_id}/misiones/{mision_id}")
async def aceptar_mision(personaje_id: int, mision_id: int):
    if personaje_id not in colas_personajes:
        colas_personajes[personaje_id] = ColaMisiones()
    colas_personajes[personaje_id].enqueue(mision_id)
    return {"mensaje": "Misión aceptada y encolada."}

# Completar misión (desencolar + sumar XP)
@router.post("/personajes/{personaje_id}/completar")
async def completar_mision(personaje_id: int):
    if personaje_id not in colas_personajes or colas_personajes[personaje_id].is_empty():
        raise HTTPException(400, "No hay misiones pendientes.")

    mision_id = colas_personajes[personaje_id].dequeue()

    mision = await database.fetch_one(misiones.select().where(misiones.c.id == mision_id))
    personaje = await database.fetch_one(personajes.select().where(personajes.c.id == personaje_id))

    nueva_xp = (personaje.experiencia or 0) + mision.xp
    await database.execute(personajes.update().where(personajes.c.id == personaje_id).values(experiencia=nueva_xp))

    return {"mensaje": "Misión completada", "xp_total": nueva_xp}

# Listar misiones en orden FIFO
@router.get("/personajes/{personaje_id}/misiones")
async def listar_misiones(personaje_id: int):
    if personaje_id not in colas_personajes:
        return []
    ids = list(colas_personajes[personaje_id].misiones)
    query = misiones.select().where(misiones.c.id.in_(ids))
    return await database.fetch_all(query)
