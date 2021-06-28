import json
import csv

with open("issues.json") as file:
    data = json.load(file)

with open("issues.csv", "w") as file:
    csv_file = csv.writer(file)
    CSV_HEADER = ["Likes", "number", "title"]
    csv_file.writerow(CSV_HEADER)

    for item in data:
        # want: votes, repo, issue num, title,
        csv_file.writerow(["?", item['number'], item['title']])
