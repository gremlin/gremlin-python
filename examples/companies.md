# Companies Endpoint

### Get Company Details

```python
from gremlinapi.companies import GremlinAPICompanies as companies

company_id = 'COMPANY_GUID'
response = companies.get_company(identifier=company_id)
```

### List Company Clients

```python
from gremlinapi.companies import GremlinAPICompanies as companies

company_id = 'COMPANY_GUID'
response = companies.list_company_clients(identifier=company_id)
```

### Invite Company User

```python
from gremlinapi.companies import GremlinAPICompanies as companies

company_id = 'COMPANY_GUID'
user_email_body = { 'email': 'andjohn@gremlin.com' }
response = companies.invite_company_user(identifier=company_id, body=user_email_body)
```

```python
from gremlinapi.companies import GremlinAPICompanies as companies

company_id = 'COMPANY_GUID'
user_email_body = { 'emails': ['andjohn+1@gremlin.com', 'andjohn+2@gremlin.com'] }
response = companies.invite_company_user(identifier=company_id, body=user_email_body)
```

### Delete Company Invite

```python
from gremlinapi.companies import GremlinAPICompanies as companies

company_id = 'COMPANY_GUID'
user_email = 'andjohn@gremlin.com'
response = companies.delete_company_invite(identifier=company_id, body=user_email)
```

### Update Company MFA Preferences

### Update Company Preferences

### Update Company SAML Properties

### List Company Users

```python
from gremlinapi.companies import GremlinAPICompanies as companies

company_id = 'COMPANY_GUID'
response = companies.list_company_users(identifier=company_id)
```

### Update Company User Roles

### Activate Company User

### Deactivate Company User