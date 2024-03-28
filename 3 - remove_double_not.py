from nltk.ccg import logic
from nltk.sem.logic import *


def remove_double_negation(expression):
    # Function to recursively remove double negations
    def transform(expr):
        if isinstance(expr, NegatedExpression):
            # Check for double negation
            if isinstance(expr.term, NegatedExpression):
                # Simplify ¬(¬A) to A
                return transform(expr.term.term)
            else:
                # Recursively transform the negated expression
                return NegatedExpression(transform(expr.term))
        elif isinstance(expr, AndExpression) or isinstance(expr, OrExpression):
            # Recursively transform the sub-expressions
            return expr.__class__(transform(expr.first), transform(expr.second))
        # Return the expression as is if it's not a negation
        return expr

    # Transform and return the expression
    return transform(expression)


expr_str = '-(-A) & -(-(B | -(-C)))'
expr_str = logic.Expression.fromstring(expr_str)

print('Original expression:', expr_str)
print('After removing double negation:', remove_double_negation(expr_str))
