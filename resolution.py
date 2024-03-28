from implication_elimination import *
from move_negation_inward import *
from remove_double_not import *
from standardize_variable_scope import *
from prenex_form import *
from skolemize import *
from eliminate_universal_quantifier import *
from to_cnf import *
from convert_to_clause import *

expr_str = 'exists y.all x.(P(x) -> Q(x)) & -(R(x) -> S(y)) & exists y.T(y)'
expr_str = logic.Expression.fromstring(expr_str)

print("Original expression:", expr_str)
expr_str = eliminate_implication(expr_str)
print("After eliminating implication:", expr_str, '\n')

print("Original expression:", expr_str)
expr_str = apply_demorgans(expr_str)
print("After applying De Morgan's laws:", expr_str, '\n')

print('Original expression:', expr_str)
expr_str = remove_double_negation(expr_str)
print('After removing double negation:', expr_str, '\n')

print("Original expression:", expr_str)
expr_str = standardize_variables(expr_str)
print("After standardizing variables:", expr_str, '\n')

print("Original expression:", expr_str)
expr_str = to_prenex_form(expr_str)
print("After converting to prenex form:", expr_str, '\n')

print("Original expression:", expr_str)
expr_str = skolemization(expr_str)
print("After skolemization:", expr_str, '\n')

print("Original expression:", expr_str)
expr_str = eliminate_universal_quantifiers(expr_str)
print("After universal quantifiers elimination:", expr_str, '\n')

print("Original expression:", expr_str)
expr_str = to_cnf(expr_str)
print("After converting to CNF:", expr_str, '\n')

print("Original expression:", expr_str)
clauses = convert_to_clauses(expr_str)
print("Clauses:")
for clause in clauses:
    print("-", clause)
