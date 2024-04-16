from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Crear la base de datos
Base = declarative_base()

# Definir la clase de la tabla 'Receta'
class Receta(Base):
    __tablename__ = 'recetas'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    ingredientes = Column(Text, nullable=False)
    pasos = Column(Text, nullable=False)

# Función para conectar a la base de datos
def conectar_base_datos():
    engine = create_engine('sqlite:///recetas.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session(), engine

# Función para agregar una nueva receta
def agregar_receta(session):
    nombre = input("Nombre de la receta: ")
    ingredientes = input("Ingredientes (separados por comas): ")
    pasos = input("Pasos de la receta: ")

    nueva_receta = Receta(nombre=nombre, ingredientes=ingredientes, pasos=pasos)
    session.add(nueva_receta)
    session.commit()
    print("Receta agregada con éxito.")

# Función para actualizar una receta existente
def actualizar_receta(session):
    id_receta = input("Ingrese el ID de la receta que desea actualizar: ")

    receta = session.query(Receta).filter_by(id=id_receta).first()

    if receta:
        print(f"Receta actual: {receta}")
        receta.nombre = input("Nuevo nombre de la receta (deje en blanco para no cambiar): ") or receta.nombre
        receta.ingredientes = input("Nuevos ingredientes (deje en blanco para no cambiar): ") or receta.ingredientes
        receta.pasos = input("Nuevos pasos de la receta (deje en blanco para no cambiar): ") or receta.pasos

        session.commit()
        print("Receta actualizada con éxito.")
    else:
        print("Receta no encontrada.")

# Función para eliminar una receta existente
def eliminar_receta(session):
    id_receta = input("Ingrese el ID de la receta que desea eliminar: ")

    receta = session.query(Receta).filter_by(id=id_receta).first()

    if receta:
        session.delete(receta)
        session.commit()
        print("Receta eliminada con éxito.")
    else:
        print("Receta no encontrada.")

# Función para ver un listado de recetas
def ver_listado_recetas(session):
    recetas = session.query(Receta).all()

    if recetas:
        for receta in recetas:
            print(f"ID: {receta.id}, Nombre: {receta.nombre}, Ingredientes: {receta.ingredientes}, Pasos: {receta.pasos}")
    else:
        print("No hay recetas en el libro.")

# Función principal
def main():
    session, _ = conectar_base_datos()

    while True:
        print("\n--- Menú ---")
        print("a) Agregar nueva receta")
        print("c) Actualizar receta existente")
        print("d) Eliminar receta existente")
        print("e) Ver listado de recetas")
        print("f) Salir")

        opcion = input("Ingrese la opción deseada: ").lower()

        if opcion == 'a':
            agregar_receta(session)
        elif opcion == 'c':
            actualizar_receta(session)
        elif opcion == 'd':
            eliminar_receta(session)
        elif opcion == 'e':
            ver_listado_recetas(session)
        elif opcion == 'f':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, elija una opción válida.")

    session.close()

if __name__ == "__main__":
    main()
