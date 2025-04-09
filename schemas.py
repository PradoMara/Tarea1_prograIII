from pydantic import BaseModel

class PersonajeIn(BaseModel):
    nombre: str

class MisionIn(BaseModel):
    descripcion: str
    xp: int
