curl -X 'PATCH' \
  'https://demo.lightspeed.tv/users/@me' \
  -H 'accept: application/json' \
  -H "x-session-token: token" \
  -H 'Content-Type: application/json' \
  -d "{
    \"avatar\": $(:)
  }"