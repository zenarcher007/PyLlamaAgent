import requests
import sys
import json
from PyLlamaAgent.Response import Response

# An Endpoint that handles submitting an API request and using the Model to decode the response
class Endpoint:
  # Example url for Ollama connection: "http://localhost:11434/api/generate"
  def __init__(self, url, output = sys.stdout, verbose = True, suppress_output = False):
    self.url = url
    self.output = output
    self.verbose = verbose # Header titles and "pleasing" output
    self.suppress_output = suppress_output # Do not output to "output" (ignores "output"); only return the generated text.

  # Makes a query to the API server, and returns the final Response object with the entire response as content when done,
  # or otherwise None in case of failure
  # Images may either be a list of URLs (if supported) or a list of base64 encoded images 
  def submit_query(self, model, prompt: str, system_prompt: str, name = "", images = None):
    data = model._formatJSONRequest(prompt, system_prompt, images)
    response = requests.post(self.url, json=data, stream=True) # Make the POST request with stream=True
    if not (self.suppress_output or self.verbose == False):
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
            if not (self.suppress_output or self.verbose == False):
              print("\n\n", file = self.output)
            response_obj.content = ''.join(resp)
            # Note that the Model object should fill the "context" parameter if end of stream was detected.
            return response_obj
          else:
            resp.append(response_obj.content) # A token
            if not self.suppress_output:
              print(response_obj.content, end = '', flush=True, file = self.output)
      
    else:
      print(f"{repr(self)} Request failed with status code: {response.status_code}", file = sys.stderr)
    return None