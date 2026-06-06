import random
import sympy as sp
from abc import ABC, abstractmethod

# ----------------------------------------------------------------------
# Clase base
# ----------------------------------------------------------------------
class DerivativeProblem(ABC):
    def __init__(self, difficulty: str):
        self.difficulty = difficulty
        self.variable = sp.Symbol('x')
        self.expression = None          # f(x) simbólica
        self.point = None               # valor numérico donde evaluar la derivada
        self.derivative_order = 1       # 1, 2, 3... (para derivadas de orden superior)
        self.answer = None              # número (float) o string especial ("NO DERIVABLE")
        self.latex = ""

    @abstractmethod
    def generate(self):
        """Genera la expresión, el punto y calcula la derivada en el punto."""
        pass

    def to_dict(self):
        """Devuelve la información del problema lista para el frontend."""
        return {
            "difficulty": self.difficulty,
            "latex": self.latex,
            "answer": self.answer,
            "tolerance_abs": 0.0001 if isinstance(self.answer, float) else None,
            "special_answer": self.answer if isinstance(self.answer, str) else None,
            "derivative_order": self.derivative_order,
        }

    def _build_latex(self, problem_type="standard", implicit_eq=None, y_var=None):
        """
        Construye la cadena LaTeX.
        problem_type: "standard" -> muestra f(x) y el punto.
                      "implicit"  -> muestra la ecuación implícita y el punto.
        """
        if problem_type == "implicit":
            eq_latex = sp.latex(implicit_eq)
            self.latex = f"\\text{{Hallar }} \\frac{{dy}}{{dx}} \\text{{ en }}({sp.latex(self.point[0])}, {sp.latex(self.point[1])}) \\text{{ si }} {eq_latex}=0"
        else:
            expr_latex = sp.latex(self.expression)
            order = self.derivative_order
            if order == 1:
                deriv_symbol = "f'"
            elif order == 2:
                deriv_symbol = "f''"
            else:
                deriv_symbol = f"f^{{({order})}}"
            self.latex = f"f(x) = {expr_latex}, \\quad {deriv_symbol}({sp.latex(self.point)}) = ?"


# ----------------------------------------------------------------------
# Plantillas FÁCIL
# ----------------------------------------------------------------------
class ConstantDerivative(DerivativeProblem):
    """Derivada de una constante: f(x)=c, f'(cualquier punto)=0."""
    def generate(self):
        c = random.randint(-10, 10)
        x = self.variable
        self.expression = c
        self.point = random.randint(-5, 5)
        self.answer = 0.0
        self._build_latex()


class PolynomialDerivative(DerivativeProblem):
    """Derivada de un polinomio simple: f(x)=x^2 + bx + c."""
    def generate(self):
        b = random.randint(-3, 3)
        c = random.randint(-3, 3)
        x = self.variable
        self.expression = x**2 + b*x + c
        self.point = random.randint(-3, 3)
        deriv = sp.diff(self.expression, x)
        self.answer = float(deriv.subs(x, self.point))
        self._build_latex()


class BasicSinCosDerivative(DerivativeProblem):
    """Derivada de seno o coseno básico: f(x)=sin(x) o cos(x)."""
    def generate(self):
        x = self.variable
        if random.choice([True, False]):
            self.expression = sp.sin(x)
        else:
            self.expression = sp.cos(x)
        self.point = random.choice([0, sp.pi/6, sp.pi/4, sp.pi/3, sp.pi/2])
        deriv = sp.diff(self.expression, x)
        self.answer = float(deriv.subs(x, self.point).evalf())
        self._build_latex()


class BasicExponentialDerivative(DerivativeProblem):
    """Derivada de la exponencial base e: f(x)=e^x."""
    def generate(self):
        x = self.variable
        self.expression = sp.exp(x)
        self.point = random.choice([0, sp.log(2), sp.log(3)])
        deriv = sp.diff(self.expression, x)
        self.answer = float(deriv.subs(x, self.point).evalf())
        self._build_latex()


# ----------------------------------------------------------------------
# Plantillas MEDIO
# ----------------------------------------------------------------------
class ProductRuleDerivative(DerivativeProblem):
    """Regla del producto: f(x) = (polinomio) * (exponencial o trig)."""
    def generate(self):
        x = self.variable
        poly = x**2 + random.randint(-2, 2)*x + random.randint(-2, 2)
        other = random.choice([sp.exp(x), sp.sin(x), sp.cos(x)])
        self.expression = poly * other
        self.point = random.choice([0, 1, -1])
        deriv = sp.diff(self.expression, x)
        self.answer = float(deriv.subs(x, self.point).evalf())
        self._build_latex()


class QuotientRuleDerivative(DerivativeProblem):
    """Regla del cociente: f(x) = (polinomio1)/(polinomio2) con denominador no nulo en el punto."""
    def generate(self):
        x = self.variable
        while True:
            num = x**2 + random.randint(-3, 3)*x + random.randint(-3, 3)
            den = x**2 + random.randint(-2, 2)*x + random.randint(1, 3)  # siempre positivo
            punto = random.randint(-2, 2)
            if den.subs(x, punto) != 0:
                break
        self.expression = num / den
        self.point = punto
        deriv = sp.diff(self.expression, x)
        self.answer = float(deriv.subs(x, self.point).evalf())
        self._build_latex()


class SimpleChainRuleDerivative(DerivativeProblem):
    """Regla de la cadena simple: f(x) = sin(kx) o e^{kx}."""
    def generate(self):
        x = self.variable
        k = random.randint(2, 5)
        inner = k * x
        outer = random.choice([sp.sin, sp.cos, sp.exp])
        self.expression = outer(inner)
        self.point = random.choice([0, sp.pi/6, sp.pi/4, 1])
        deriv = sp.diff(self.expression, x)
        self.answer = float(deriv.subs(x, self.point).evalf())
        self._build_latex()


class FractionalExponentDerivative(DerivativeProblem):
    """Potencia con exponente fraccionario: f(x) = x^(p/q) o sqrt(x)."""
    def generate(self):
        x = self.variable
        # sqrt(x), cbrt(x), x^(3/2), etc.
        choices = [sp.sqrt(x), x**sp.Rational(1,3), x**sp.Rational(2,3), x**sp.Rational(3,2)]
        self.expression = random.choice(choices)
        # elegir punto donde la derivada exista (x>0 para potencias no enteras)
        self.point = random.choice([1, 4, 8, 9])
        deriv = sp.diff(self.expression, x)
        self.answer = float(deriv.subs(x, self.point).evalf())
        self._build_latex()


class NaturalLogDerivative(DerivativeProblem):
    """Derivada del logaritmo natural: f(x) = ln(x) o ln(kx)."""
    def generate(self):
        x = self.variable
        k = random.randint(1, 5)
        self.expression = sp.log(k * x)
        self.point = random.choice([1, 2, sp.E])
        deriv = sp.diff(self.expression, x)
        self.answer = float(deriv.subs(x, self.point).evalf())
        self._build_latex()


class InverseTrigDerivative(DerivativeProblem):
    """Derivada de función trigonométrica inversa: arcsin(x) o arctan(x)."""
    def generate(self):
        x = self.variable
        func = random.choice([sp.asin, sp.atan])
        self.expression = func(x)
        # puntos donde la derivada sea finita y sencilla
        self.point = random.choice([0, sp.Rational(1,2), sp.Rational(1, sp.sqrt(2)), sp.Rational(1,3)])
        deriv = sp.diff(self.expression, x)
        self.answer = float(deriv.subs(x, self.point).evalf())
        self._build_latex()


# ----------------------------------------------------------------------
# Plantillas DIFÍCIL
# ----------------------------------------------------------------------
class NestedChainRuleDerivative(DerivativeProblem):
    """Regla de la cadena anidada: f(x) = e^{sin(x^2)} o sqrt(cos(x))."""
    def generate(self):
        x = self.variable
        # Posibles composiciones profundas
        options = [
            sp.exp(sp.sin(x**2)),
            sp.sqrt(sp.cos(x)),     # en punto donde cos>0
            sp.sin(sp.exp(x)),
            sp.ln(1 + x**2)
        ]
        self.expression = random.choice(options)
        # elegir punto adecuado para evitar dominios problemáticos
        if self.expression == sp.sqrt(sp.cos(x)):
            self.point = 0  # cos(0)=1
        elif self.expression == sp.ln(1 + x**2):
            self.point = random.choice([0, 1])
        else:
            self.point = random.choice([0, sp.pi/4, 1])
        deriv = sp.diff(self.expression, x)
        self.answer = float(deriv.subs(x, self.point).evalf())
        self._build_latex()


class HigherOrderDerivative(DerivativeProblem):
    """Derivada de orden superior: f''(c) o f'''(c)."""
    def generate(self):
        x = self.variable
        # polinomio de grado suficiente
        grado = random.randint(3, 5)
        coeffs = [random.randint(-3, 3) for _ in range(grado+1)]
        self.expression = sum(c * x**i for i, c in enumerate(coeffs))
        self.derivative_order = random.randint(2, 3)  # segunda o tercera derivada
        self.point = random.randint(-2, 2)
        deriv = self.expression
        for _ in range(self.derivative_order):
            deriv = sp.diff(deriv, x)
        self.answer = float(deriv.subs(x, self.point))
        self._build_latex()


class ImplicitDerivative(DerivativeProblem):
    """Derivación implícita: dada una ecuación F(x,y)=0 y un punto, hallar dy/dx."""
    def generate(self):
        x, y = sp.symbols('x y')
        # Usamos un círculo: x^2 + y^2 = r^2 -> F = x^2 + y^2 - r^2 = 0
        r = random.randint(3, 6)
        F = x**2 + y**2 - r**2
        # Elegimos un punto del círculo con coordenadas enteras (terna pitagórica básica)
        # Usamos (3,4) con r=5, (4,3), (0,5), (5,0), etc.
        # Para simplificar, escogemos ángulo notable: x0 = r * cos(theta), y0 = r * sin(theta)
        theta = random.choice([0, sp.pi/6, sp.pi/4, sp.pi/3, sp.pi/2])
        x0 = r * sp.cos(theta)
        y0 = r * sp.sin(theta)
        # Calculamos dy/dx = -Fx/Fy
        Fx = sp.diff(F, x)
        Fy = sp.diff(F, y)
        deriv_impl = -Fx/Fy
        dy_dx = deriv_impl.subs({x: x0, y: y0}).evalf()
        self.answer = float(dy_dx)
        self.expression = None  # no aplica la representación estándar
        self.point = (x0, y0)   # tupla (x0,y0)
        # Construir LaTeX especial
        eq_latex = sp.latex(F)
        self._build_latex(problem_type="implicit", implicit_eq=F, y_var=y)


# ----------------------------------------------------------------------
# Factoría
# ----------------------------------------------------------------------
class DerivativeGenerator:
    _easy_classes = [
        ConstantDerivative,
        PolynomialDerivative,
        BasicSinCosDerivative,
        BasicExponentialDerivative,
    ]
    _medium_classes = [
        ProductRuleDerivative,
        QuotientRuleDerivative,
        SimpleChainRuleDerivative,
        FractionalExponentDerivative,
        NaturalLogDerivative,
        InverseTrigDerivative,
    ]
    _hard_classes = [
        NestedChainRuleDerivative,
        HigherOrderDerivative,
        ImplicitDerivative,
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


