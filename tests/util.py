api_key: str = "api-key-string"
bearer_token: str = "bearer-token-string"
mock_data = {"testkey": "testval"}


def mock_json():
    return mock_data


mock_team_id = "1234567890a"
mock_body = {"body": mock_data}
mock_guid = {"guid": mock_data}
mock_identifier = {
    "identifier": mock_data,
    "email": "testemail@example.com",
    "body": mock_data,
    "name": "Gremlin",
}
mock_payload = {
    "body": mock_data,
    "headers": "1234567890",
    "data": mock_data,
}
mock_uid = {"body": mock_data, "uid": "1234567890z"}
mock_metrics = {
    "attackId": "1234567890",
    "scenarioId": "1234567890",
    "scenarioRunNumber": "1",
}
mock_report = {
    "start": "mock_start",
    "end": "mock_end",
    "period": "4",
    "startDate": "1/1/1900",
    "endDate": "1/1/2000",
    "trackingPeriod": "6",
}
mock_saml = {
    "SAMLResponse": "mock_response",
    "RelayState": "mock_state",
    "companyName": "Gremlin Mocks",
    "destination": "earth",
    "acsHandler": "mock_handler",
    "code": "12567890",
}
