import os
from models import Estudiante, Materia, Matricula
from shared.json_manager import GestorJSON
from shared.herramientas import normalizar_email, email_valido

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
gestor_estudiantes = GestorJSON(os.path.join(BASE_DIR, "data", "estudiantes.json"))
gestor_materias = GestorJSON(os.path.join(BASE_DIR, "data", "materias.json"))
gestor_matriculas = GestorJSON(os.path.join(BASE_DIR, "data", "matriculas.json"))


# Funciones genéricas de persistencia/colecciones.
def leer_objetos(gestor, clase):
    return [clase.desde_diccionario(registro) for registro in gestor.leer()]


def obtener_por_id(objetos, id_registro):
    try:
        id_registro = int(id_registro)
    except (TypeError, ValueError):
        return None
    return next((obj for obj in objetos if obj.id == id_registro), None)


def buscar(objetos, termino, atributos):
    termino = str(termino).strip().lower()
    return [obj for obj in objetos if any(termino in str(getattr(obj, atributo, "")).lower()
                                           for atributo in atributos)]


def siguiente_id(gestor):
    ids = [int(registro.get("id", 0)) for registro in gestor.leer()]
    return max(ids, default=0) + 1


def guardar_nuevo(gestor, objeto):
    datos = gestor.leer()
    datos.append(objeto.a_diccionario())
    gestor.guardar(datos)
    return objeto


def reemplazar(gestor, objeto):
    datos = gestor.leer()
    for indice, registro in enumerate(datos):
        if int(registro.get("id", -1)) == objeto.id:
            datos[indice] = objeto.a_diccionario()
            gestor.guardar(datos)
            return True
    return False


def eliminar(gestor, id_registro):
    datos = gestor.leer()
    nuevos = [r for r in datos if int(r.get("id", -1)) != int(id_registro)]
    if len(nuevos) == len(datos):
        return False
    gestor.guardar(nuevos)
    return True


def ids_registrados(gestor):
    return {int(r["id"]) for r in gestor.leer() if "id" in r}


def indice_por_id(objetos):
    return {obj.id: obj for obj in objetos}


# ESTUDIANTES
def obtener_estudiantes():
    return leer_objetos(gestor_estudiantes, Estudiante)


def obtener_estudiante(id_registro):
    return obtener_por_id(obtener_estudiantes(), id_registro)


def buscar_estudiantes(termino):
    return buscar(obtener_estudiantes(), termino, ("nombre", "apellido", "email", "carnet", "carrera"))


def crear_estudiante(datos):
    nombre = str(datos.get("nombre", "")).strip()
    apellido = str(datos.get("apellido", "")).strip()
    email = normalizar_email(datos.get("email", ""))
    carnet = str(datos.get("carnet", "")).strip().upper()
    carrera = str(datos.get("carrera", "")).strip().title()
    if not all((nombre, apellido, email, carnet)):
        raise ValueError("Nombre, apellido, email y carnet son obligatorios.")
    if not email_valido(email):
        raise ValueError("El email no tiene un formato válido.")
    estudiantes = obtener_estudiantes()
    if email in {e.email for e in estudiantes}:
        raise ValueError("Ese email ya está registrado.")
    if carnet in {e.carnet for e in estudiantes}:
        raise ValueError("Ese carnet ya está registrado.")
    estudiante = Estudiante(siguiente_id(gestor_estudiantes), nombre, apellido, email, carnet, carrera)
    return guardar_nuevo(gestor_estudiantes, estudiante)


def actualizar_estudiante(id_registro, cambios):
    estudiante = obtener_estudiante(id_registro)
    if not estudiante:
        raise ValueError("No existe un estudiante con ese ID.")
    nombre = str(cambios.get("nombre", estudiante.nombre)).strip()
    apellido = str(cambios.get("apellido", estudiante.apellido)).strip()
    email = normalizar_email(cambios.get("email", estudiante.email))
    carnet = str(cambios.get("carnet", estudiante.carnet)).strip().upper()
    carrera = str(cambios.get("carrera", estudiante.carrera)).strip().title()
    if not all((nombre, apellido, email, carnet)):
        raise ValueError("Nombre, apellido, email y carnet son obligatorios.")
    if not email_valido(email):
        raise ValueError("El email no tiene un formato válido.")
    for otro in obtener_estudiantes():
        if otro.id != estudiante.id and otro.email == email:
            raise ValueError("Ese email ya está registrado.")
        if otro.id != estudiante.id and otro.carnet == carnet:
            raise ValueError("Ese carnet ya está registrado.")
    actualizado = Estudiante(estudiante.id, nombre, apellido, email, carnet, carrera)
    reemplazar(gestor_estudiantes, actualizado)
    return actualizado


def eliminar_estudiante(id_registro):
    if any(m.estudiante_id == int(id_registro) for m in obtener_matriculas()):
        raise ValueError("No se puede eliminar: el estudiante tiene matrículas registradas.")
    if not eliminar(gestor_estudiantes, id_registro):
        raise ValueError("No existe un estudiante con ese ID.")
    return True


# MATERIAS
def obtener_materias():
    return leer_objetos(gestor_materias, Materia)


def obtener_materia(id_registro):
    return obtener_por_id(obtener_materias(), id_registro)


def buscar_materias(termino):
    return buscar(obtener_materias(), termino, ("nombre", "codigo"))


def materias_sin_cupo():
    return [materia for materia in obtener_materias() if not materia.hay_cupo()]


def crear_materia(datos):
    nombre = str(datos.get("nombre", "")).strip()
    codigo = str(datos.get("codigo", "")).strip().upper()
    try:
        creditos = int(datos.get("creditos", 0))
        cupos = int(datos.get("cupos", Materia.CUPOS_MAXIMOS))
    except (TypeError, ValueError):
        raise ValueError("Créditos y cupos deben ser números enteros.")
    if not nombre or not codigo:
        raise ValueError("Nombre y código son obligatorios.")
    if any(m.codigo == codigo for m in obtener_materias()):
        raise ValueError("Ese código de materia ya está registrado.")
    if not 1 <= creditos <= 10:
        raise ValueError("Los créditos deben estar entre 1 y 10.")
    if not 0 <= cupos <= Materia.CUPOS_MAXIMOS:
        raise ValueError(f"Los cupos deben estar entre 0 y {Materia.CUPOS_MAXIMOS}.")
    materia = Materia(siguiente_id(gestor_materias), nombre, codigo, creditos, cupos)
    return guardar_nuevo(gestor_materias, materia)


def actualizar_materia(id_registro, cambios):
    materia = obtener_materia(id_registro)
    if not materia:
        raise ValueError("No existe una materia con ese ID.")
    nombre = str(cambios.get("nombre", materia.nombre)).strip()
    codigo = str(cambios.get("codigo", materia.codigo)).strip().upper()
    try:
        creditos = int(cambios.get("creditos", materia.creditos))
        cupos = int(cambios.get("cupos", materia.cupos))
    except (TypeError, ValueError):
        raise ValueError("Créditos y cupos deben ser números enteros.")
    if not nombre or not codigo:
        raise ValueError("Nombre y código son obligatorios.")
    if any(m.id != materia.id and m.codigo == codigo for m in obtener_materias()):
        raise ValueError("Ese código de materia ya está registrado.")
    if not 1 <= creditos <= 10:
        raise ValueError("Los créditos deben estar entre 1 y 10.")
    ocupados = sum(1 for mat in obtener_matriculas() if mat.materia_id == materia.id)
    minimo = max(0, materia.cupos)
    if not 0 <= cupos <= Materia.CUPOS_MAXIMOS:
        raise ValueError(f"Los cupos deben estar entre 0 y {Materia.CUPOS_MAXIMOS}.")
    # No permitir reducir los cupos disponibles por debajo de cero ni ignorar matrículas activas.
    if cupos + ocupados > Materia.CUPOS_MAXIMOS:
        raise ValueError("Los cupos disponibles más las matrículas superan el máximo permitido.")
    actualizada = Materia(materia.id, nombre, codigo, creditos, cupos)
    reemplazar(gestor_materias, actualizada)
    return actualizada


def eliminar_materia(id_registro):
    if any(m.materia_id == int(id_registro) for m in obtener_matriculas()):
        raise ValueError("No se puede eliminar: la materia tiene matrículas registradas.")
    if not eliminar(gestor_materias, id_registro):
        raise ValueError("No existe una materia con ese ID.")
    return True


# MATRICULAS
def obtener_matriculas():
    return leer_objetos(gestor_matriculas, Matricula)


def obtener_matricula(id_registro):
    return obtener_por_id(obtener_matriculas(), id_registro)


def crear_matricula(datos):
    try:
        estudiante_id = int(datos.get("estudiante_id"))
        materia_id = int(datos.get("materia_id"))
    except (TypeError, ValueError):
        raise ValueError("Debes indicar IDs válidos de estudiante y materia.")
    periodo = str(datos.get("periodo", "")).strip()
    if not periodo:
        raise ValueError("El periodo es obligatorio.")
    estudiante = obtener_estudiante(estudiante_id)
    materia = obtener_materia(materia_id)
    if not estudiante:
        raise ValueError("El estudiante no existe.")
    if not materia:
        raise ValueError("La materia no existe.")
    if not materia.hay_cupo():
        raise ValueError("La materia no tiene cupos disponibles.")
    if any(m.estudiante_id == estudiante_id and m.materia_id == materia_id and m.periodo == periodo
           for m in obtener_matriculas()):
        raise ValueError("El estudiante ya está matriculado en esa materia y periodo.")
    nota = datos.get("nota")
    if nota not in (None, "") and not Materia.es_nota_valida(nota):
        raise ValueError("La nota debe ser un número entre 0 y 20.")
    matricula = Matricula(siguiente_id(gestor_matriculas), estudiante_id, materia_id, periodo, nota)
    materia.ocupar_cupo()
    reemplazar(gestor_materias, materia)
    guardar_nuevo(gestor_matriculas, matricula)
    return matricula


def registrar_nota(id_registro, nota):
    if not Materia.es_nota_valida(nota):
        raise ValueError("La nota debe ser un número entre 0 y 20.")
    matricula = obtener_matricula(id_registro)
    if not matricula:
        raise ValueError("No existe una matrícula con ese ID.")
    matricula.nota = float(nota)
    reemplazar(gestor_matriculas, matricula)
    return matricula


def retirar_matricula(id_registro):
    matricula = obtener_matricula(id_registro)
    if not matricula:
        raise ValueError("No existe una matrícula con ese ID.")
    materia = obtener_materia(matricula.materia_id)
    if materia:
        materia.liberar_cupo()
        reemplazar(gestor_materias, materia)
    eliminar(gestor_matriculas, id_registro)
    return True


def certificado(id_registro):
    matricula = obtener_matricula(id_registro)
    if not matricula:
        raise ValueError("No existe una matrícula con ese ID.")
    estudiante = obtener_estudiante(matricula.estudiante_id)
    materia = obtener_materia(matricula.materia_id)
    return {
        "matricula": matricula,
        "estudiante": estudiante,
        "materia": materia,
        "estado": matricula.estado()
    }


def matriculas_por_estudiante():
    resultado = {}
    for matricula in obtener_matriculas():
        resultado.setdefault(matricula.estudiante_id, []).append(matricula)
    return resultado


def promedio_de_estudiante(id_registro):
    estudiante = obtener_estudiante(id_registro)
    if not estudiante:
        raise ValueError("No existe un estudiante con ese ID.")
    notas = [m.nota for m in obtener_matriculas()
             if m.estudiante_id == estudiante.id and m.nota is not None]
    return round(sum(notas) / len(notas), 2) if notas else None
