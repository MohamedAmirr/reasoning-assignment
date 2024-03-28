from nltk.ccg import logic
from nltk.sem.logic import *


def eliminate_implication(expression):
    # Function to recursively eliminate implications and biconditionals from an expression
    def transform(expr):
        if isinstance(expr, ImpExpression):
            # Transform A -> B into ¬A ∨ B
            not_a = NegatedExpression(expr.first)
            return OrExpression(not_a, expr.second)
        elif isinstance(expr, IffExpression):
            # Transform A <-> B into (A -> B) & (B -> A), then eliminate implications in those
            a_implies_b = ImpExpression(expr.first, expr.second)
            b_implies_a = ImpExpression(expr.second, expr.first)
            return AndExpression(transform(a_implies_b), transform(b_implies_a))
        elif isinstance(expr, AndExpression) or isinstance(expr, OrExpression):
            # Recursively transform the sub-expressions
            return expr.__class__(transform(expr.first), transform(expr.second))
        elif isinstance(expr, NegatedExpression):
            # Recursively transform the negated expression
            return NegatedExpression(transform(expr.term))
        elif isinstance(expr, (AllExpression, ExistsExpression)):
            # For quantified expressions, apply transformation to the term
            return expr.__class__(expr.variable, transform(expr.term))
        else:
            # Return the expression as is if it's a variable or atomic predicate
            return expr

    # Transform and return the expression
    return transform(expression)


