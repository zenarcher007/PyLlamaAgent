import requests
import json
import base64
import sys
import os

# A class which submits JSON queries to a language model API; tested only on the Ollama API
class Agent:
  def __init__(self, name, model, system="", url = "http://localhost:11434/api/generate", output = sys.stdout, verbose = True, suppress_output = False):
    self.system = system
    self.name = name
    self.model = model
    self.context = []
    self.url = url
    self.output = output
    self.verbose = verbose # Header titles and "pleasing" output
    self.suppress_output = suppress_output # Do not output to "output" (ignores "output"). Text will be returned from the function as a string.
  
  def clear_context(self):
    self.context = []

  def __str__(self):
    return f"[{self.model}] {self.name}"
  
  def __repr__(self):
    return f"<Agent [{self.model}] {self.name}>"

  def ask(self, prompt, images = None):
    data = {
      "system": self.system,
      "model": self.model,
      "prompt": prompt,
    }
    if self.context != []:
      data["context"] = self.context[0]
    if images != None:
      data["images"] = []
      c = 0
      for path in images:
        path = os.path.expanduser(path)
        c = c + 1
        if self.verbose:
          print(f"\r{str(self)}: Loading Image {c}/{len(images)}...", end = '', file = sys.stderr)
        image_file= open(path,"rb")
        image_data_binary = image_file.read()
        image_data = (base64.b64encode(image_data_binary)).decode('ascii')
        data["images"].append(image_data)
      if self.verbose:
        print("\n", file=sys.stderr)
    
    # Make the POST request with stream=True
    response = requests.post(self.url, json=data, stream=True)
    if not (self.suppress_output or self.verbose == False):
      print(f"{str(self)}:", file = self.output)
    # Check if the request was successful
    resp = []
    if response.status_code == 200:
      for line in response.iter_lines():
        if line:
          # Decode each line as a JSON object
          decoded_line = json.loads(line.decode('utf-8'))
          if decoded_line['done'] == True:
            self.context.append(list(decoded_line['context']))
            break
          else:
            resp.append(decoded_line['response']) # A token
            if not self.suppress_output:
              print(decoded_line['response'], end = '', flush=True, file = self.output)
      if not (self.suppress_output or self.verbose == False):
        print("\n\n", file = self.output)
    else:
      print(f"{repr(self)} Request failed with status code: {response.status_code}", file = sys.stderr)
    fullresp = ''.join(resp)
    return fullresp