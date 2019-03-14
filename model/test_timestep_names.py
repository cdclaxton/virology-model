from model.timestep_names import TimestepNames


def test_timestep_names_1():
    t = TimestepNames()

    filepath = "./model/test_data/timestep_names_1.csv"
    t.read_from_file(filepath, ",", "\"", "utf-8")

    assert t.timestep_to_name == {
        0: "March 2019",
        1: "April 2019",
        2: "May 2019"
    }
