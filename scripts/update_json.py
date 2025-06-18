import json
import os
import re
def extract_field(text, header):
    pattern = rf"### {header}\s+(.*?)(?:\n###|\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""
with open(os.environ['GITHUB_EVENT_PATH'], 'r', encoding='utf-8') as f:
    event = json.load(f)
    body = event["issue"]["body"]
title = extract_field(body, "title")
date = extract_field(body, "date")
arxiv_link = extract_field(body, "arxiv_link")
github_link = extract_field(body, "github_link")
official_link = extract_field(body, "official_link")
category = extract_field(body, "category")
new_entry = {
    "title": title,
    "date": date,
    "arxiv_link": arxiv_link,
    "github_link": github_link,
    "official_link": official_link,
    "category": category
}
with open('public/data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
if category not in data:
    data[category] = []
found = False
for i, entry in enumerate(data[category]):
    if entry['title'] == new_entry['title']:
        data[category][i] = new_entry
        found = True
        break
if not found:
    data[category].append(new_entry)
with open('public/data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)