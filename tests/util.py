api_key: str = "api-key-string"
bearer_token: str = "bearer-token-string"
mock_data = {"testkey": "testval"}


def mock_json():
    return mock_data


mock_body = {"body": mock_data}
mock_guid = {"guid": mock_data}
mock_identifier = {
    "identifier": mock_data,
    "email": "testemail@example.com",
    "body": mock_data,
}
