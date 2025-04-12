from wikipedia_crewai.src.wikipedia_crewai.tools import wikipedia_search

topic = "AI"

# Test direct string
print(wikipedia_search("Inteligência Artificial"))

# Test JSON string
print(wikipedia_search('{"topic": "Inteligência Artificial"}'))

# Test agent-style input
print(wikipedia_search({"input_data": {"description": "Inteligência Artificial"}}))

# Test alternative formats
print(wikipedia_search({"description": "Inteligência Artificial"}))
print(wikipedia_search({"value": "Inteligência Artificial"}))
