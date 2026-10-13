# Sistema académico en Python

Proyecto de consola que administra estudiantes, materias y matrículas usando Python, clases, herencia, polimorfismo y persistencia en archivos JSON.

## Requisitos
- Python 3.9 o superior.
- No necesita instalar librerías externas.

## Estructura
```text
sistema_academico/
├── main.py
├── views.py
├── models.py
├── README.md
├── shared/
│   ├── __init__.py
│   ├── herramientas.py
│   └── json_manager.py
└── data/
    ├── estudiantes.json
    ├── materias.json
    └── matriculas.json
```

## Ejecutar
Abre una terminal dentro de esta carpeta y ejecuta:

```bash
python main.py
```

En Windows también puede funcionar `py main.py`.

Los archivos JSON se crean automáticamente al iniciar el programa. Para comenzar desde cero, cierra el programa y vacía el contenido de los tres JSON dejando `[]`.

## Funciones
- Crear, listar, buscar, actualizar y eliminar estudiantes.
- Crear, listar, buscar, actualizar y eliminar materias.
- Controlar cupos disponibles (matricular reduce un cupo; retirar matrícula lo libera).
- Registrar notas entre 0 y 20.
- Estado calculado automáticamente: Aprobado desde 14, Reprobado por debajo de 14, Pendiente si aún no hay nota.
- Certificado de matrícula y promedio de notas de un estudiante.
- Validaciones para email, carnet, código de materia, créditos, cupos y matrículas duplicadas.

## Nota
El proyecto conserva la separación por capas solicitada en la guía: `models.py` contiene los modelos, `views.py` las operaciones y reglas del sistema, `main.py` la interacción por consola, y `shared/` las utilidades reutilizables.
