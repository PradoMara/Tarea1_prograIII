from sqlalchemy import Table, Column, Integer, String, ForeignKey
from database import metadata

personajes = Table(
    "personajes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", String, unique=True),
    Column("experiencia", Integer, default=0)
)

misiones = Table(
    "misiones",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("descripcion", String),
    Column("xp", Integer)
)

personaje_mision = Table(
    "personaje_mision",
    metadata,
    Column("personaje_id", Integer, ForeignKey("personajes.id")),
    Column("mision_id", Integer, ForeignKey("misiones.id"))
)
