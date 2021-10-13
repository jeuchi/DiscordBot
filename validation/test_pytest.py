import json
from constants import EMAIL, PASSWORD
from ubi import *

# Valid Ubisoft account
ubi = UbiAuth(email=EMAIL, password=PASSWORD)

def test_bad_authentication():
    bad_ubi = UbiAuth(email='fakeeeeee', password='lrkg4kotk4otk4')
    assert bad_ubi.create_ubi_authentication() == False

def test_not_expired():
    # First with different message
    resp_raw = '{"message":"Not expired", "age":30, "city":"New York"}'
    resp_json = json.loads(resp_raw)
    assert ubi.check_expiration(resp_json) == False

    # Second with no message at all
    resp_raw = '{"age":30, "city":"New York"}'
    resp_json = json.loads(resp_raw)
    assert ubi.check_expiration(resp_json) == False

def test_expired():
    # Should return message found and reauthenticate
    resp_raw = '{"message":"Ticket is expired", "name":"John", "city":"New York"}'
    resp_json = json.loads(resp_raw)
    assert ubi.check_expiration(resp_json) == True

def test_bad_get_data():
    # Assert invalid ticket/ids fails and create authentication
    assert ubi.get_ubi_data(link='dfdsfsdfsf') == False
    authenticated = ubi.create_ubi_authentication()
    
    # With authentication, assert link fails
    assert authenticated == True
    assert ubi.get_ubi_data(link='dfdsfsdfsf') == False

def test_valid_get_data():
    # Assert invalid ticket/ids fails and create authentication
    assert ubi.get_ubi_data(link='dfdsfsdfsf') == False
    authenticated = ubi.create_ubi_authentication()
    assert authenticated == True
    
    # With authentication, validate JSON response from all links
    username = 'KingGeorge'
    link = f'https://public-ubiservices.ubi.com/v3/profiles?namesOnPlatform={username}&platformType=uplay'
    resp_json = ubi.get_ubi_data(link=link)
    assert resp_json != False
    user_id = resp_json['profiles'][0]['userId']

    # Validate player info
    link = f'https://public-ubiservices.ubi.com/v1/spaces/5172a557-50b5-4665-b7db-e3f2e8c5041d/sandboxes/OSBOR_PC_LNCH_A/r6karma/players?board_id=pvp_ranked&season_id=-1&region_id=ncsa&profile_ids={user_id}'
    resp_json = ubi.get_ubi_data(link=link)
    assert resp_json != False

    # Validate player level
    link = f'https://public-ubiservices.ubi.com/v1/profiles/{user_id}/stats/ProgressionClearanceLevel?spaceId=5172a557-50b5-4665-b7db-e3f2e8c5041d'
    resp_json = ubi.get_ubi_data(link=link)
    assert resp_json != False

    # Validate play time
    link = f'https://public-ubiservices.ubi.com/v1/profiles/stats?profileIds={user_id}&spaceId=5172a557-50b5-4665-b7db-e3f2e8c5041d&statNames=ProgressionPvPTimePlayed'
    resp_json = ubi.get_ubi_data(link=link)
    assert resp_json != False