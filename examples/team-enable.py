import getpass
from gremlinapi.config import GremlinAPIConfig as config
from gremlinapi.clients import GremlinAPIClients as clients
from gremlinapi.orgs import GremlinAPIOrgs as orgs
import sys

def enable_all(team_id, targets) -> bool:
    success = True
    for rover in targets:
        if clients.activate_client(teamId=team_id, guid=rover['identifier']) != 'Success':
            success = False
    return success

def disable_all(team_id, targets) -> bool:
    success = True
    for rover in targets:
        if clients.deactivate_client(teamId=team_id, guid=rover['identifier']) != 'Success':
            success = False
    return success

def confirm_yes() -> bool:
    while True:
        answer = input("Proceed?  Enter \"yes\" or \"no\": ").casefold()
        if answer == 'yes':
            return True
        elif answer == 'no':
            return False
        else:
            print(f"""\"{answer}\" is not valid.""")

def interactive_enable_agents() -> bool:
    print("""
This application needs your Gremlin API Key.  Managing Gremlin API Keys is done at
https://app.gremlin.com/profile/apikeys

The next prompt, where you enter your Gremlin API Key, does not echo what you type to help keep your
Gremlin API Key protected.  Ctrl + Shift + V works to paste in Linux and Windows.  Command + V works
to paste in macOS.  Your Gremlin API Key can be copied from the webpage by clicking the double
document copy button next to the API Key name then clicking the popup.
""")
    key = getpass.getpass('Enter your Gremlin API Key: ')
    config.api_key = 'Key 8b4500db2d49008c5a89336b0cef41ca0e08ae5b0f8034497fd2cc61b1f20a5e'
    all_orgs = orgs.list_orgs()
    name_and_id = [(x['name'].casefold(), x['name'], x['identifier']) for x in all_orgs]
    name_and_id.sort()
    print(f"""
There are {len(name_and_id)} teams accessible.  Please enter the number or name of the team you want
to change.
""")
    for index, rover in enumerate(name_and_id):
        print(f"  {index+1:>2}  {rover[1]}")
    print()
    team = input('Enter the team to change: ')
    try:
        team_index = int(team) - 1
    except ValueError:
        folded = team.casefold()
        for index, rover in enumerate(name_and_id):
            if folded == rover[0]:
                team_index = index
    try:
        team_index
        team_index_valid = True
    except NameError:
        team_index_valid = False
    if team_index_valid:
        if team_index >= len(name_and_id):
            print(f"""
{team} is too big.  The maximum is {len(name_and_id)}.
""")
            return False
        if team_index < 0:
            print(f"""
{team} is too small.  The minimum is 1.
""")
            return False
    else:
        # Try a substring search?  Or a prefix search?
        print(f"""
{team} is not a valid number nor is it a valid team name.
""")
        return False
    team_id = name_and_id[team_index][2]
    targets = clients.list_clients(teamId=team_id)
    print(f"""
The \"{name_and_id[team_index][1]}\" team has {len(targets['active'])+len(targets['idle'])} enabled Agent(s) and {len(targets['inactive'])} disabled Agent(s).

Do you want all the Agents to be enabled or disabled?
""")
    action = input("Enter \"enabled\" or \"disabled\": ").casefold()
    success = True
    if action == 'enabled':
        targets = targets['inactive']
        print()
        if len(targets) > 0:
            if len(targets) <= 20:
                print("The following disabled Agents will be enabled...")
                print()
                for rover in targets:
                    print("  ", rover['identifier'])
            else:
                print(f"""The {len(targets)} disabled Agents will be enabled.""")
            print()
            if confirm_yes():
                if not enable_all(team_id, targets):
                    success = False
        else:
            print("There are no disabled Agents to enable.")
        print()
    elif action == 'disabled':
        targets = targets['active'] + targets['idle']
        print()
        if len(targets) > 0:
            if len(targets) <= 20:
                print("The following enabled Agents will be disabled...")
                print()
                for rover in targets:
                    print("  ", rover['identifier'])
            else:
                print(f"""The {len(targets)} enabled Agents will be disabled.""")
            print()
            if confirm_yes():
                if not disable_all(team_id, targets):
                    success = False
        else:
            print("There are no enabled Agents to disable.")
        print()
    else:
        print(f"""
{action} is not a valid action.
""")
        success = False
    return success

if __name__ == '__main__':
    sys.exit(interactive_enable_agents())
