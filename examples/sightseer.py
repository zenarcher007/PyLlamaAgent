#!/usr/bin/env python3

from PyLlamaAgent import Agent, Endpoint, OllamaModel
import sys

# Demonstrates the ability for llava-capable models to process images
# Example Usage: ./sightseer.py "Describe this image." ~/Downloads/DSC_3713.JPG
def main(argv=None):
  if len(argv) <= 1:
    print(f"Usage: {argv[0]} <Prompt> [image 1] [image 2]...")
    sys.exit()
  
  endpoint = Endpoint("http://localhost:11434/api/generate")
  model = OllamaModel(tag = "llava:7b-v1.5-q2_K")

  agent = Agent("SightSeer", model, endpoint)
  agent.ask(argv[1], images = argv[2:])
  print("\n", file = sys.stderr)
  

if __name__ == "__main__":
  main(sys.argv)

