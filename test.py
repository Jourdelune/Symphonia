import requests

url = 'https://discordbotlist.com/api/v1/bots/805082505320333383/stats'
myobj = {'guilds': 40, 'users': 143372}

headers= {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0IjoxLCJpZCI6IjgwNTA4MjUwNTMyMDMzMzM4MyIsImlhdCI6MTYxNDc4MzQ1NX0.2SFePhEe8sqx6kpk0JaEsu84tL1-OvchDYikR8Mfyqs'}
        
x = requests.post(url, headers=headers, data = myobj)

for i in x:
    print(i)
        