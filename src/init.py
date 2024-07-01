import requests

url = "https://cunghocvui.com/phuong-trinh?chat_tham_gia=NH3&page=1"

response = requests.get(url)

if response.status_code == 200:
    print(response.text)
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")
