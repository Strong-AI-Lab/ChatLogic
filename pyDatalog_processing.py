import traceback
from pyDatalog import pyDatalog

try:
    # Declare the pyDatalog variables
    pyDatalog.create_terms(
        'X, bald_eagle, sleepy, rough, leopard, heavy, fierce, visits, rabbit, sees, dog, nice, furry, lovely, needs, slow, around, strong, cute, big, small, awful, beautiful')

    # Define the facts
    +sleepy('bald_eagle')
    +rough('bald_eagle')
    +heavy('leopard')
    +fierce('leopard')
    +visits('bald_eagle', 'rabbit')
    +sees('leopard', 'dog')
    +nice('rabbit')
    +nice('dog')
    +furry('dog')
    +lovely('dog')

    # Define the rules
    needs(X) <= ~nice(X)
    slow(X) <= needs(X)
    heavy(X) <= ~around(X)
    cute(X) <= ~strong(X)
    lovely(X) <= furry(X)
    small(X) <= lovely(X) & ~big(X)
    awful(X) <= heavy(X) & ~around(X)
    big(X) <= sleepy(X) & rough(X)
    fierce(X) <= big(X) & ~lovely(X)
    beautiful(X) <= cute(X)

    # Query the knowledge base
    result = awful('bald_eagle')
    if result:
        print(1)
    else:
        print(0)
except Exception as e:
    traceback_info = traceback.format_exc()
    print(traceback_info)
