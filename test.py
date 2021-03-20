import requests

url = 'https://top.gg/api/bots/805082505320333383/stats'

server_count = {'server_count': 73, 'shard_count': 1} 

headers= {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjgwNTA4MjUwNTMyMDMzMzM4MyIsImJvdCI6dHJ1ZSwiaWF0IjoxNjE1NzA0NjA1fQ.srX61MkOVRsjAgF2_4yVGwHLC7RJINCZQJike33Noh8'}
        
x = requests.post(url, headers=headers, json=server_count)
for i in x:
    print(i)
        