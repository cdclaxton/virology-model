from config.reader import validate_config, read_json_config


def test_valid1():
    file_path = "./config/test_data/valid1.json"
    assert validate_config(read_json_config(file_path))


def test_invalid1():
    file_path = "./config/test_data/invalid1.json"
    assert not validate_config(read_json_config(file_path))


def test_invalid2():
    file_path = "./config/test_data/invalid2.json"
    assert not validate_config(read_json_config(file_path))
