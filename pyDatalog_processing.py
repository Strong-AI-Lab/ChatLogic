import traceback
from pyDatalog import pyDatalog
try:
    # Declare the pyDatalog variables
    pyDatalog.create_terms('X, snake, tired, dull, reckless, chase, wolf, visit, mouse, awful, big, dog, nice, quiet, round, cute, furry, small, lovely, strong, angry, slow, obese, fierce, sleepy, adorable, funny, beautiful, lazy, heavy, boring, rough, smart')

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
    +dog('The dog')
    +nice('The dog')
    +quiet('The dog')
    +round('The dog')
    +mouse('The mouse')
    +cute('The mouse')
    +furry('The mouse')
    +small('The mouse')

    # Define the rules
    cute[X] <= nice[X]
    dull[X] <= sees(X, 'the dog')
    lazy[X] <= sees(X, 'the dog')
    reckless[X] <= tired[X] & dull[X]
    lovely[X] <= cute[X] & furry[X]
    strong[X] <= awful[X] & big[X]
    angry[X] <= reckless[X]
    slow[X] <= angry[X]
    big[X] <= slow[X]
    awful[X] <= big[X]
    furry[X] <= cute[X]
    small[X] <= furry[X]
    round[X] <= small[X]
    smart[X] <= round[X]
    kind[X] <= small[X]
    obese[X] <= strong[X]
    fierce[X] <= obese[X]
    dull[X] <= fierce[X]
    sleepy[X] <= dull[X]
    adorable[X] <= lovely[X]
    funny[X] <= adorable[X]
    tired[X] <= funny[X]
    beautiful[X] <= tired[X]
    heavy[X] <= lazy[X]
    boring[X] <= heavy[X]
    rough[X] <= boring[X]

    # Query the knowledge base
    result = smart('The dog')
    if result:
        print(1)
    else:
        print(0)
except Exception as e:
    traceback_info = traceback.format_exc()
    print(traceback_info)