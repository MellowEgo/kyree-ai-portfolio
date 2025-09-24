# stub index builder
import os, json
os.makedirs("projects/02_genai_policy_assistant/.index", exist_ok=True)
with open("projects/02_genai_policy_assistant/.index/meta.json","w") as f:
    json.dump({"status":"indexed"}, f)
print("Indexed policies.")