import requests
import json

r = requests.post(
    "http://127.0.0.1:8000/api/query",
    json={"query": "Apa prosedur maintenance untuk pompa?", "mode": "rag"},
)
data = r.json()

print("=" * 60)
print("STATUS:", data.get("status"))
print("GENERATION MODE:", data.get("generation_metadata", {}).get("mode", "N/A"))
print("CONFIDENCE:", data.get("trust_badge", {}).get("confidence_percentage", "N/A"), "%")
print("=" * 60)

sources = data.get("sources", [])
print(f"\nSOURCES COUNT: {len(sources)}")
for i, s in enumerate(sources[:5]):
    print(f"\n  [{i+1}] doc_id     = {s.get('doc_id', '?')}")
    print(f"      title      = {s.get('title', '?')[:80]}")
    print(f"      score      = {s.get('similarity_score', '?')}")
    print(f"      approval   = {s.get('approval_status', '?')}")
    content = s.get("content", "")[:200]
    print(f"      content    = {content}...")

print("\n" + "=" * 60)
answer = data.get("answer", {})
if isinstance(answer, dict):
    summary = answer.get("summary", "N/A")[:500]
    print(f"ANSWER (first 500 chars):\n{summary}")
else:
    print(f"ANSWER: {str(answer)[:500]}")

print("\nEXECUTION TIMELINE:")
for step in data.get("execution_timeline", []):
    print(f"  - {step}")
