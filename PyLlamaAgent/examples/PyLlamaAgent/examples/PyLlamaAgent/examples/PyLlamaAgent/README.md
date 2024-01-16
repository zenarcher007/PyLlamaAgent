# PyLlamaAgent
A simple Agent API for generating conversations between AI models

---
PyLlamaAgent is a lightweight, easy to use, and extensible API, designed to simplify generating conversations between any number of Llama models for research and experimentation. Although only the Ollama API is currently supported, its modular design allows for potential integration with other common chatbot APIs. The API allows for multimodal image input and full customization of model parameters, and allows context to be stored in conversations.
<br>
## The Three Classes
Emphasizing simplicity, the three main objects you may use are the **Model**, **Endpoint**, and **Agent** objects:<br><br>
The **Model** class defines the Llama model and metaparameters to use (and internally, also defines *how* to parse communications with the API server). The **Endpoint** class uses Python's native *requests* module to submit an API request. The **Agent** class accepts both a **Model** and an **Endpoint** class as arguments, and automatically retains its chat context between queries.


### Example usage:
```
import sys
from PyLlamaAgent import OllamaModel, Endpoint, Agent

mymodel = OllamaModel(tag = "llama2:latest", temperature = 0.8)

# Output: stream object, or None for no output. verbose=False: only stream model output
myendpoint = Endpoint("http://localhost:11434/api/generate", output = sys.stdout, verbose = True)

sally = Agent(name="Sally", model=mymodel, endpoint=myendpoint, system_prompt = "Your name is Sally, an innocent snowman.")
florvo = Agent(name="Florvo", model=mymodel, endpoint=myendpoint, system_prompt = "Your name is Florvo, a ferocious fire-breathing dragon who wants to destroy Gorgeshurg.")

response = sally.ask("Announce yourself, and your presence in the great ice castle, Gorgeshurg. Show your fear for the great, ferocious fire-breathing dragon, Florvo.")
while True:
  response = florvo.ask(response)
  response = sally.ask(response)
```
<br>See the [Ollama API documentation](https://github.com/jmorganca/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values) for the full list of supported **Model** parameters.<br>
[List of supported Ollama tags](https://ollama.ai/library)

### Writing API integrations
The Model class is designed to function as a standalone model for an chatbot API design. Although not all features may be supported for every API, this helps to ensure ease of development and simplify the design. Most essentially, the *_formatJSONRequest* and *_decodeJSONResponse* functions are designed to abstract both the formatting of JSON API requests and the handling of JSON responses from the model:<br>
* _formatJSONRequest(self, prompt, system_prompt, images = None)<br>
This function is passed the request info, and must format this into a valid JSON request for the chatbot API. Images are passed as base64 input, as is standard in most chatbot APIs.<br>
* _decodeJSONResponse(self, decoded_json):
This function is called repeatedly for every message from a chatbot API stream. It must read the message and return a *Response(response, done, context)* object, where "response" is the tokens generated as text in the message, "done" is a boolean indicating whether the API has indicated the end of the message, and "context" is a Python list of integers, typically returned at the end of an API request. When "done" is True, it must fill the "context" parameter. Otherwise, it can remain as None.