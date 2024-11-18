import requests
url = "http://127.0.0.1:8001/add"

data={
    
    'username':'saad'
}

response=requests.post(url,json=data)

if response.status_code==200:
    print('success')
else:
    print('fail')