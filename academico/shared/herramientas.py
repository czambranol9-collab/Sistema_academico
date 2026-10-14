def imprimir_exito(mensaje):
    print(f"✓ {mensaje}")


def imprimir_error(mensaje):
    print(f"✗ {mensaje}")


def imprimir_aviso(mensaje):
    print(f"⚠ {mensaje}")


def normalizar_texto(valor):
    return str(valor).strip()


def normalizar_email(email):
    return str(email).strip().lower()


def email_valido(email):
    email = normalizar_email(email)
    return "@" in email and "." in email.split("@")[-1] and " " not in email
