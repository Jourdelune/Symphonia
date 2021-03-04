import requests

url = 'https://shadow-bot.fr/api/public/bot/stats'

server_count = {'server_count': '45'} 

headers= {'Authorization': 'Z9hQSpFaLPOCR0urPgBDrgVNGvtvTC'}
        
x = requests.post(url, headers=headers, json=server_count)

        