#!/usr/bin/env python3

from PyLlamaAgent import Agent
import sys

# Demonstrates the ability for llava-capable models to process images
# Example Usage: ./sightseer.py "Describe this image." ~/Downloads/DSC_3713.JPG
def main(argv=None):
  if len(argv) <= 1:
    print(f"Usage: {argv[0]} <Prompt> [image 1] [image 2]...")
    sys.exit()
  agent = Agent("SightSeer", "llava:7b-v1.5-q2_K")
  agent.ask(argv[1], images = argv[2:])
  print("\n", file = sys.stderr)
  

if __name__ == "__main__":
  main(sys.argv)

