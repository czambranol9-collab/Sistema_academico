from datetime import date


class ModeloBase:
    """Clase base para los modelos que se guardan en JSON."""

    def __init__(self, id_registro):
        self.id = int(id_registro)

    def a_diccionario(self):
        return {"id": self.id}

    @classmethod
    def desde_diccionario(cls, datos):
        # En JSON el identificador se llama "id"; el constructor usa "id_registro".
        datos = dict(datos)
        if "id" in datos:
            datos["id_registro"] = datos.pop("id")
        return cls(**datos)

    def etiqueta(self):
        return f"Registro #{self.id}"

    def __str__(self):
        return self.etiqueta()


class Persona(ModeloBase):
    def __init__(self, id_registro, nombre, apellido, email):
        super().__init__(id_registro)
        self.nombre = str(nombre).strip().title()
        self.apellido = str(apellido).strip().title()
        self.email = str(email).strip().lower()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["apellido"] = self.apellido
        datos["email"] = self.email
        return datos

    def etiqueta(self):
        return f"{self.nombre} {self.apellido} · {self.email}"


class Estudiante(Persona):
    def __init__(self, id_registro, nombre, apellido, email, carnet="", carrera=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.carnet = str(carnet).strip().upper()
        self.carrera = str(carrera).strip().title()

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["carnet"] = self.carnet
        datos["carrera"] = self.carrera
        return datos

    def etiqueta(self):
        return f"{self.nombre} {self.apellido} · {self.carnet} · {self.carrera}"


class Materia(ModeloBase):
    CUPOS_MAXIMOS = 30
    NOTA_APROBACION = 14

    def __init__(self, id_registro, nombre, codigo, creditos, cupos=CUPOS_MAXIMOS):
        super().__init__(id_registro)
        self.nombre = str(nombre).strip().title()
        self.codigo = str(codigo).strip().upper()
        self.creditos = int(creditos)
        self.cupos = int(cupos)

    @staticmethod
    def es_nota_valida(valor):
        try:
            nota = float(valor)
            return 0 <= nota <= 20
        except (TypeError, ValueError):
            return False

    def hay_cupo(self):
        return self.cupos > 0

    def ocupar_cupo(self):
        if not self.hay_cupo():
            return False
        self.cupos -= 1
        return True

    def liberar_cupo(self):
        if self.cupos < self.CUPOS_MAXIMOS:
            self.cupos += 1
            return True
        return False

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos.update({
            "nombre": self.nombre,
            "codigo": self.codigo,
            "creditos": self.creditos,
            "cupos": self.cupos
        })
        return datos

    def etiqueta(self):
        alerta = " · SIN CUPOS" if not self.hay_cupo() else ""
        return f"{self.codigo} · {self.nombre} · {self.creditos} créditos · cupos {self.cupos}{alerta}"


class Matricula(ModeloBase):
    def __init__(self, id_registro, estudiante_id, materia_id, periodo, nota=None, fecha=""):
        super().__init__(id_registro)
        self.estudiante_id = int(estudiante_id)
        self.materia_id = int(materia_id)
        self.periodo = str(periodo).strip()
        self.nota = None if nota in (None, "") else float(nota)
        self.fecha = str(fecha).strip() or date.today().isoformat()

    def esta_aprobada(self):
        return self.nota is not None and self.nota >= Materia.NOTA_APROBACION

    def estado(self):
        if self.nota is None:
            return "Pendiente"
        return "Aprobado" if self.esta_aprobada() else "Reprobado"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos.update({
            "estudiante_id": self.estudiante_id,
            "materia_id": self.materia_id,
            "periodo": self.periodo,
            "nota": self.nota,
            "fecha": self.fecha
        })
        return datos

    def etiqueta(self):
        nota = "Sin nota" if self.nota is None else f"Nota {self.nota:g}"
        return f"Matrícula #{self.id} · estudiante {self.estudiante_id} · materia {self.materia_id} · {self.periodo} · {nota} · {self.estado()}"
