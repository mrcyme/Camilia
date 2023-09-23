import openai
import json
import re

with open("./keys.json", 'r') as j:
    keys = json.loads(j.read())
    openai.api_key = keys["OPENAI_API_KEY"]

class Model:
    def __init__(self, model_name):
        self.model_name = model_name
    
    def get_response(self, prompt):
        raise NotImplementedError("Subclasses should implement this method.")


class OpenAI(Model):
    def __init__(self, model_name="gpt-3.5-turbo"):
        super().__init__(model_name)
    
    def get_response(self, conversation):
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=conversation
        )
        return response.choices[0].message

def get_model(model_name):
    # Depending on your actual implementation, you might do more here.
    if model_name in ["gpt4", "gpt-3.5-turbo"]:
        return OpenAI(model_name)


class Chatbot:
    def __init__(self, model_name, system_prompt=None):
        self.model = get_model(model_name)
        self.conversation_tracker = []
        if system_prompt:
            self.conversation_tracker.append(
                {"role": "system", "content": "You are a helpful assistant."})

    def chat(self, prompt):
        self.conversation_tracker.append({"role": "user", "content": prompt})
        response = self.model.get_response(self.conversation_tracker)
        self.conversation_tracker.append({"role": response.role, "content": response.content})
        return response.content

    def get_conversation_history(self):
        return self.conversation_tracker


class CodeChatbot(Chatbot):
    
    def chat(self, prompt, filepath):
        """append the file content to the prompt"""
        if not prompt:
            prompt = "write code"

        with open(filepath, 'r') as file:
            content = file.read()
            extension = filepath.split('.')[-1]
            extension = '.' + extension
            commented_content = self.comment_out_content(content, extension)
            prompt = prompt + "\n" + content
            response = self.process_response(super().chat(prompt), extension)  # Call the chat method of the parent class
            final_content = commented_content + "\n" + response

        with open(filepath, 'w') as file:
            file.write(final_content)

        return response
    
    @staticmethod
    def comment_out_content(content, extension):
        """Adds comment markers based on file type."""
        COMMENT_MARKERS = {
            '.py': ('"""', '"""'),
            '.js': ('/*', '*/'),
            '.json': ('/*', '*/'),
            '.md': ('<!--', '-->'),
            '.sh': (': <<EOF', 'EOF')
        }

        start_marker, end_marker = COMMENT_MARKERS.get(extension, ('', ''))
        return start_marker + '\n' + content + '\n' + end_marker
    
    def process_response(self, response, extension):
        # Identify the language from the marker, capture code between markers
        match = re.search(r"```(\w+)\s(.*?)```", response, re.DOTALL)
        
        if not match:
            # If no code markers are found, return the response as a comment
            return self.comment_out_content(response, extension)

        language, code = match.groups()

        # Remove the markers and code from the original response
        non_code_content = response.replace(f"```{language}\n{code}```", '').strip()

        # Comment out the non-code content
        commented_non_code = self.comment_out_content(non_code_content, extension)

        return commented_non_code + '\n' + code





def get_chatbot(model_name, chatbot_type):
    if model_name == "gpt4" and chatbot_type== "write_code_from_file":
        return CodeChatbot("gpt4")
    if model_name == "gpt-3.5-turbo" and chatbot_type== "write_code_from_file":
        return CodeChatbot("gpt-3.5-turbo")
    if model_name == "gpt-3.5-turbo" and chatbot_type=="simple_chatbot":
        return Chatbot("gpt-3.5-turbo")


# Usage:
bot = get_chatbot("gpt-3.5-turbo", "write_code_from_file")
#bot = get_chatbot("gpt-3.5-turbo", "simple_chatbot")
#response = bot.chat("salut mec")
# 
response = bot.chat("Please write a javascript program that:", r"C:\Users\simeo\OneDrive - Vrije Universiteit Brussel\Documenten\Developpement\PERSO\Camilia\test.js")
print(response)  # This should display the bot's response

#history = bot.get_conversation_history()
#print(history) 