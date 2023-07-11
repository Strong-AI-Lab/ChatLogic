import traceback
from pyDatalog import pyDatalog
try:
    # Declare the pyDatalog variables
    pyDatalog.create_terms('X, high, heavy, big, tiny, small, clever, smart, quiet, rough, dull, sad, short, imperfect, wealthy, thin, little, kind, nice, bad, poor, huge')
    
    # Define the facts
    +high('Dave')
    +heavy('Dave')
    +big('Dave')
    +tiny('Harry')
    +small('Harry')
    +clever('Alan')
    +smart('Alan')
    +quiet('Alan')
    +rough('Charlie')
    +dull('Charlie')
    +sad('Charlie')
    
    # Define the rules
    clever(X) <= high(X)
    short(X) <= tiny(X) & small(X)
    imperfect(X) <= rough(X) & dull(X)
    wealthy(X) <= clever(X) & smart(X)
    thin(X) <= short(X)
    little(X) <= thin(X)
    sad(X) <= little(X)
    dull(X) <= sad(X)
    smart(X) <= clever(X)
    quiet(X) <= smart(X)
    strong(X) <= quiet(X)
    huge(X) <= strong(X)
    kind(X) <= wealthy(X)
    nice(X) <= kind(X)
    heavy(X) <= nice(X)
    big(X) <= heavy(X)
    bad(X) <= imperfect(X)
    poor(X) <= bad(X)
    small(X) <= poor(X)
    tiny(X) <= small(X)
    
    # Query the knowledge base
    result = huge('Dave')
    if result:
        print(1)
    else:
        print(0)
except Exception as e:
    traceback_info = traceback.format_exc()
    print(traceback_info)