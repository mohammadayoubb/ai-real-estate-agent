import json

from app.services.llm_chain import extract_features_stage1


queries = [
    "A 3-bedroom two-story house with a 2-car garage built in 2005.",
    "A modern 4-bedroom home with 2500 square feet, 3 bathrooms, and a 2-car garage in NAmes, built in 2012.",
    "Small ranch house in a quiet neighborhood with one bathroom and a big lot.",
]

for i, query in enumerate(queries, 1):
    print(f"\n{'=' * 60}")
    print(f"Query {i}")
    print(f"{'=' * 60}")
    print("Input:")
    print(query)

    result = extract_features_stage1(query)

    print("\nOutput:")
    if isinstance(result, dict):
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result.model_dump(), indent=2))
