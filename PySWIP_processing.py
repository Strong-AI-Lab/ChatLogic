from pyswip import Prolog
prolog = Prolog()

# Propositions
prolog.assertz("rough(wolf)")
prolog.assertz("lazy(wolf)")
prolog.assertz("sleepy(wolf)")
prolog.assertz("sees(wolf, mouse)")
prolog.assertz("needs(crocodile, dog)")
prolog.assertz("awful(crocodile)")
prolog.assertz("heavy(crocodile)")
prolog.assertz("quiet(mouse)")
prolog.assertz("round(mouse)")
prolog.assertz("kind(mouse)")
prolog.assertz("small(dog)")
prolog.assertz("beautiful(dog)")
prolog.assertz("lovely(dog)")
prolog.assertz("small(X) :- quiet(X)")
prolog.assertz("chases(X, mouse) :- lazy(X)")
prolog.assertz("slow(X) :- chases(X, mouse)")
prolog.assertz("sleepy(X) :- rough(X), lazy(X)")
prolog.assertz("furry(X) :- small(X), beautiful(X)")
prolog.assertz("fierce(X) :- awful(X), heavy(X)")
prolog.assertz("dull(X) :- sleepy(X)")
prolog.assertz("beautiful(X) :- small(X)")
prolog.assertz("big(X) :- fierce(X)")
prolog.assertz("cute(X) :- furry(X)")

# Question
query = "beautiful(mouse)"
results = list(prolog.query(query))
if results:
    print("true")
else:
    print("false")

