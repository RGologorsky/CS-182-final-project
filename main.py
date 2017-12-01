from printing import *
from branch_and_bound import *

assignment1 = (["cs50"], ["cs51", "am107"], ["cs121"], ["cs124"])
assignment2 = ([], ["cs51", "cs124"], ["cs50"])

print "\n"

print_assignment(assignment1)
print_assignment(assignment2)

c1 = cost(assignment1)
c2 = cost(assignment2)

print "\n COSTS"
print("C1 cost: %d" % c1)
print("C2 cost: %d" % c2)
