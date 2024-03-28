from nltk.sem import logic
from nltk.sem.logic import *


def apply_demorgans(expression):
    # Function to recursively apply De Morgan's laws
    def transform(expr):
        if isinstance(expr, NegatedExpression):
            # Apply De Morgan's laws
            inner_expr = expr.term
            if isinstance(inner_expr, AndExpression):
                # ¬(A ∧ B) ≡ (¬A) ∨ (¬B)
                return OrExpression(NegatedExpression(inner_expr.first),
                                    NegatedExpression(inner_expr.second))
            elif isinstance(inner_expr, OrExpression):
                # ¬(A ∨ B) ≡ (¬A) ∧ (¬B)
                return AndExpression(NegatedExpression(inner_expr.first),
                                     NegatedExpression(inner_expr.second))
            elif isinstance(expr.term, AllExpression):
                # ~Ax p = Ex ~p
                return ExistsExpression(expr.term.variable,
                                        apply_demorgans(
                                            NegatedExpression(expr.term.term)
                                        ))
            elif isinstance(expr.term, ExistsExpression):
                # ~Ex p = Ax ~p
                return AllExpression(expr.term.variable,
                                     apply_demorgans(
                                         NegatedExpression(expr.term.term)
                                     ))
            elif isinstance(expr.term, NegatedExpression):
                # ~~p = p
                return apply_demorgans(expr.term.term)
            else:
                # ~p = ~p
                return expr
        elif isinstance(expr, AndExpression) or isinstance(expr, OrExpression):
            # Recursively transform the sub-expressions
            return expr.__class__(transform(expr.first), transform(expr.second))
        elif isinstance(expr, (AllExpression, ExistsExpression)):
            # (Ax p) = Ax p, (Ex p) = Ex p
            return type(expr)(expr.variable, apply_demorgans(expr.term))
        # Return the expression as is if it's not a conjunction, disjunction, or negation
        return expr

    # Transform and return the expression
    return transform(expression)


