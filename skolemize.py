from nltk.ccg import logic
from nltk.sem.logic import ExistsExpression, AllExpression, Variable, Expression, skolem_function


def skolemization(expression, mapping=None):
    if mapping is None:
        mapping = set()
    if isinstance(expression, ExistsExpression):
        # Replace the existentially quantified variable with a Skolem function/constant
        skolemized_term = expression.term.replace(expression.variable, skolem_function(mapping))
        return skolemization(skolemized_term, mapping)
    elif isinstance(expression, AllExpression):
        # For universally quantified expressions, add the variable to the mapping and continue skolemization
        return AllExpression(
            expression.variable,
            skolemization(expression.term, mapping | {expression.variable})
        )
    else:
        # Base case: return the expression if it's neither existential nor universal quantification
        return expression


