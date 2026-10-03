import urllib.request
import json

url = "http://127.0.0.1:8000/api/query"
data = json.dumps({"query": "Apa prosedur maintenance untuk pompa?", "mode": "rag"}).encode("utf-8")
headers = {"Content-Type": "application/json"}

try:
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode("utf-8"))
        print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Error: {e}")
