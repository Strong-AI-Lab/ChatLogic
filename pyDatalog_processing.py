import traceback
from pyDatalog import pyDatalog
try:
    # Declare the pyDatalog variables
    pyDatalog.create_terms('X, leopard, boring, rough, reckless, attack, rabbit, bear, visit, dog, heavy, strong, smart, round_, quiet, lovely, beautiful, furry, small, obese, lazy, angry, fierce, big, dull, adorable, cute, funny, sleepy, awful, slow, tired, nice, kind')
    
    # Define the facts
    +leopard('The leopard')
    +boring('The leopard')
    +rough('The leopard')
    +reckless('The leopard')
    +attack('The leopard', 'the rabbit')
    +bear('The bear')
    +visit('The bear', 'the dog')
    +heavy('The bear')
    +strong('The bear')
    +rabbit('The rabbit')
    +smart('The rabbit')
    +round_('The rabbit')  # Change round to round_
    +quiet('The rabbit')
    +dog('The dog')
    +lovely('The dog')
    +beautiful('The dog')
    +furry('The dog')
    
    # Define the rules
    sleepy(X) <= rough(X) & attack(X, 'the rabbit')
    reckless(X) <= boring(X) & rough(X)
    small(X) <= lovely(X) & beautiful(X)
    obese(X) <= heavy(X) & strong(X)
    lazy(X) <= reckless(X)
    angry(X) <= lazy(X)
    strong(X) <= angry(X)
    dull(X) <= rough(X)
    furry(X) <= beautiful(X)
    quiet(X) <= furry(X)
    nice(X) <= quiet(X)
    kind(X) <= furry(X)
    fierce(X) <= obese(X)
    big(X) <= fierce(X)
    adorable(X) <= small(X)
    cute(X) <= adorable(X)
    funny(X) <= boring(X)
    awful(X) <= sleepy(X)
    slow(X) <= awful(X)
    tired(X) <= slow(X)
    
    # Query the knowledge base
    result = dull('The bear')
    if result:
        print(1)
    else:
        print(0)
except Exception as e:
    traceback_info = traceback.format_exc()
    print(traceback_info)