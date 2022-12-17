from integration_tests.api.parameters.post_parameters_header import sync_detailed
from integration_tests.client import Client
from integration_tests.models.post_parameters_header_response_200 import PostParametersHeaderResponse200


def test(client: Client) -> None:
    string_header = "a test string"
    integer_header = 1
    number_header = 1.1
    boolean_header = True

    response = sync_detailed(
        client=client,
        boolean_header=boolean_header,
        string_header=string_header,
        integer_header=integer_header,
        number_header=number_header,
    )

    parsed = response.parsed
    assert parsed is not None, f"{response.status_code}: {response.content!r}"
    assert isinstance(
        parsed,
        PostParametersHeaderResponse200,
    ), parsed
    assert parsed.string == string_header
    assert parsed.integer == integer_header
    assert parsed.number == number_header
    assert parsed.boolean == boolean_header
