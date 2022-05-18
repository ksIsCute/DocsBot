import requests
with open("pfp.jpg", "rb") as img:
  imgb = img.read()
link = requests.patch(
  "https://demo.lightspeed.tv/users/@me", 
  headers={
    "accept": "application/json", 
    "x-session-token": "LbFMF_TWZg7ROiAYDo1tPmcd1SFUr_UuZntVBxfmiEjuYibOyL8v_n9AGKkRMpEJ", 
    "Content-Type": "application/json"
  }, data={
    "avatar": imgb
  }
)

try:
  print(link.json())
except Exception as e:
  print(e)