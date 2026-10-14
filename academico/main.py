from views import (
    obtener_estudiantes, crear_estudiante, actualizar_estudiante, eliminar_estudiante,
    buscar_estudiantes, obtener_materias, crear_materia, actualizar_materia,
    eliminar_materia, buscar_materias, materias_sin_cupo, obtener_matriculas,
    crear_matricula, registrar_nota, retirar_matricula, certificado,
    promedio_de_estudiante
)
from shared.herramientas import imprimir_exito, imprimir_error, imprimir_aviso


def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            imprimir_error("Ingresa un número entero válido.")


def listar(titulo, objetos):
    print(f"\n--- {titulo} ---")
    if not objetos:
        print("No hay registros.")
        return
    for objeto in objetos:
        print(f"ID {objeto.id}: {objeto.etiqueta()}")


def menu_estudiantes():
    while True:
        print("\n=== ESTUDIANTES ===")
        print("1. Listar  2. Crear  3. Buscar  4. Actualizar  5. Eliminar  0. Volver")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                listar("Estudiantes", obtener_estudiantes())
            elif opcion == "2":
                datos = {
                    "nombre": input("Nombre: "),
                    "apellido": input("Apellido: "),
                    "email": input("Email: "),
                    "carnet": input("Carnet: "),
                    "carrera": input("Carrera: ")
                }
                est = crear_estudiante(datos)
                imprimir_exito(f"Estudiante creado con ID {est.id}.")
            elif opcion == "3":
                listar("Resultados", buscar_estudiantes(input("Término de búsqueda: ")))
            elif opcion == "4":
                id_est = pedir_entero("ID del estudiante: ")
                datos = {
                    "nombre": input("Nuevo nombre: "),
                    "apellido": input("Nuevo apellido: "),
                    "email": input("Nuevo email: "),
                    "carnet": input("Nuevo carnet: "),
                    "carrera": input("Nueva carrera: ")
                }
                est = actualizar_estudiante(id_est, datos)
                imprimir_exito(f"Estudiante {est.id} actualizado.")
            elif opcion == "5":
                eliminar_estudiante(pedir_entero("ID a eliminar: "))
                imprimir_exito("Estudiante eliminado.")
            elif opcion == "0":
                return
            else:
                imprimir_aviso("Opción no válida.")
        except ValueError as error:
            imprimir_error(str(error))


def menu_materias():
    while True:
        print("\n=== MATERIAS ===")
        print("1. Listar  2. Crear  3. Buscar  4. Actualizar  5. Eliminar")
        print("6. Mostrar materias sin cupo  0. Volver")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                listar("Materias", obtener_materias())
            elif opcion == "2":
                datos = {
                    "nombre": input("Nombre: "),
                    "codigo": input("Código: "),
                    "creditos": input("Créditos (1-10): "),
                    "cupos": input("Cupos disponibles (0-30): ")
                }
                materia = crear_materia(datos)
                imprimir_exito(f"Materia creada con ID {materia.id}.")
            elif opcion == "3":
                listar("Resultados", buscar_materias(input("Término de búsqueda: ")))
            elif opcion == "4":
                id_mat = pedir_entero("ID de la materia: ")
                datos = {
                    "nombre": input("Nuevo nombre: "),
                    "codigo": input("Nuevo código: "),
                    "creditos": input("Nuevos créditos: "),
                    "cupos": input("Nuevos cupos disponibles: ")
                }
                materia = actualizar_materia(id_mat, datos)
                imprimir_exito(f"Materia {materia.id} actualizada.")
            elif opcion == "5":
                eliminar_materia(pedir_entero("ID a eliminar: "))
                imprimir_exito("Materia eliminada.")
            elif opcion == "6":
                listar("Materias sin cupo", materias_sin_cupo())
            elif opcion == "0":
                return
            else:
                imprimir_aviso("Opción no válida.")
        except ValueError as error:
            imprimir_error(str(error))


def menu_matriculas():
    while True:
        print("\n=== MATRÍCULAS ===")
        print("1. Listar  2. Crear  3. Registrar nota  4. Certificado")
        print("5. Retirar matrícula  6. Promedio de estudiante  0. Volver")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                listar("Matrículas", obtener_matriculas())
            elif opcion == "2":
                datos = {
                    "estudiante_id": input("ID del estudiante: "),
                    "materia_id": input("ID de la materia: "),
                    "periodo": input("Periodo (ej. 2026-1): "),
                    "nota": input("Nota (dejar vacío si aún no tiene): ").strip() or None
                }
                matricula = crear_matricula(datos)
                imprimir_exito(f"Matrícula creada con ID {matricula.id}.")
            elif opcion == "3":
                id_mat = pedir_entero("ID de la matrícula: ")
                nota = input("Nota (0-20): ")
                matricula = registrar_nota(id_mat, nota)
                imprimir_exito(f"Nota guardada. Estado: {matricula.estado()}.")
            elif opcion == "4":
                datos = certificado(pedir_entero("ID de la matrícula: "))
                print("\n=== CERTIFICADO ACADÉMICO ===")
                print(f"Estudiante: {datos['estudiante'].nombre} {datos['estudiante'].apellido}")
                print(f"Carnet: {datos['estudiante'].carnet}")
                print(f"Materia: {datos['materia'].nombre} ({datos['materia'].codigo})")
                print(f"Periodo: {datos['matricula'].periodo}")
                print(f"Nota: {datos['matricula'].nota if datos['matricula'].nota is not None else 'Pendiente'}")
                print(f"Estado: {datos['estado']}")
            elif opcion == "5":
                retirar_matricula(pedir_entero("ID de la matrícula a retirar: "))
                imprimir_exito("Matrícula retirada y cupo liberado.")
            elif opcion == "6":
                promedio = promedio_de_estudiante(pedir_entero("ID del estudiante: "))
                print("Promedio:", promedio if promedio is not None else "Todavía no tiene notas registradas.")
            elif opcion == "0":
                return
            else:
                imprimir_aviso("Opción no válida.")
        except ValueError as error:
            imprimir_error(str(error))


def main():
    while True:
        print("\n================================")
        print("     SISTEMA ACADÉMICO")
        print("================================")
        print("1. Estudiantes")
        print("2. Materias")
        print("3. Matrículas")
        print("0. Salir")
        opcion = input("Selecciona una opción: ").strip()
        if opcion == "1":
            menu_estudiantes()
        elif opcion == "2":
            menu_materias()
        elif opcion == "3":
            menu_matriculas()
        elif opcion == "0":
            print("Hasta pronto.")
            break
        else:
            imprimir_aviso("Opción no válida.")


if __name__ == "__main__":
    main()
