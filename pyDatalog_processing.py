import traceback
from pyDatalog import pyDatalog

try:
    # Declare the pyDatalog variables
    pyDatalog.create_terms(
        'X, Y, Z, big, huge, thin, small, wealthy, poor, dull, rough, quiet, nice, kind, smart, sad, bad, high')

    # Define the facts
    + big('Fiona')
    + huge('Fiona')
    + thin('Charlie')
    + small('Charlie')
    + wealthy('Harry')
    + poor('Gary')
    + dull('Gary')
    + ~rough('Fiona')
    + ~thin('Fiona')
    + ~wealthy('Fiona')
    + ~high('Fiona')
    + ~small('Fiona')
    + ~rough('Charlie')
    + ~thin('Charlie')
    + ~wealthy('Charlie')
    + ~high('Charlie')
    + ~high('Harry')
    + ~small('Harry')
    + ~rough('Harry')
    + ~thin('Harry')
    + ~small('Gary')
    + ~rough('Gary')
    + ~thin('Gary')
    + ~wealthy('Gary')
    + ~high('Gary')


    # Define the rules
    poor(X) <= ~high(X)
    quiet(X) <= ~rough(X)
    nice(X) <= wealthy(X)
    kind(X) <= nice(X) & ~bad(X)
    bad(X) <= thin(X) & small(X)
    dull(X) <= bad(X) & ~nice(X)
    smart(X) <= quiet(X)

    # Query the knowledge base
    result = sad('Fiona')
    if result:
        print(1)
    else:
        print(0)
except Exception as e:
    traceback_info = traceback.format_exc()
    print(traceback_info)