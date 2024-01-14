#!/usr/bin/env python3

import sys
import re
from PyLlamaAgent import Agent


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

  writer = Agent("Writer", "mistral", "You are to revise your ascii art in a code block, taking the user feedback into consideration.")
  # vvv Don't forget to change the object in the prompt here if you decide to do so vvv
  checker = Agent("Checker", "mistral", f"You are a reviewer. Without directly telling what the image is supposed to be, review that the ascii art represents the best possible representation of the target image, and without providing examples, list ONLY EXACTLY ONE SPECIFIC and helpful improvement to strive for. The ascii art should look as much as possible like a {sys.argv[1]}. Remember: colors don't exist in ASCII art.") #"You are a code reviewer. Double-check the provided program. Say whether you think it meets the requirements, and state any issues you see using constructive critisism. You are not tutoring, but simply reviewing the work of the user while ensuring it will compile and produce the desired result. Positive encouragement isn't necessary, and all critisism is welcomed. The program should use dynamic programming to find the optimal number of multiplications needed to compute a matrix chain product whose sequence of dimensions is (5, 3, 6, 4, 5, 2), and A4 is a 4x5 matrix.") #"You are a philosopher arguing why artificial intelligence will have a NEGATIVE impact on the world. You are to carefully consider and critique the argument of the philosopher debating the negative impacts, and argue your counterclaim in a critical, context-aware, and evidence-backed manner."
  r = writer.ask(f"Make a large ascii art of a {sys.argv[1]}. Remember: colors don't exist in ASCII art.")
  finalcode = None
  while "```" in str(r):
    finalcode = get_code_blocks_contents(r)
    r = checker.ask("List potential improvements that could be made.")
    #checker.clear_context() # In some models, it helpts to erase the checker's memory so it doesn't think it is tutoring the writer.
    r = writer.ask("Rewrite the art based on these following suggestions:\n" + r)

  print(finalcode)

if __name__ == "__main__":
  main(sys.argv)