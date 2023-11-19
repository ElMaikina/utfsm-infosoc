def validar_rut(rut):
    # Eliminar puntos y guiones del Rut, si los hay
    rut = rut.replace(".", "").replace("-", "")

    if not rut[:-1].isdigit():
        return False

    rut_numero = int(rut[:-1])
    rut_verificador = rut[-1]

    # Validar que el Rut tenga 8 o 7 dígitos y el dígito verificador sea un número o la letra 'K'
    if len(rut) not in (8, 9) or not rut_verificador.isdigit() and rut_verificador.upper() != "K":
        return False

    # Calcular el dígito verificador esperado
    suma = 0
    multiplo = 2

    for digito in reversed(str(rut_numero)):
        suma += int(digito) * multiplo
        multiplo = (multiplo % 7) + 1

    resto = suma % 11
    digito_esperado = 11 - resto

    # Si el dígito esperado es 10, entonces debe ser 'K'
    if digito_esperado == 10:
        digito_esperado = 'K'

    # Comprobar si el dígito verificador es válido
    if str(digito_esperado) == rut_verificador or digito_esperado == rut_verificador:
        print("RUT valido!")
        return True
    else:
        print("RUT invalido!")
        return False
