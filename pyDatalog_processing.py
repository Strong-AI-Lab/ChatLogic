from pyDatalog import pyDatalog
# Define facts
pyDatalog.create_terms('X, sad, big, huge, high, little, thin, kind, smart, quiet, poor, dull, short, bad, nice, small, wealthy, rough')
+big('Harry')
+huge('Harry')
+high('Harry')
+little('Bob')
+thin('Bob')
+kind('Anne')
+smart('Anne')
+quiet('Anne')
+poor('Erin')
+dull('Erin')
+sad('Erin')
# Define rulse
kind(X) <= big(X)
short(X) <= little(X) & thin(X)
bad(X) <= poor(X) & dull(X)
nice(X) <= kind(X) & smart(X)
small(X) <= short(X)
smart(X) <= kind(X)
wealthy(X) <= nice(X)
rough(X) <= bad(X)

# Question
result = ~smart('Harry')
print(result)



