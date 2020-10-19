# Logging in with SAML

#### Example

This test obtains a SAML Assertion from OneLogin, and uses it to obtain a Gremlin bearer token

```python

import gremlinapi
import requests
import json

from gremlinapi.attacks import GremlinAPIAttacks

gremlin_team_id = '<YOUR GREMLIN TEAM ID>'
gremlin_company_name = '<YOUR GREMLIN COMPANY NAME>'

ol_api = "https://api.us.onelogin.com"

ol_client_id = "<OneLogin Client ID>"
ol_client_sc = "<OneLogin Secret Key>"

ol_user = "<OneLogin User Email>"
ol_pass = "<OneLogin User Password>"
ol_app_id = "<OneLogin App ID>"
ol_subdomain = "<OneLogin Account Name>"

ol_relay_state = f'{gremlin_company_name}|||https://app.gremlin.com/users/sso/saml/acs|||/'

content_type = "application/json"

### BEGIN GET SAML ASSERTION ###
ol_bearer_response = requests.post(f'{ol_api}/auth/oauth2/v2/token',
                                data=json.dumps({"grant_type": "client_credentials"}),
                                headers={"Authorization": f'client_id:{ol_client_id}, client_secret:{ol_client_sc}',
                                         "Content-Type": content_type})
ol_bearer_data = ol_bearer_response.json()
ol_bearer_token = ol_bearer_data['access_token']

ol_saml_response = requests.post(f'{ol_api}/api/2/saml_assertion',
                                 data=json.dumps({
                                     "username_or_email": ol_user,
                                     "password": ol_pass,
                                     "app_id": ol_app_id,
                                     "subdomain": ol_subdomain
                                 }),
                                 headers={"Authorization": f'bearer:{bearer_token}', "Content-Type": content_type})
ol_saml_data = ol_saml_response.json()
saml_assertion = ol_saml_data['data']
### END GET SAML ASSERTION ###

### LOG INTO GREMLIN API ###
gremlinapi.saml_login(email=ol_user, saml_assertion=saml_assertion, relay_state=ol_relay_state)

### Ensure we can retrieve data
GremlinAPIAttacks.list_attacks(teamId=gremlin_team_id)

```