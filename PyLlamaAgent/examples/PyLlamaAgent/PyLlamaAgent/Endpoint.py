#Copyright 2024 <Justin Douty>
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import requests
import sys
import json
from PyLlamaAgent.Response import Response

# An Endpoint that handles submitting an API request and using the Model to decode the response
class Endpoint:
  def __init__(self, url, output = sys.stdout, verbose = True):
    self.url = url
    self.output = output # If None: do not output to "output" (ignores "output"); only return the generated text.

    self.verbose = verbose # Header titles and "pleasing" output
    
  # Makes a query to the API server, and returns the final Response object with the entire response as content when done,
  # or otherwise None in case of failure
  # Images may either be a list of URLs (if supported) or a list of base64 encoded images 
  def submit_query(self, model, prompt: str, system_prompt: str, name = "", images = None):
    data = model._formatJSONRequest(prompt, system_prompt, images)
    response = requests.post(self.url, json=data, stream=True) # Make the POST request with stream=True
    if not (self.output == None or self.verbose == False):
      print(f"[{model.name()}] {name}:", file = self.output)
    # Check if the request was successful
    resp = []
    if response.status_code == 200:
      for line in response.iter_lines():
        if line:
          # Decode each line as a JSON object
          decoded_json = json.loads(line.decode('utf-8'))
          response_obj = model._decodeJSONResponse(decoded_json)
          if response_obj.done == True: # End of stream signal
            if not (self.output == None or self.verbose == False):
              print("\n\n", file = self.output)
            response_obj.content = ''.join(resp)
            # Note that the Model object should fill the "context" parameter if end of stream was detected.
            return response_obj
          else:
            resp.append(response_obj.content) # A token
            if not self.output == None:
              print(response_obj.content, end = '', flush=True, file = self.output)
      
    else:
      print(f"{repr(self)} Request failed with status code: {response.status_code}", file = sys.stderr)
    return None