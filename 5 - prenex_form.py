from nltk.ccg import logic
from nltk.sem.logic import NegatedExpression, ExistsExpression, AllExpression, AndExpression, OrExpression


def to_prenex_form(expression):
    # Function to recursively move quantifiers to the front
    def move_quantifiers(expr):
        if isinstance(expr, (AndExpression, OrExpression)):
            # If the current expression is an AND or OR, solve it.
            first, q1, v1 = move_quantifiers(expr.first)
            second, q2, v2 = move_quantifiers(expr.second)
            return type(expr)(first, second), q1 + q2, v1 + v2
        elif isinstance(expr, AllExpression):
            # If the current expression is a universal quantifier, move it to the front
            term, qs, vs = move_quantifiers(expr.term)
            return term, qs + [AllExpression], vs + [expr.variable]
        elif isinstance(expr, ExistsExpression):
            # If the current expression is an existential quantifier, move it to the front
            term, qs, vs = move_quantifiers(expr.term)
            return term, qs + [ExistsExpression], vs + [expr.variable]
        elif isinstance(expr, NegatedExpression):
            # If the current expression is a negation, solve it.
            term, qs, vs = move_quantifiers(expr.term)
            return NegatedExpression(term), qs, vs
        else:
            # For atomic expressions, return as is
            return expr, [], []

    expression, quantifiers, variables = move_quantifiers(expression)

    for quantifier, variable in sorted(zip(quantifiers, variables), key=lambda x: 1 if x[0] == AllExpression else 0):
        expression = quantifier(variable, expression)

    return expression


expr_str = 'some x all y (P(x) | P(y) -> (P(x) & P(y)))'
expr_str = logic.Expression.fromstring(expr_str)

print("Original expression:", expr_str)
print("After converting to prenex form:", to_prenex_form(expr_str))
