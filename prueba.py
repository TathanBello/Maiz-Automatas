"""
Prototipo de Autómatas para Sistema de Predicción de Sequías
Autor: Jonathan David Lancheros Bello (Ejemplo)
Lenguaje: Python 3

Este script incluye:
- Expresiones regulares para detectar patrones de sequía e inundación.
- Autómata finito determinista (DFA) para detección de sequía.
- Autómata de pila (PDA) para el lenguaje L = { t^n h^n | n >= 1 }.

Alfabeto:
    t : Temperatura alta (por encima del umbral)
    h : Humedad baja (por debajo del umbral)
    r : Evento de lluvia
    a : Alerta generada
    x : Lectura normal (sin riesgo)
"""

import re

# ---------------------- Expresiones Regulares ----------------------
sequía_regex = re.compile(r't{3,}h{2,}')
inundación_regex = re.compile(r'r{2,}x{3,}')

def detectar_patrones(secuencia: str):
    """
    Detecta patrones de sequía e inundación en la secuencia de entrada.
    Devuelve un diccionario con coincidencias encontradas.
    """
    sequía = [m.group() for m in sequía_regex.finditer(secuencia)]
    inundación = [m.group() for m in inundación_regex.finditer(secuencia)]
    return {
        'sequía': sequía,
        'inundación': inundación
    }

# ---------------------- Autómata Finito Determinista ----------------------
class DFA:
    """
    DFA que acepta cualquier cadena que contenga el patrón t{3,}h{2,}.
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self.estado = 'q0'
        self.cont_t = 0
        self.cont_h = 0

    def step(self, simbolo: str):
        if self.estado == 'q0':
            if simbolo == 't':
                self.cont_t = 1
                self.estado = 'q1'
            else:
                self.reset()
        elif self.estado == 'q1':
            if simbolo == 't':
                self.cont_t += 1
                self.estado = 'q2' if self.cont_t == 2 else 'q1'
            else:
                self.reset()
                if simbolo == 't':
                    self.cont_t = 1
                    self.estado = 'q1'
        elif self.estado == 'q2':
            if simbolo == 't':
                self.cont_t += 1
                if self.cont_t >= 3:
                    self.estado = 'q3'
            else:
                self.reset()
                if simbolo == 't':
                    self.cont_t = 1
                    self.estado = 'q1'
        elif self.estado == 'q3':
            if simbolo == 'h':
                self.cont_h = 1
                self.estado = 'q4'
            elif simbolo == 't':
                self.cont_t += 1
                self.estado = 'q3'
            else:
                self.reset()
        elif self.estado == 'q4':
            if simbolo == 'h':
                self.cont_h += 1
                if self.cont_h >= 2:
                    self.estado = 'q_accept'
            elif simbolo == 't':
                self.cont_t = 1
                self.cont_h = 0
                self.estado = 'q1'
            else:
                self.reset()
        elif self.estado == 'q_accept':
            self.estado = 'q_accept'

    def run(self, secuencia: str):
        self.reset()
        for s in secuencia:
            self.step(s)
            if self.estado == 'q_accept':
                return True
        return False


# ---------------------- Autómata de Pila ----------------------
class PDA:
    """
    PDA que acepta el lenguaje L = { t^n h^n | n >= 1 }.
    """
    def acepta(self, secuencia: str):
        pila = []
        visto_t = False
        i = 0
        n = len(secuencia)
        while i < n and secuencia[i] == 't':
            pila.append('T')
            visto_t = True
            i += 1
        while i < n and secuencia[i] == 'h':
            if not pila:
                return False
            pila.pop()
            i += 1
        return visto_t and (not pila) and i == n


# ---------------------- Ejecución de Ejemplo ----------------------
if __name__ == '__main__':
    ejemplos = ['xxttthhxx', 'ttthh', 'ttth', 'tttthhhr', 'rrxxrxx', 'rrxxx', 'rrxxxx', 'tttthhhh']
    print("=== Detección con Expresiones Regulares ===")
    for s in ejemplos:
        res = detectar_patrones(s)
        print(f"Secuencia: {s} -> Sequía: {res['sequía']}, Inundación: {res['inundación']}")

    print("\n=== Detección con Autómata Finito (DFA) ===")
    dfa = DFA()
    for s in ejemplos:
        print(f"Secuencia: {s} -> ¿Patrón de sequía detectado? {'Sí' if dfa.run(s) else 'No'}")

    print("\n=== Aceptación con Autómata de Pila (PDA) ===")
    pda = PDA()
    for s in ['th', 'tthh', 'ttthhh', 'tth', 'thh', 'xth']:
        print(f"Secuencia: {s} -> ¿PDA acepta? {'Sí' if pda.acepta(s) else 'No'}")
