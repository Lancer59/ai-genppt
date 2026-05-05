import os
from dotenv import load_dotenv

load_dotenv()

from genppt.agent.graph import graph

initial_state = {
    "topic": "The future of AI",
    "slide_count": 3,
    "theme": "dark",
    "output_path": "output_test.pptx"
}

print("Running pipeline...")
result = graph.invoke(initial_state)
print("Success:", result.get("pptx_path"))
