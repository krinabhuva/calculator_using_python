from flask import Flask, render_template, request, jsonify
import ast
import operator

app = Flask(__name__)

# Safe operators
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.Mod: operator.mod
}

def evaluate(node):
    if isinstance(node, ast.Constant):
        return node.value

    elif isinstance(node, ast.BinOp):
        left = evaluate(node.left)
        right = evaluate(node.right)

        if isinstance(node.op, ast.Div) and right == 0:
            raise ZeroDivisionError("Cannot divide by zero")

        return operators[type(node.op)](left, right)

    elif isinstance(node, ast.UnaryOp):
        return operators[type(node.op)](evaluate(node.operand))

    else:
        raise TypeError("Invalid Expression")

def safe_eval(expression):
    tree = ast.parse(expression, mode='eval')
    return evaluate(tree.body)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expression = data.get('expression', '')

        expression = expression.replace('%', '/100')

        result = safe_eval(expression)

        return jsonify({
            "result": result
        })

    except ZeroDivisionError:
        return jsonify({
            "error": "Cannot divide by zero"
        }), 400

    except Exception:
        return jsonify({
            "error": "Invalid Expression"
        }), 400

if __name__ == '__main__':
    app.run(debug=True)