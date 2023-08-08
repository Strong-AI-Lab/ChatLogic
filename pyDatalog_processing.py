import traceback
from pyDatalog import pyDatalog

try:
    # Declare the pyDatalog variables
    pyDatalog.create_terms(
        'X, Erin, Bob, Dave, Harry, high, big, strong, little, thin, smart, wealthy, kind, sad, bad, poor, small, short, quiet, nice, dull, rough')

    # Define the facts
    +high('Erin')
    +big('Erin')
    +strong('Erin')
    +little('Bob')
    +thin('Bob')
    +smart('Dave')
    +wealthy('Dave')
    +kind('Dave')
    +sad('Harry')
    +bad('Harry')
    +poor('Harry')

    # Define the rules
    smart(X) <= high(X)
    small(X) <= little(X) & thin(X)
    dull(X) <= sad(X) & bad(X)
    quiet(X) <= smart(X) & wealthy(X)
    wealthy(X) <= smart(X)
    nice(X) <= quiet(X)
    rough(X) <= dull(X)
    short(X) <= small(X)  # Missing rule for 'All small people are short.'

    # Query the knowledge base
    result = short('Bob')
    if result:
        print(1)
    else:
        print(0)
except Exception as e:
    traceback_info = traceback.format_exc()
    print(traceback_info)