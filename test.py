import requests

url = 'https://discord.boats/api/bot/805082505320333383'

server_count = {'server_count': '49'} 

headers= {'Authorization': '4CtE99IQcwtbOMNUCGVvbHKayi6JZXBTy1kQNxR6Q9aYwL2mlJkvfIMytVqhxwJ2rwC6XGA4sTXbF0VbOuxq1cmUMP2s3rauyjxlVm0n3Xm47ixufp4rwPYuIQyN6uS3i7w8CR08PCHyt2r1rE2j6Mj3CTZ'}
        
x = requests.post(url, headers=headers, json=server_count)
for i in x:
    print(i)
        