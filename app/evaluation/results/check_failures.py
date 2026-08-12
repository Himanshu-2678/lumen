import json


with open(
    "app/evaluation/results/ragas_results.json",
    "r",
    encoding="utf-8"
) as file:
    results = json.load(file)


for item in results:

    if item.get("faithfulness", 1) < 0.5:

        print("\nQUESTION:")
        print(item["question"])

        print("FAITHFULNESS:")
        print(item["faithfulness"])

        print("=" * 50)