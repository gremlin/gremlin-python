api_key: str = "api-key-string"
bearer_token: str = "bearer-token-string"
mock_data = {"testkey": "testval"}
hooli_id = "9676868b-60d2-5ebe-aa66-c1de8162ff9d"
from gremlinapi.attack_helpers import (
    GremlinAttackTargetHelper,
    GremlinAttackCommandHelper,
)

mock_access_token = "asdf976asdf9786"
mock_bearer_token = "kjhg2345kjhg234"


def access_token_json():
    return {"access_token": mock_access_token}


def bearer_token_json():
    return {"header": mock_bearer_token}


def mock_json():
    return mock_data


mock_team_id = "1234567890a"
mock_body = {"body": mock_data}
mock_guid = {"guid": mock_data}
mock_scenario_guid = {
    "guid": mock_data,
    "body": mock_data,
    "startDate": "1/1/1900",
    "endDate": "1/1/2000",
    "runNumber": 1,
    "staticEndpointName": "not-a-website.comorg",
}
mock_users = {
    "role": "mock user role",
    "email": "useremail@useremailfakesite123456789.com",
    "password": "1234567890poiuytrewqASDFGHJKL",
    "orgId": "102928384756z",
    "renewToken": "42",
    "companyId": "c0mp4ny",
    "companyName": "Mocking Co, A Mockery Company",
    "provider": "MacinoogleSoft",
    "teamId": "h4x0r734m",
    "accessToken": "1q2w3e4r5t6y7u8i9o90p",
    "token": "1a1f3d4ca3f41fb4d1cb4cd4bfcd14c",
}
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
mock_scenario = {
    "description": "A mock scenario",
    "hypothesis": "to prove test status",
    "name": "mock_scenario",
}
mock_scenario_step = {
    "delay": 65536,
    "command": GremlinAttackCommandHelper(),
    "target": GremlinAttackTargetHelper(),
}
mock_ilfi_node = {
    "name": "mock_scenario",
    "command": GremlinAttackCommandHelper(),
    "target": GremlinAttackTargetHelper(),
}
mock_delay_node = {"delay": "42"}
mock_status_check_node = {
    "description": "A mock status check node",
    "endpoint_url": "definitely-fake-website1234.com",
    "endpoint_headers": {"name": "mock header"},
    "evaluation_response_body_evaluation": "mock evaluation",
    "evaluation_ok_status_codes": ["24-42"],
    "evaluation_ok_latency_max": 999,
}
