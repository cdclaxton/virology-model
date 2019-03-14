from model.individuals import Individuals


def test_update_individual_1():
    person = {Individuals.ID_FIELD_NAME: "id-1",
              "name": "Chris",
              "age": 23}

    individuals = Individuals()
    assert len(individuals.individual_to_attributes) == 0

    individuals.update_individual(person)
    assert len(individuals.individual_to_attributes) == 1

    assert individuals.individual_to_attributes == {
        "id-1": {"name": "Chris", "age": 23}}


def test_update_individual_2():
    person1 = {Individuals.ID_FIELD_NAME: "id-1",
               "name": "Chris",
               "age": 23}

    person2 = {Individuals.ID_FIELD_NAME: "id-2",
               "name": "Dave",
               "age": 29}

    individuals = Individuals()
    assert len(individuals.individual_to_attributes) == 0

    individuals.update_individual(person1)
    assert len(individuals.individual_to_attributes) == 1
    assert "id-1" in individuals.individual_to_attributes.keys()

    individuals.update_individual(person2)
    assert len(individuals.individual_to_attributes) == 2
    assert individuals.individual_to_attributes == {
        "id-1": {"name": "Chris", "age": 23},
        "id-2": {"name": "Dave", "age": 29}}


def test_update_from_file_1():
    filepath = "./model/test_data/individuals_1.csv"

    individuals = Individuals()
    individuals.update_from_file(1, filepath, ",", "\"", "utf-8")

    assert individuals.individual_to_attributes == {
        'id-1': {'name': 'Chris', 'age': '21'},
        'id-2': {'name': 'Dave', 'age': '29'}}

    assert individuals.timestep == 1


def test_update_from_file_2():
    filepath = "./model/test_data/individuals_1.csv"

    # Define a dictionary of converters
    converters = {'age': lambda x: int(x)}

    individuals = Individuals()
    individuals.update_from_file(1, filepath, ",", "\"", "utf-8", converters)

    assert individuals.individual_to_attributes == {
        'id-1': {'name': 'Chris', 'age': 21},
        'id-2': {'name': 'Dave', 'age': 29}}

    assert individuals.timestep == 1
