from pyDatalog import pyDatalog
pyDatalog.create_terms('X,huge,poor,dull,sad,big,kind,bad,rough')
+poor('Eric')
+big('Eric')
+sad('Eric')
bad[X] <= poor[X] & big[X]
rough(X) <= bad(X)
result = rough('Eric')
print(result)
