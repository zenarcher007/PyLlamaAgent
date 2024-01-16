#!/usr/bin/env python3

#Copyright 2024 <Justin Douty>
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import requests
import json
import re
import math
import sys
from io import StringIO
import traceback
from PyLlamaAgent import Agent

def get_code_blocks_contents(text):
  pattern = r"^(```[a-z0-9]*)(.*?)(```$)"
  #pattern = r"^```"
  #c = re.compile(pattern, re.MULTILINE)
  #matches = [match for match in c.finditer(text)]
  matches = re.search(pattern, text, flags = re.MULTILINE | re.DOTALL)
  #print(matches)
  if matches:
    return matches.group(2)
  else:
    return None


def main(argv=None):
  coder = Agent("Coder", "mistral")
  prompt = "Write a Python function that calculates the first 10 terms of the fibbinocchi sequence"
  r = coder.ask(prompt)
  func = get_code_blocks_contents(r)
  r = coder.ask("Write code for test cases for this function. The test cases should each call the original function and test that its return value is as-expected. Make sure to write a complete program with import statements, a \"main\" function, the original function, the test cases, and anything else necessary. Call each of the test case functions in main, and call the \"finish(status)\" function with True if all cases passed, or False if not (DO NOT define this function as it already exists). Any additional printouts are to your benefit.")
  prog = get_code_blocks_contents(r)
  redirected_output_out = ""
  redirected_output_err = ""
  while True:
    symbolTable = vars(math).copy()
    symbolTable.update(vars(re))
    fStatus = None
    def finish(status):
      print("Agent called finish with status: " + str(status))
      fStatus = status
    symbolTable['finish'] = finish
    symbolTable['__name__'] = '__main__'
    #symbolTable['main'] = None
  
    e = ""
    redirected_output = ""
    # Capture stdout from exec https://stackoverflow.com/a/3906309
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    redirected_output_out = sys.stdout = StringIO()
    redirected_output_err = sys.stderr = StringIO()
    prog = str(prog)
    print("Compiling...", file = sys.stderr)
    print(prog)
    result = None
    try:
      prog = compile(prog, '<string>', 'exec', optimize=2)
      exec(prog, symbolTable, symbolTable)
      #result = symbolTable['main']()
    except Exception as exc:
      tb = traceback.format_exc()
      e = tb
      #repr(exc)
      print(f"\nAgent's code failed with exception: \n{e}\nprintout:\n{redirected_output_out}\n{redirected_output_err}\n")
      r = coder.ask(f"The function doesn't work. The code has the exception:\n {e}.\n It also printed \"{redirected_output_out}\n{redirected_output_err}\". Please rewrite just the original function.")
      prog = get_code_blocks_contents(r)
    
    redirected_output_out = redirected_output_out.read()
    redirected_output_err = redirected_output_err.read()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    
    if fStatus == True: # Note that this works because "main" will be preserved in the symbol table unless updated
      print("Agent's code passed all self-designed test cases!")
      break
    elif fStatus == None:
      print("\nAgent did not return status in main() function. Retrying...\n")
      r = coder.ask("You are supposed to call finish(True) when all test cases pass, or finish(False) otherwise (DO NOT define this function as it already exists).")
      #coder.ask("You are supposed to make the program exit with a status of 1 if none of the test cases pass, or 0 if they all succeed.") #coder.ask("Even though it is counterintuitive, you are supposed to return True FROM the main() function if all test cases pass, or False if not. Please update the main() function")
      prog = get_code_blocks_contents(r)
    elif fStatus == False:
      print("\nAgent did not pass all self-designed test cases.\n")
      r = coder.ask("Your code did not pass your test cases. Please revise your code.")
      prog = get_code_blocks_contents(r)
    
  print("\nFinal program:\n\n" + prog)
if __name__ == "__main__":
  main()
