# A Cross-API compatible Response object for communication between Model objects, Endpoint, and Agent
class Response:
  def __init__(self, content, done, context = None):
    self.content = content
    self.done = done
    self.context = context
  
  def __repr__(self):
    return f"<Llama Response Object | content: {self.content}, done: {self.done}, context: {self.context}>"
  
  def __str__(self):
    return f"<Response | content: {self.content}, done: {self.done}, context: {self.context}>"