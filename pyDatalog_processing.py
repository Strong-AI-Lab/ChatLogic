import traceback
from pyDatalog import pyDatalog
try:
    # Declare the pyDatalog variables
    pyDatalog.create_terms('X, strong, huge, big, short, little, thin, dull, rough, bad, quiet, wealthy, kind, small, nice, poor, smart, sad')
    # Define the facts
    +strong('Dave')
    +huge('Dave')
    +big('Dave')
    +short('Gary')
    +little('Gary')
    +quiet('Bob')
    +wealthy('Bob')
    +smart('Bob')
    +dull('Harry')
    +rough('Harry')
    +sad('Harry')
    # Define the rules
    quiet(X) <= strong(X)
    thin(X) <= short(X) & little(X)
    bad(X) <= dull(X) & rough(X)
    kind(X) <= quiet(X) & wealthy(X)
    small(X) <= thin(X)
    wealthy(X) <= quiet(X)
    nice(X) <= kind(X)
    poor(X) <= bad(X)
    # Query the knowledge base
    result = small('Gary')
    if result:
        print(0)
    else:
        print(1)
except Exception as e:
    traceback_info = traceback.format_exc()
    print(traceback_info)