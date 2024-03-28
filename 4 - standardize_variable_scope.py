from nltk.ccg import logic
from nltk.sem.logic import AllExpression, ExistsExpression, AndExpression, OrExpression, NegatedExpression, \
    unique_variable


def standardize_variables(expression, expression_variables=None):
    if expression_variables is None:
        expression_variables = set()

    if isinstance(expression, AllExpression):
        # For AllExpression, if the variable is already in mapping, perform alpha conversion to a unique variable
        if expression.variable in expression_variables:
            expression = expression.alpha_convert(unique_variable(ignore=expression_variables))
        else:
            expression_variables.add(expression.variable)
        return AllExpression(
            expression.variable,
            standardize_variables(expression.term, expression_variables)
        )
    elif isinstance(expression, ExistsExpression):
        # For ExistsExpression, similar to AllExpression, check and perform alpha conversion if necessary
        if expression.variable in expression_variables:
            expression = expression.alpha_convert(unique_variable(ignore=expression_variables))
        else:
            expression_variables.add(expression.variable)
        return ExistsExpression(
            expression.variable,
            standardize_variables(expression.term, expression_variables)
        )
    elif isinstance(expression, (AndExpression, OrExpression)):
        # For AndExpression and OrExpression, recursively standardize the variables in both sub-expressions
        return type(expression)(
            standardize_variables(expression.first, expression_variables),
            standardize_variables(expression.second, expression_variables)
        )
    elif isinstance(expression, NegatedExpression):
        # For NegatedExpression, recursively standardize the variable in the negated sub-expression
        return NegatedExpression(
            standardize_variables(expression.term, expression_variables)
        )
    else:
        # Base case: if the expression is not a quantifier, conjunction, disjunction, or negation, return it as is
        return expression


expr_str = 'some x.P(x) & all x.Q(x)'
expr_str = logic.Expression.fromstring(expr_str)

print("Original expression:", expr_str)
print("After standardizing variables:", standardize_variables(expr_str))
