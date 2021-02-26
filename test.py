import requests

url = 'https://botsfordiscord.com/api/bot/805082505320333383'
myobj = {'server_count': 35}

headers= {'Authorization': '955a0d28ac9a65513c11309d286dd49328f5a7844d774704bb46a6365d288f70c3ea3aff6d6f5d563affbd98327fa0f38c145a97128f5615ee9c406dd8803aff'}
        
x = requests.post(url, headers=headers, data = myobj)

print(x.text)