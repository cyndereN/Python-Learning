from collections import namedtuple
from hypothesis import note, given
from hypothesis.strategies import builds,text, lists, floats, dates

Person= namedtuple('Person', ['name', 'birthday', 'pets', 'height'])

def person_strategy():
    return builds(
        Person,
        name=text(),
        birthday=dates(),
        pets=lists(text()),
        height=floats()
    )

@given(person_strategy())
def test_person(p):
    print(p)
    assert True

test_person()