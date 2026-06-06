import random
import sympy as sp
from abc import ABC, abstractmethod

# ----------------------------------------------------------------------
# Clase base
# ----------------------------------------------------------------------
class LimitProblem(ABC):
    def __init__(self, difficulty: str):
        self.difficulty = difficulty
        self.variable = sp.Symbol('x')
        self.expression = None
        self.point = None        # puede ser sp.oo, -sp.oo o un número
        self.direction = None    # '+' o '-' para límites laterales, None para bilateral
        self.answer = None       # número (float) o string especial
        self.latex = ""

    @abstractmethod
    def generate(self):
        """Genera los atributos expression, point, direction y calcula la respuesta."""
        pass

    def to_dict(self):
        """Devuelve un diccionario con toda la información necesaria para el frontend."""
        return {
            "difficulty": self.difficulty,
            "latex": self.latex,
            "answer": self.answer,
            "tolerance_abs": 0.0001 if isinstance(self.answer, float) else None,
            "special_answer": self.answer if isinstance(self.answer, str) else None,
        }

    def _build_latex(self):
        """Construye la cadena LaTeX del límite."""
        expr_latex = sp.latex(self.expression)
        if self.point == sp.oo:
            point_str = r"\infty"
        elif self.point == -sp.oo:
            point_str = r"-\infty"
        else:
            point_str = sp.latex(self.point)

        dir_str = ""
        if self.direction == '+':
            dir_str = r"\to %s^+" % point_str
        elif self.direction == '-':
            dir_str = r"\to %s^-" % point_str
        else:
            dir_str = r"\to %s" % point_str

        self.latex = r"\lim_{x %s} \left(%s\right)" % (dir_str, expr_latex)


# ----------------------------------------------------------------------
# Plantillas FÁCIL
# ----------------------------------------------------------------------
class ConstantLimit(LimitProblem):
    """Límite de una constante: lim_{x->a} c"""
    def generate(self):
        c = random.randint(-10, 10)
        a = random.randint(-5, 5)
        self.expression = c
        self.point = a
        self.direction = None
        self.answer = float(c)  # siempre es la constante
        self._build_latex()


class DirectSubstitutionLimit(LimitProblem):
    """Límite con sustitución directa, p.ej. polinomio simple."""
    def generate(self):
        a = random.randint(-3, 3)
        # generamos un polinomio: x^2 + bx + c
        b = random.randint(-3, 3)
        c = random.randint(-3, 3)
        x = self.variable
        self.expression = x**2 + b*x + c
        self.point = a
        self.direction = None
        self.answer = float(self.expression.subs(x, a))
        self._build_latex()


class KnownTrigLimit(LimitProblem):
    """Límite trigonométrico conocido: sin(x)/x -> 1 cuando x->0"""
    def generate(self):
        # siempre sin(x)/x en 0
        x = self.variable
        self.expression = sp.sin(x) / x
        self.point = 0
        self.direction = None
        self.answer = 1.0
        self._build_latex()


class SimpleInfiniteLimit(LimitProblem):
    """Límite con infinito simple: 1/x^2 en 0+ -> +∞"""
    def generate(self):
        x = self.variable
        self.expression = 1 / x**2
        self.point = 0
        self.direction = '+'   # límite lateral para que sea +∞
        self.answer = "+∞"     # cadena especial
        self._build_latex()


# ----------------------------------------------------------------------
# Plantillas MEDIO
# ----------------------------------------------------------------------
class FactorableZeroLimit(LimitProblem):
    """Indeterminación 0/0 factorizable: (x^2 - a^2)/(x - a) en x->a"""
    def generate(self):
        a = random.randint(-4, 4)
        if a == 0:
            a = 1  # evitar degenerado
        x = self.variable
        self.expression = (x**2 - a**2) / (x - a)
        self.point = a
        self.direction = None
        # el límite simplificado es 2a
        self.answer = float(2 * a)
        self._build_latex()


class InfiniteOverInfiniteLimit(LimitProblem):
    """Indeterminación ∞/∞: cociente de polinomios del mismo grado x->∞"""
    def generate(self):
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        x = self.variable
        # (a*x^2 + ...) / (b*x^2 + ...)  -> a/b
        self.expression = (a*x**2 + random.randint(-3, 3)*x + random.randint(-3,3)) / \
                          (b*x**2 + random.randint(-3, 3)*x + random.randint(-3,3))
        self.point = sp.oo
        self.direction = None
        self.answer = float(a / b)
        self._build_latex()


class ConjugateRootsLimit(LimitProblem):
    """Raíces conjugadas: (sqrt(x) - sqrt(a))/(x - a) en x->a"""
    def generate(self):
        a = random.randint(2, 9)  # a>0 para que sqrt sea real
        x = self.variable
        self.expression = (sp.sqrt(x) - sp.sqrt(a)) / (x - a)
        self.point = a
        self.direction = None
        # límite = 1/(2*sqrt(a))
        self.answer = float(1 / (2 * sp.sqrt(a)))
        self._build_latex()


# ----------------------------------------------------------------------
# Plantillas DIFÍCIL
# ----------------------------------------------------------------------
class OscillatingLimit(LimitProblem):
    """Límite que no existe por oscilación: sin(1/x) en x->0"""
    def generate(self):
        x = self.variable
        self.expression = sp.sin(1/x)
        self.point = 0
        self.direction = None
        # sympy devuelve nan -> DNE
        self.answer = "DNE"
        self._build_latex()


class DifferentLateralsLimit(LimitProblem):
    """Laterales distintos: |x-a|/(x-a) en x->a => DNE"""
    def generate(self):
        a = random.randint(-3, 3)
        x = self.variable
        self.expression = sp.Abs(x - a) / (x - a)
        self.point = a
        self.direction = None   # límite bilateral, no existe
        # Podemos verificarlo con sympy: limit bilateral da nan
        self.answer = "DNE"
        self._build_latex()


class RepeatedLHospitalLimit(LimitProblem):
    """Regla de L'Hôpital repetida: (sin(x) - x)/x^3 en x->0 = -1/6"""
    def generate(self):
        x = self.variable
        self.expression = (sp.sin(x) - x) / x**3
        self.point = 0
        self.direction = None
        self.answer = -1.0 / 6.0
        self._build_latex()


# ----------------------------------------------------------------------
# Factoría para obtener un problema según dificultad
# ----------------------------------------------------------------------
class LimitGenerator:
    """Genera problemas de límites según la dificultad."""

    _easy_classes = [ConstantLimit, DirectSubstitutionLimit, KnownTrigLimit, SimpleInfiniteLimit]
    _medium_classes = [FactorableZeroLimit, InfiniteOverInfiniteLimit, ConjugateRootsLimit]
    _hard_classes = [OscillatingLimit, DifferentLateralsLimit, RepeatedLHospitalLimit]

    @classmethod
    def generate_problem(cls, difficulty: str) -> dict:
        """
        difficulty: 'facil', 'medio', 'dificil'
        Retorna un dict con la información del límite.
        """
        if difficulty == 'facil':
            chosen = random.choice(cls._easy_classes)
        elif difficulty == 'medio':
            chosen = random.choice(cls._medium_classes)
        elif difficulty == 'dificil':
            chosen = random.choice(cls._hard_classes)
        else:
            raise ValueError("Dificultad no reconocida")

        problem = chosen(difficulty)
        problem.generate()
        return problem.to_dict()


