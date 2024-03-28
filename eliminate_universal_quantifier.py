from nltk.sem import logic
from nltk.sem.logic import *


def eliminate_universal_quantifiers(expression):
    if isinstance(expression, AllExpression):
        # For an AllExpression (universal quantification), recursively eliminate it from its term
        return eliminate_universal_quantifiers(expression.term)
    else:
        # For any other type of expression, return it as is
        return expression


