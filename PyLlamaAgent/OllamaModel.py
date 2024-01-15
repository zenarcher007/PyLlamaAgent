from PyLlamaAgent.Response import Response
import os

# A model definition with all parameters available on the Ollama Modelfile API
# See https://github.com/jmorganca/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values for more information
class OllamaModel:
  def __init__(self, tag, mirostat = None, mirostat_eta = None, mirostat_tau = None, num_ctx = None, num_gqa = None, num_gpu = None, num_thread = None, repeat_last_n = None, repeat_penalty = None, temperature = None, seed = None, stop = None, tfs_z = None, num_predict = None, top_k = None, top_p = None):
    self.tag = tag
    self.params = {
      "mirostat": mirostat,
      "mirostat_eta": mirostat_eta,
      "mirostat_tau": mirostat_tau,
      "num_ctx": num_ctx,
      "num_gqa": num_gqa,
      "num_gpu": num_gpu,
      "num_thread": num_thread,
      "repeat_last_n": repeat_last_n,
      "repeat_penalty": repeat_penalty,
      "temperature": temperature,
      "seed": seed,
      "stop": stop,
      "tfs_z": tfs_z,
      "num_predict": num_predict,
      "top_k": top_k,
      "top_p": top_p
    }
    # Now, remove any unset parameters and let them use their default values
    self.params = {k:v for k, v in self.params.items() if v != None}
  
  # Returns a friendly name of this model
  def name(self):
    return self.tag

  # The model class defines how its JSON request should be formatted to accomodate differences between APIs 
  def _formatJSONRequest(self, prompt, system_prompt, images = None):
    data = {
      "system": system_prompt,
      "model": self.tag,
      "prompt": prompt,
    }
    if images != None:
      data["images"] = images
    data.update(self.params)
    return data
   
  # Defines how to return the content in the provided API JSON result, and how to check whether it is at the end of the output
  # Returns a Response object
  def _decodeJSONResponse(self, decoded_json):
    response = decoded_json['response'] # A token
    done = decoded_json['done']
    context = None
    if done == True:
      context = decoded_json['context']
    return Response(response, done, context)