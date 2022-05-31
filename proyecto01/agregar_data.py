from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import enlace

engine = create_engine(enlace)

from app import Docente

Session = sessionmaker(bind=engine)
session = Session()

# se crea un objetos de tipo Docente
docente1 = Docente(nombre="Tony", apellido="García", \
        ciudad="Loja")

docente2 = Docente(nombre="Luis", apellido="Borrero", \
        ciudad="Loja")

docente3 = Docente(nombre="Ana", apellido="Salcedo", \
        ciudad="Zamora")

docente4 = Docente(nombre="Monica", apellido="Valenzuela", \
        ciudad="Zamora")

# se agrega los objetos
# a la sesión
# a la espera de un commit
# para agregar un registro a la base de
# datos
session.add(docente1)
session.add(docente2)
session.add(docente3)
session.add(docente4)

# se confirma las transacciones
session.commit()
