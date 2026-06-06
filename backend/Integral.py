import random
import sympy as sp
from abc import ABC, abstractmethod

# ----------------------------------------------------------------------
# Clase base
# ----------------------------------------------------------------------
class IntegralProblem(ABC):
    def __init__(self, difficulty: str):
        self.difficulty = difficulty
        self.variable = sp.Symbol('x')
        self.expression = None       # f(x) simbólica
        self.lower_limit = None      # a
        self.upper_limit = None      # b
        self.answer = None           # float (valor del área) o string "DIVERGE"
        self.latex = ""

    @abstractmethod
    def generate(self):
        """Genera la expresión, los límites y calcula la integral definida."""
        pass

    def to_dict(self):
        return {
            "difficulty": self.difficulty,
            "latex": self.latex,
            "answer": self.answer,
            "tolerance_abs": 0.0001 if isinstance(self.answer, float) else None,
            "special_answer": self.answer if isinstance(self.answer, str) else None,
            "lower_limit": float(self.lower_limit) if self.lower_limit is not None else None,
            "upper_limit": float(self.upper_limit) if self.upper_limit is not None else None,
        }

    def _build_latex(self):
        expr_latex = sp.latex(self.expression)
        a_latex = sp.latex(self.lower_limit)
        b_latex = sp.latex(self.upper_limit)
        self.latex = f"\\int_{{{a_latex}}}^{{{b_latex}}} {expr_latex} \\, dx"


# ----------------------------------------------------------------------
# Plantillas FÁCIL
# ----------------------------------------------------------------------
class ConstantIntegral(IntegralProblem):
    """∫_a^b c dx = c*(b-a)."""
    def generate(self):
        c = random.randint(-5, 5)
        a = random.randint(-3, 3)
        b = random.randint(a+1, a+4)
        self.expression = c
        self.lower_limit = a
        self.upper_limit = b
        self.answer = float(c * (b - a))
        self._build_latex()


class LinearIntegral(IntegralProblem):
    """∫_a^b (mx + n) dx."""
    def generate(self):
        m = random.randint(-4, 4)
        n = random.randint(-4, 4)
        a = random.randint(-2, 2)
        b = random.randint(a+1, a+4)
        x = self.variable
        self.expression = m*x + n
        self.lower_limit = a
        self.upper_limit = b
        # área exacta usando sympy (aunque podríamos calcular manualmente)
        area = sp.integrate(self.expression, (x, a, b))
        self.answer = float(area)
        self._build_latex()


class SimplePolynomialIntegral(IntegralProblem):
    """∫_a^b (x^2 + p x + q) dx."""
    def generate(self):
        p = random.randint(-3, 3)
        q = random.randint(-3, 3)
        a = random.randint(-2, 2)
        b = random.randint(a+1, a+4)
        x = self.variable
        self.expression = x**2 + p*x + q
        self.lower_limit = a
        self.upper_limit = b
        area = sp.integrate(self.expression, (x, a, b))
        self.answer = float(area)
        self._build_latex()


class SinCosPeriodIntegral(IntegralProblem):
    """∫_0^π sin(x) dx = 2, o ∫_0^{π/2} cos(x) dx = 1."""
    def generate(self):
        x = self.variable
        # Elegir entre seno o coseno con límites que den un resultado entero
        if random.choice([True, False]):
            self.expression = sp.sin(x)
            self.lower_limit = 0
            self.upper_limit = sp.pi
            self.answer = 2.0
        else:
            self.expression = sp.cos(x)
            self.lower_limit = 0
            self.upper_limit = sp.pi/2
            self.answer = 1.0
        self._build_latex()


class BasicExponentialIntegral(IntegralProblem):
    """∫_0^c e^{kx} dx = (e^{kc} - 1)/k."""
    def generate(self):
        x = self.variable
        k = random.randint(1, 3)
        c = random.choice([1, 2, sp.log(2)])  # c=ln(2) da resultado exacto 1/k
        self.expression = sp.exp(k * x)
        self.lower_limit = 0
        self.upper_limit = c
        area = sp.integrate(self.expression, (x, 0, c))
        self.answer = float(area.evalf())
        self._build_latex()


# ----------------------------------------------------------------------
# Plantillas MEDIO
# ----------------------------------------------------------------------
class PolynomialDegree34(IntegralProblem):
    """∫_a^b (ax^3 + bx^2 + cx + d) dx."""
    def generate(self):
        coeffs = [random.randint(-3, 3) for _ in range(4)]  # grado 3..0
        # asegurar que no sea nulo el término principal
        if coeffs[0] == 0:
            coeffs[0] = random.choice([1, -1])
        x = self.variable
        self.expression = coeffs[0]*x**3 + coeffs[1]*x**2 + coeffs[2]*x + coeffs[3]
        a = random.randint(-2, 1)
        b = random.randint(a+1, a+3)
        self.lower_limit = a
        self.upper_limit = b
        area = sp.integrate(self.expression, (x, a, b))
        self.answer = float(area)
        self._build_latex()


class TrigWithFrequency(IntegralProblem):
    """∫_a^b sin(kx) o cos(kx) con frecuencia k>1 y límites ajustados para un área sencilla."""
    def generate(self):
        x = self.variable
        k = random.randint(2, 4)
        # Usamos un cuarto de periodo para obtener área = 1/k
        # ∫_0^{π/(2k)} cos(kx) dx = 1/k
        if random.choice([True, False]):
            self.expression = sp.cos(k*x)
            self.lower_limit = 0
            self.upper_limit = sp.pi/(2*k)
        else:
            self.expression = sp.sin(k*x)
            # ∫_0^{π/k} sin(kx) dx = 2/k  (área de una media onda completa)
            self.lower_limit = 0
            self.upper_limit = sp.pi/k
        area = sp.integrate(self.expression, (x, self.lower_limit, self.upper_limit))
        self.answer = float(area.evalf())
        self._build_latex()


class SimpleIntegrationByParts(IntegralProblem):
    """∫_0^1 x e^x dx = 1 (partes típica)."""
    def generate(self):
        x = self.variable
        self.expression = x * sp.exp(x)
        self.lower_limit = 0
        self.upper_limit = 1
        area = sp.integrate(self.expression, (x, 0, 1))
        self.answer = float(area)  # 1.0
        self._build_latex()


# ----------------------------------------------------------------------
# Plantillas DIFÍCIL
# ----------------------------------------------------------------------
class TrigEvenPower(IntegralProblem):
    """∫_0^π sin^2(x) dx = π/2 o ∫_0^{π/2} cos^2(x) dx = π/4."""
    def generate(self):
        x = self.variable
        if random.choice([True, False]):
            self.expression = sp.sin(x)**2
            self.lower_limit = 0
            self.upper_limit = sp.pi
            self.answer = float(sp.pi/2)
        else:
            self.expression = sp.cos(x)**2
            self.lower_limit = 0
            self.upper_limit = sp.pi/2
            self.answer = float(sp.pi/4)
        self._build_latex()


class TrigSubstitution(IntegralProblem):
    """∫_0^{1/2} 1/√(1-x^2) dx = π/6 o ∫_0^1 1/(1+x^2) dx = π/4."""
    def generate(self):
        x = self.variable
        # Elegir entre dos integrales clásicas que requieren sustitución trigonométrica
        if random.choice([True, False]):
            self.expression = 1 / sp.sqrt(1 - x**2)
            self.lower_limit = 0
            self.upper_limit = sp.Rational(1, 2)  # 1/2
            self.answer = float(sp.pi/6)
        else:
            self.expression = 1 / (1 + x**2)
            self.lower_limit = 0
            self.upper_limit = 1
            self.answer = float(sp.pi/4)
        self._build_latex()


# ----------------------------------------------------------------------
# Factoría
# ----------------------------------------------------------------------
class IntegralGenerator:
    _easy_classes = [
        ConstantIntegral,
        LinearIntegral,
        SimplePolynomialIntegral,
        SinCosPeriodIntegral,
        BasicExponentialIntegral,
    ]
    _medium_classes = [
        PolynomialDegree34,
        TrigWithFrequency,
        SimpleIntegrationByParts,
    ]
    _hard_classes = [
        TrigEvenPower,
        TrigSubstitution,
    ]

    @classmethod
    def generate_problem(cls, difficulty: str) -> dict:
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


