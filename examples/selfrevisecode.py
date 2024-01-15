#!/usr/bin/env python3

import sys
import re
from PyLlamaAgent import Agent, Endpoint, OllamaModel

def get_code_blocks_contents(text):
    pattern = r"```(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    else:
        return None

def main(argv):
  endpoint = Endpoint("http://localhost:11434/api/generate")
  model = OllamaModel(tag = "codellama:13b")

  # (Prompts developed for learning and experimentation purposes outside of class)
  writer = Agent("Writer", model, endpoint, system_prompt="You are a code-writer Agent. You are to revise your entire program in a code block, taking the user feedback into consideration. The program should find the optimal number of multiplications needed to compute a matrix chain product whose sequence of dimensions is (5, 3, 6, 4, 5, 2), and A4 is a 4x5 matrix. Not much explanation is necessary.") #"You are a philosopher arguing why artificial intelligence will have a POSITIVE impact on the world. You are to carefully consider and critique the argument of the philosopher debating the negative impacts, and argue your counterclaim in a critical, context-aware and evidence-backed manner.")
  # On some models, I notice sometimes the checker becomes a "coach", attempting to provide encouragement to the writer. The writer then gets confused, thinks it is a sentient developer, and gets lazy.

  checker = Agent("Checker", model, endpoint, system_prompt = "The provided program should use dynamic programming to find the optimal number of multiplications needed to compute a matrix chain product whose sequence of dimensions is (5, 3, 6, 4, 5, 2), and A4 is a 4x5 matrix. You are a code reviewer. Say whether the program meets the requirements, and state any potential issues you see. Do NOT highlight improvements on previous versions of the code unless those parts still need to be improved.") #"You are a code reviewer. Double-check the provided program. Say whether you think it meets the requirements, and state any issues you see using constructive critisism. You are not tutoring, but simply reviewing the work of the user while ensuring it will compile and produce the desired result. Positive encouragement isn't necessary, and all critisism is welcomed. The program should use dynamic programming to find the optimal number of multiplications needed to compute a matrix chain product whose sequence of dimensions is (5, 3, 6, 4, 5, 2), and A4 is a 4x5 matrix.") #"You are a philosopher arguing why artificial intelligence will have a NEGATIVE impact on the world. You are to carefully consider and critique the argument of the philosopher debating the negative impacts, and argue your counterclaim in a critical, context-aware, and evidence-backed manner."
  r = writer.ask("Write a program for a dynamic algorithm in C++ which can find the optimal number of multiplications needed to compute a matrix chain product whose sequence of dimensions is (5, 3, 6, 4, 5, 2), and A4 is a 4x5 matrix.")
  finalcode = None
  while "```" in str(r):
    finalcode = get_code_blocks_contents(r)
    r = checker.ask("Say \"[GOOD]\" (in brackets and capital letters) at the VERY END of your statement if the code meets the requirements AND you don't have any suggestions for improving it, or else highlight any potential issues or syntax errors in the code\n\n:" + finalcode) # Highlight any potential issues in the provided code below, or say \"[GOOD]\" (in brackets and capital letters) if you think there is no way to further improve it:\n\n" + r)
    checker.clear_context() # Erase the checker's memory so it doesn't think it has to tutor the writer.
    if("[GOOD]" in r):
      #with open("out.cpp", "w") as out:
      break
    #writer.clear_context()
    r = writer.ask("Rewrite the program based on these following suggestions:\n" + r)

  print(finalcode) # TODO: A compiler Agent that takes the resulting code and attempts to compile it, rerunning the debate if it doesn't work.



if __name__ == "__main__":
  main(sys.argv)