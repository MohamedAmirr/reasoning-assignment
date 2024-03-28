from nltk.ccg import logic
from nltk.sem.logic import AndExpression, OrExpression, Expression


def to_cnf(expression):
    if isinstance(expression, AndExpression):
        # For an AndExpression, recursively apply to_cnf to both sub-expressions
        return AndExpression(
            to_cnf(expression.first),
            to_cnf(expression.second)
        )
    elif isinstance(expression, OrExpression):
        if isinstance(expression.first, AndExpression):
            # Distributive law: ((p & q) | r) = (p | r) & (q | r)
            return AndExpression(
                to_cnf(
                    OrExpression(expression.first.first, expression.second)
                ),
                to_cnf(
                    OrExpression(expression.first.second, expression.second)
                )
            )
        elif isinstance(expression.second, AndExpression):
            # Distributive law: (r | (p & q)) = (r | p) & (r | q)
            return AndExpression(
                to_cnf(
                    OrExpression(expression.first, expression.second.first)
                ),
                to_cnf(
                    OrExpression(expression.first, expression.second.second)
                )
            )
        else:
            # For a simple OrExpression, recursively apply to_cnf to both sub-expressions
            return OrExpression(
                to_cnf(expression.first),
                to_cnf(expression.second)
            )
    else:
        # For atomic expressions or expressions that don't require conversion, return them as is
        return expression


