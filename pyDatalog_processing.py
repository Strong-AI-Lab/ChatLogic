import traceback
from pyDatalog import pyDatalog
try:
    # Declare the pyDatalog variables
    pyDatalog.create_terms('X, Alan, strong, high, Fiona, little, small, Bob, wealthy, Harry, sad, rough, smart, bad, nice, dull, quiet, poor, kind, big')

    # Define the facts
    +strong('Alan')
    +high('Alan')
    +little('Fiona')
    +small('Fiona')
    +wealthy('Bob')
    +sad('Harry')
    +rough('Harry')

    # Define the rules
    sad(X) <= ~big(X)
    smart(X) <= ~bad(X)
    nice(X) <= wealthy(X)
    quiet(X) <= nice(X) & ~dull(X)
    poor(X) <= sad(X) & ~big(X)
    dull(X) <= little(X) & small(X)
    rough(X) <= dull(X) & ~nice(X)
    kind(X) <= smart(X)

    # Query the knowledge base
    result = kind['Harry'] # Change kind('Harry') to kind['Harry']
    if result:
        print(1)
    else:
        print(0)
except Exception as e:
    traceback_info = traceback.format_exc()
    print(traceback_info)