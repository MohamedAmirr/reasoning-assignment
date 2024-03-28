from nltk.ccg import logic
from nltk.sem.logic import AndExpression, OrExpression, ImpExpression, IffExpression, NegatedExpression, \
    AllExpression, ExistsExpression, Variable


def convert_to_clauses(expression):
    clauses = []
    next_var_id = [0]  # Counter for generating unique variable names

    # Generates a unique variable name
    def new_var_name():
        name = f"x{next_var_id[0]}"
        next_var_id[0] += 1
        return name

    # Recursively process the expression to extract clauses
    def process(expr, current_clause=[]):
        if isinstance(expr, AndExpression):
            # If the expression is a conjunction, process both sides separately
            process(expr.first, current_clause)
            process(expr.second, current_clause)
        else:
            # For other types of expressions, consider them as individual clauses
            standardized_clause, _, _ = standardize_variables(expr, {}, {})
            clauses.append(standardized_clause)

    # Standardizes variable names within a clause
    def standardize_variables(expr, local_var_map, global_var_map):
        if isinstance(expr, Variable):
            # For variables, ensure unique naming
            if expr not in global_var_map:
                new_name = Variable(new_var_name())
                global_var_map[expr] = new_name
                local_var_map[expr] = new_name
            return global_var_map[expr], local_var_map, global_var_map

        elif isinstance(expr, (NegatedExpression, AllExpression, ExistsExpression)):
            # For expressions wrapped by a negation or quantifier, process the contained term
            new_term, local_var_map, global_var_map = standardize_variables(expr.term, local_var_map, global_var_map)
            return expr.__class__(new_term), local_var_map, global_var_map

        elif isinstance(expr, (AndExpression, OrExpression, ImpExpression, IffExpression)):
            # For binary operations, process both sides and combine them
            new_first, local_var_map, global_var_map = standardize_variables(expr.first, local_var_map, global_var_map)
            new_second, local_var_map, global_var_map = standardize_variables(expr.second, local_var_map,
                                                                              global_var_map)
            return expr.__class__(new_first, new_second), local_var_map, global_var_map

        return expr, local_var_map, global_var_map

    # Start processing the expression to extract and standardize clauses
    process(expression)
    return clauses


expr_str = '((-P(F1(y)) | P(F1(y))) & (-P(F1(y)) | P(y)) & (-P(y) | P(F1(y))) & (-P(y) | P(y)))'
expr_str = logic.Expression.fromstring(expr_str)

print("Original expression:", expr_str)
print("Clauses:")
clauses = convert_to_clauses(expr_str)
for clause in clauses:
    print("-", clause)
