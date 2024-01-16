#!/usr/bin/env python3

#Copyright 2024 <Justin Douty>
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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

