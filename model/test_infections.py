from model.infections import Infections


def test_infections_1():
    infections = Infections()
    assert infections.individual_to_infection == {}

    # Add the first individual
    infections.update_infection(individual_id='id-1', infection_strain=None)
    assert infections.individual_to_infection == {'id-1': None}

    # Update the first individual
    infections.update_infection(individual_id='id-1', infection_strain='ebola')
    assert infections.individual_to_infection == {'id-1': 'ebola'}


def test_infections_2():
    infections = Infections()

    # Add the first individual
    infections.update_infection(individual_id='id-1', infection_strain=None)
    assert infections.individual_to_infection == {'id-1': None}

    # Add the second individual
    infections.update_infection(individual_id='id-2', infection_strain='ebola')
    assert infections.individual_to_infection == {'id-1': None, 'id-2': 'ebola'}


def test_infections_from_file_1():
    infections = Infections()

    infections.update_from_file(1, "./model/test_data/infections_1.csv", ",", "\"", "utf-8")
    assert infections.individual_to_infection == {
        "0001": None,
        "0002": None,
        "0003": "ebola"
    }

    assert infections.timestep == 1