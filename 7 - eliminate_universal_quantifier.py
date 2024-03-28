from nltk.sem import logic
from nltk.sem.logic import *


def eliminate_universal_quantifiers(expression):
    if isinstance(expression, AllExpression):
        # For an AllExpression (universal quantification), recursively eliminate it from its term
        return eliminate_universal_quantifiers(expression.term)
    else:
        # For any other type of expression, return it as is
        return expression


expr_str = 'all x.(P(x) & Q(x))'
expr_str = logic.Expression.fromstring(expr_str)

print("Original expression:", expr_str)
print("After universal quantifiers elimination:", eliminate_universal_quantifiers(expr_str))
