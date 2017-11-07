import pytest
from stripe_pipeline.handlers import get_value
from stripe_pipeline.handlers import validate_and_extract
from stripe_pipeline.handlers import JSONFormatException


def test_get_value():
    a_dict = {'a': {'b': {'d': 3}}}

    assert get_value(a_dict, ('a', 'b', 'd')) == 3

    with pytest.raises(JSONFormatException) as error:
        get_value(a_dict, ('a', 'b', 'c'))
        
    assert 'c not found in input JSON' in str(error.value)


def test_validate_and_extract():
    correct_json = """
        {
            "a": {
                "b": {
                    "c": 123
                }
            }
        }
    """

    assert validate_and_extract(correct_json, ('a', 'b', 'c')) == 123

    incorrect_json = """
        {
            "a": {
                "b": {
                    "c": 123
            }
        }"""

    with pytest.raises(JSONFormatException) as error:
        validate_and_extract(incorrect_json, ('a', 'b', 'c'))
    assert 'Decoding error encountered' in str(error.value)
