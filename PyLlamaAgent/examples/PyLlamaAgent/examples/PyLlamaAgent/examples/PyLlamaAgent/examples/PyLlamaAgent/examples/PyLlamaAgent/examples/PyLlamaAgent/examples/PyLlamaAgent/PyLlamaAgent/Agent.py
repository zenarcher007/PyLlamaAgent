


#Copyright 2024 <Justin Douty>
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import os
import base64
import sys

class Agent:
  # Note: model is for <type>Model object
  def __init__(self, name, model, endpoint, system_prompt = "", context = []):
    # Note that any variable here not marked with "_" is designed to be modifiable
    self.system_prompt = system_prompt
    self.name = name
    self.model = model
    self.context = context
    self.endpoint = endpoint
  
  def __str__(self):
    return f"[{self.model.name()}] {self.name}"
  
  def __repr__(self):
    return f"<Agent [{self.model.name()}] {self.name}>"

  def clear_context(self):
    self.context = []

  # Verbose: the Agent will print the status while loading images
  def ask(self, prompt, images = None, verbose = True):
    img_input = None
    if images != None:
      img_input = []
      c = 0
      for path in images:
        path = os.path.expanduser(path)
        c = c + 1
        if verbose:
          print(f"\r{str(self)}: Loading Image {c}/{len(images)}...", end = '', file = sys.stderr)
        image_file= open(path,"rb")
        image_data_binary = image_file.read()
        image_data = (base64.b64encode(image_data_binary)).decode('ascii')
        img_input.append(image_data)
      if verbose:
        print("\n", file=sys.stderr)
    
    response = self.endpoint.submit_query(self.model, prompt, self.system_prompt, name = self.name, images = img_input)
    self.context.append(response.context)
    return response.content
  