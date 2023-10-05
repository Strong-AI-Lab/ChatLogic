import traceback
from pyDatalog import pyDatalog
try:
    # Declare the pyDatalog variables
    pyDatalog.create_terms('X, Harry, strong, huge, Gary, small, short, Charlie, wealthy, Fiona, rough, poor, big, sad, smart, kind, bad, nice, dull, quiet')

    # Define the facts
    +strong('Harry')
    +huge('Harry')
    +small('Gary')
    +short('Gary')
    +wealthy('Charlie')
    +rough('Fiona')
    +poor('Fiona')

    # Define the rules
    rough(X) <= ~big(X)
    smart(X) <= ~sad(X)
    kind(X) <= wealthy(X)
    nice(X) <= kind(X) & ~bad(X)
    dull(X) <= rough(X) & ~big(X)
    bad(X) <= small(X) & short(X)
    poor(X) <= bad(X) & ~kind(X)
    quiet(X) <= smart(X)

    # Query the knowledge base
    result = ~poor('Gary')
    if result:
        print(1)
    else:
        print(0)
except Exception as e:
    traceback_info = traceback.format_exc()
    print(traceback_info)