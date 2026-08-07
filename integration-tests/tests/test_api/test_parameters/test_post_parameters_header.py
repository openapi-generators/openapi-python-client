from integration_tests.api.parameters.post_parameters_header import request
from integration_tests.client import Client


async def test(client: Client) -> None:
    string_header = "a test string"
    integer_header = 1
    number_header = 1.1
    boolean_header = True

    parsed = await request(
        client=client,
        boolean_header=boolean_header,
        string_header=string_header,
        integer_header=integer_header,
        number_header=number_header,
    )

    assert parsed.string == string_header
    assert parsed.integer == integer_header
    assert parsed.number == number_header
    assert parsed.boolean == boolean_header
