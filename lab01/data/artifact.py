#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora Científica Básica
Este programa implementa una calculadora con operaciones matemáticas básicas
y algunas funciones científicas avanzadas.
"""

import math

# Constantes matemáticas importantes
PI = math.pi
EULER = math.e

def calcular_suma(numero_uno, numero_dos):
    """
    Calcula la suma de dos números.

    Args:
        numero_uno: El primer número a sumar
        numero_dos: El segundo número a sumar

    Returns:
        La suma de los dos números
    """
    resultado = numero_uno + numero_dos
    return resultado

def calcular_resta(numero_uno, numero_dos):
    """Calcula la resta de dos números."""
    return numero_uno - numero_dos

def calcular_multiplicacion(numero_uno, numero_dos):
    """Calcula el producto de dos números."""
    return numero_uno * numero_dos

def calcular_division(numerador, denominador):
    """
    Calcula la división de dos números.
    Maneja el caso especial de división por cero.
    """
    if denominador == 0:
        raise ValueError("No se puede dividir por cero")
    return numerador / denominador

def calcular_potencia(base, exponente):
    """Calcula la potencia de un número."""
    return base ** exponente

def calcular_raiz_cuadrada(numero):
    """
    Calcula la raíz cuadrada de un número.
    Solo acepta números no negativos.
    """
    if numero < 0:
        raise ValueError("No se puede calcular la raíz cuadrada de un número negativo")
    return math.sqrt(numero)

def verificar_es_par(numero):
    """
    Verifica si un número es par.

    Args:
        numero: El número entero a verificar

    Returns:
        True si el número es par, False en caso contrario
    """
    return numero % 2 == 0

def verificar_es_primo(numero):
    """
    Verifica si un número es primo.
    Un número primo solo es divisible por 1 y por sí mismo.
    """
    if numero < 2:
        return False

    # Verificar divisibilidad desde 2 hasta la raíz cuadrada del número
    for divisor in range(2, int(math.sqrt(numero)) + 1):
        if numero % divisor == 0:
            return False

    return True

def calcular_factorial(numero):
    """
    Calcula el factorial de un número.
    El factorial de n es el producto de todos los enteros positivos hasta n.
    """
    if numero < 0:
        raise ValueError("No se puede calcular el factorial de un número negativo")

    if numero == 0 or numero == 1:
        return 1

    resultado = 1
    for i in range(2, numero + 1):
        resultado *= i

    return resultado

def calcular_area_circulo(radio):
    """Calcula el área de un círculo dado su radio."""
    if radio < 0:
        raise ValueError("El radio no puede ser negativo")
    return PI * radio ** 2

def calcular_perimetro_circulo(radio):
    """Calcula el perímetro (circunferencia) de un círculo dado su radio."""
    if radio < 0:
        raise ValueError("El radio no puede ser negativo")
    return 2 * PI * radio

def menu_principal():
    """
    Muestra el menú principal de la calculadora y procesa las opciones del usuario.
    """
    print("=" * 50)
    print("CALCULADORA CIENTÍFICA")
    print("=" * 50)
    print("1. Suma")
    print("2. Resta")
    print("3. Multiplicación")
    print("4. División")
    print("5. Potencia")
    print("6. Raíz cuadrada")
    print("7. Verificar si es número par")
    print("8. Verificar si es número primo")
    print("9. Calcular factorial")
    print("10. Área de círculo")
    print("11. Salir")
    print("=" * 50)

def ejecutar_calculadora():
    """
    Función principal que ejecuta el bucle de la calculadora.
    """
    continuar = True

    while continuar:
        menu_principal()
        opcion = input("\nSeleccione una opción (1-11): ")

        try:
            if opcion == "1":
                num1 = float(input("Ingrese el primer número: "))
                num2 = float(input("Ingrese el segundo número: "))
                resultado = calcular_suma(num1, num2)
                print(f"Resultado: {num1} + {num2} = {resultado}")

            elif opcion == "2":
                num1 = float(input("Ingrese el primer número: "))
                num2 = float(input("Ingrese el segundo número: "))
                resultado = calcular_resta(num1, num2)
                print(f"Resultado: {num1} - {num2} = {resultado}")

            elif opcion == "3":
                num1 = float(input("Ingrese el primer número: "))
                num2 = float(input("Ingrese el segundo número: "))
                resultado = calcular_multiplicacion(num1, num2)
                print(f"Resultado: {num1} × {num2} = {resultado}")

            elif opcion == "4":
                num1 = float(input("Ingrese el numerador: "))
                num2 = float(input("Ingrese el denominador: "))
                resultado = calcular_division(num1, num2)
                print(f"Resultado: {num1} ÷ {num2} = {resultado}")

            elif opcion == "5":
                base = float(input("Ingrese la base: "))
                exp = float(input("Ingrese el exponente: "))
                resultado = calcular_potencia(base, exp)
                print(f"Resultado: {base}^{exp} = {resultado}")

            elif opcion == "6":
                num = float(input("Ingrese el número: "))
                resultado = calcular_raiz_cuadrada(num)
                print(f"Resultado: √{num} = {resultado}")

            elif opcion == "7":
                num = int(input("Ingrese un número entero: "))
                es_par = verificar_es_par(num)
                if es_par:
                    print(f"{num} es un número par")
                else:
                    print(f"{num} es un número impar")

            elif opcion == "8":
                num = int(input("Ingrese un número entero: "))
                es_primo = verificar_es_primo(num)
                if es_primo:
                    print(f"{num} es un número primo")
                else:
                    print(f"{num} no es un número primo")

            elif opcion == "9":
                num = int(input("Ingrese un número entero: "))
                resultado = calcular_factorial(num)
                print(f"Resultado: {num}! = {resultado}")

            elif opcion == "10":
                radio = float(input("Ingrese el radio del círculo: "))
                area = calcular_area_circulo(radio)
                perimetro = calcular_perimetro_circulo(radio)
                print(f"Área: {area:.2f}")
                print(f"Perímetro: {perimetro:.2f}")

            elif opcion == "11":
                print("Gracias por usar la calculadora. ¡Hasta luego!")
                continuar = False

            else:
                print("Opción no válida. Por favor, seleccione una opción entre 1 y 11.")

        except ValueError as error:
            print(f"Error: {error}")
        except Exception as error:
            print(f"Ha ocurrido un error inesperado: {error}")

        print()  # Línea en blanco para separar

# Punto de entrada del programa
if __name__ == "__main__":
    ejecutar_calculadora()
