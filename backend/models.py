"""
create a abstract class model with attribute : 
- name
- version
- input_tokens


and methods : 
- chat


Then create a class openai, a class anthropic, and a class google that inherit from class model
each class should take an api key in their constructor

"""
import openai
from abc import ABC, abstractmethod

class Model(ABC):
    def __init__(self, version, input_tokens):
        self.version = version

    @abstractmethod
    def initiate_conversation(self):
        pass

    @abstractmethod
    def chat(self):
        pass

class OpenAI(Model):
    def __init__(self, version, api_key):
        super().__init__(version)
        self.api_key = api_key

    def chat(self):
        # Implement chat functionality for OpenAI here
        pass

class Anthropic(Model):
    def __init__(self, version, api_key):
        super().__init__(version)
        self.api_key = api_key

    def chat(self):
        # Implement chat functionality for Anthropic here
        pass

class Google(Model):
    def __init__(self, version, api_key):
        super().__init__(version)
        self.api_key = api_key

    def chat(self):
        # Implement chat functionality for OpenAI here
        pass



def get_model(model_name):
    # Depending on your actual implementation, you might do more here.
    return Model(model_name)


