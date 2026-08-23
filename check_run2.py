import sys, json
d = json.load(open("runs/run-2-2026-08-23T00:34:23Z.json"))
print("model:", d["model"])
print("run:", d.get("run"))
print("host:", d["host"])
for r in d["results"]:
    print(r["prompt"], ":", r["tokens"], "tok,", r["total_s"], "s", "first_token_s:", r["first_token_s"])