from flask import Flask, request, render_template_string
import cmath

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rozwiązywacz Równań Sześciennych</title>
</head>
<body>
    <h1>Rozwiązywacz Równań Sześciennych</h1>
    <form method="post">
        <label for="a">Współczynnik a:</label>
        <input type="text" id="a" name="a" required><br><br>
        <label for="b">Współczynnik b:</label>
        <input type="text" id="b" name="b" required><br><br>
        <label for="c">Współczynnik c:</label>
        <input type="text" id="c" name="c" required><br><br>
        <label for="d">Współczynnik d:</label>
        <input type="text" id="d" name="d" required><br><br>
        <button type="submit">Rozwiąż</button>
    </form>
    {% if result %}
        <h2>Wynik:</h2>
        <ul>
        {% for root in result %}
            <li>{{ root }}</li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""

def calculate_roots(a, b, c, d):
    p = (3*a*c - b**2) / (3*a**2)
    q = (2*b**3 - 9*a*b*c + 27*a**2*d) / (27*a**3)
    delta = (q/2)**2 + (p/3)**3

    roots = []
    if delta > 0:
        u = cmath.exp(cmath.log(-q/2 + cmath.sqrt(delta)) / 3)
        v = cmath.exp(cmath.log(-q/2 - cmath.sqrt(delta)) / 3)
        x1 = u + v - b/(3*a)
        roots.append(round(x1.real, 6))
    elif delta == 0:
        u = (-q/2)**(1/3)
        x1 = 2*u - b/(3*a)
        x2 = -u - b/(3*a)
        roots.append(round(x1.real, 6))
        roots.append(round(x2.real, 6))
    else:
        phi = cmath.acos(-q/2 / (-p/3)**(3/2))
        u = 2 * (-p/3)**0.5
        x1 = u * cmath.cos(phi/3) - b/(3*a)
        x2 = u * cmath.cos((phi + 2*cmath.pi)/3) - b/(3*a)
        x3 = u * cmath.cos((phi + 4*cmath.pi)/3) - b/(3*a)
        roots.append(round(x1.real, 6))
        roots.append(round(x2.real, 6))
        roots.append(round(x3.real, 6))

    return [str(root) for root in roots]

@app.route('/', methods=['GET', 'POST'])
def solve_cubic():
    result = None
    if request.method == 'POST':
        try:
            a = float(request.form['a'])
            b = float(request.form['b'])
            c = float(request.form['c'])
            d = float(request.form['d'])
            result = calculate_roots(a, b, c, d)
        except ValueError:
            result = ['Nieprawidłowe dane. Proszę wprowadzić poprawne wartości liczbowe.']
    return render_template_string(html_template, result=result)

if __name__ == '__main__':
    app.run(debug=True)
