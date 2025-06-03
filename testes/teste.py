import requests
import json

url = "https://patrus.sensrit.com.br/api/ticket/ticketFindManagement?limit=1&offset=0"

payload = json.dumps({
  "statusFilter": [],
  "job": False,
  "filterColumns": {
    "grid_id": "R75152"
  }
})

headers = {
  'x-access-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOnsiaWQiOjMwLCJyb2xlIjoidGVjaCIsIm5hbWUiOiJKb2FvIFBlZHJvIE1hcnRpbnMgZG9zIFNhbnRvcyIsImxhbmd1YWdlIjpudWxsLCJob3N0IjoicGF0cnVzLnNlbnNyaXQuY29tLmJyIiwidGVuYW50Ijoic2Vuc3IiLCJjb21wYW55Ijp7ImlkIjoxfSwiaWRfbGFuZ3VhZ2UiOm51bGwsInRpbWV6b25lIjp7ImlkIjoxMjAsInZhbHVlIjoiQW1lcmljYS9TYW9fUGF1bG8iLCJpbnRlcnZhbCI6eyJob3VycyI6LTN9fX0sImRhdGUiOjE3NDg5NTE3MTEsImlhdCI6MTc0ODk1MTcxMSwiZXhwIjoxNzQ4OTY2MTExfQ.210F88gCiasdOIollg32RbnWMZoJB7KxgnSAzdW0eS8',
  'Content-Type': 'application/json',
  'Cookie': '36cb03=YYpl8fFdB0khneOPUbbPM2VVp0ADXNEQQfuC+MOiYAGlL7Liv1OoaQeHgI9PRkul613+0ZlugTOxAWZAGnp2mX7/ddmCCl+xFwJC/MIdqN+1pi4396xT5mIe+5aBaUYXA3uy5rsrapNp1FNxEKgCfZvpmdD1qALVo9sQiStCCcmYCFE1'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
