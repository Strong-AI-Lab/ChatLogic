from pyDatalog import pyDatalog

# Declare the pyDatalog variables
pyDatalog.create_terms('X, snake, tired, dull, reckless, chase, dog, wolf, visit, mouse, awful, big, nice, quiet, around, cute, furry, small, lovely, strong, angry, slow, smart, kind, obese, fierce, sleepy, adorable, funny, beautiful, lazy, heavy, boring, rough')

# Define the facts
+snake('The snake')
+tired('The snake')
+dull('The snake')
+reckless('The snake')
+chase('The snake', 'the dog')
+wolf('The wolf')
+visit('The wolf', 'the mouse')
+awful('The wolf')
+big('The wolf')
+nice('The dog')
+quiet('The dog')
+around('The dog')
+cute('The mouse')
+furry('The mouse')
+small('The mouse')

# Define the rules
cute(X) <= nice(X)
dull(X) <= chase(X, 'the dog')
lazy(X) <= chase(X, 'the dog')
reckless(X) <= tired(X) & dull(X)
lovely(X) <= cute(X) & furry(X)
strong(X) <= awful(X) & big(X)
angry(X) <= reckless(X)
slow(X) <= angry(X)
big(X) <= slow(X)
furry(X) <= cute(X)
small(X) <= furry(X)
around(X) <= small(X)
smart(X) <= around(X)
kind(X) <= small(X)
obese(X) <= strong(X)
fierce(X) <= obese(X)
dull(X) <= fierce(X)
sleepy(X) <= dull(X)
adorable(X) <= lovely(X)
funny(X) <= adorable(X)
tired(X) <= funny(X)
beautiful(X) <= tired(X)
heavy(X) <= lazy(X)
boring(X) <= heavy(X)
rough(X) <= boring(X)

# Query the knowledge base
result = rough('The snake')

if result:
    print(1)
else:
    print(0)
