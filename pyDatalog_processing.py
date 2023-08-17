import traceback
from pyDatalog import pyDatalog
try:
    # Declare the pyDatalog variables
    pyDatalog.create_terms('X, strong, big, thin, short, smart, rough, bad, huge, poor, quiet, wealthy, dull, nice, sad, kind')
    
    # Define the facts
    +strong('Dave')
    +big('Dave')
    +thin('Charlie')
    +short('Charlie')
    +smart('Anne')
    +rough('Alan')
    +bad('Alan')
    
    # Define the rules
    rough(X) <= ~huge(X)
    quiet(X) <= ~poor(X)
    wealthy(X) <= smart(X)
    nice(X) <= wealthy(X) & ~dull(X)
    sad(X) <= rough(X) & ~huge(X)
    dull(X) <= thin(X) & short(X)
    bad(X) <= dull(X) & ~wealthy(X)
    kind(X) <= quiet(X)
    
    # Query the knowledge base
    result = ~kind('Alan')
    if result:
        print(1)
    else:
        print(0)
except Exception as e:
    traceback_info = traceback.format_exc()
    print(traceback_info)
