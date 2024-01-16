#!/usr/bin/env python3

#Copyright 2024 <Justin Douty>
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import re
from PyLlamaAgent import Agent, Endpoint, OllamaModel


def get_code_blocks_contents(text):
  pattern = r"^(```[a-z0-9]*)(.*?)(```$)"
  matches = re.search(pattern, text, flags = re.MULTILINE | re.DOTALL)
  if matches:
    return matches.group(2)
  else:
    return None

def main(argv):
  if len(argv) == 1:
    print(f"Usage: {sys.argv[0]} <name_of_object>") # Try a castle
    sys.exit(1)

  endpoint = Endpoint("http://localhost:11434/api/generate")
  model = OllamaModel(tag = "mistral")
  
  writer = Agent(name = "Writer", model=model, endpoint=endpoint, system_prompt = "You are to revise your ascii art in a code block, taking the user feedback into consideration.")
  checker = Agent(name = "Checker", model=model, endpoint=endpoint, system_prompt = f"You are a reviewer. Without directly telling what the image is supposed to be, review that the ascii art represents the best possible representation of the target image, and without providing examples, list ONLY EXACTLY ONE SPECIFIC and helpful improvement to strive for. The ascii art should look as much as possible like a {sys.argv[1]}. Remember: colors don't exist in ASCII art.")
  r = writer.ask(f"Make a large ascii art of a {sys.argv[1]}. Remember: colors don't exist in ASCII art.")
  finalcode = None
  while "```" in str(r):
    finalcode = get_code_blocks_contents(r)
    r = checker.ask("List potential improvements that could be made.")
    #checker.clear_context() # In some models, it helps to erase the checker's memory so it doesn't think it is tutoring the writer.
    r = writer.ask("Rewrite the art based on these following suggestions:\n" + r)

  print(finalcode)

if __name__ == "__main__":
  main(sys.argv)