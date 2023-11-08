import re
import base64
from models import get_model

class Chatbot:
    def __init__(self, model_name, system_prompt=None):
        self.model = get_model(model_name)
        self.conversation_tracker = []
        if system_prompt:
            self.conversation_tracker.append(
                {"role": "system", "content": "You are a helpful assistant."})

    def chat(self, prompt, images=[]):
        # Function to encode the image
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        # Prepare the content list with the initial text prompt
        content = [{"type": "text", "text": prompt}]

        # Iterate over the images
        for image in images:
            # Check if the image is a URL or a local path
            if image.startswith('http://') or image.startswith('https://'):
                # If it's a URL, add it directly to the content list
                content.append({"type": "image_url", "image_url": image})
            else:
                # If it's a local path, encode the image in base64 and add it to the content list
                base64_image = encode_image(image)
                content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})
        
        self.conversation_tracker.append({"role": "user", "content": content})
        # Get the response from the model
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
    if model_name=="gpt-4-1106-preview" and chatbot_type=="simple_chatbot":
        return Chatbot("gpt-4-1106-preview")
    if model_name=="gpt-4-1106-preview" and chatbot_type=="write_code_from_file":
        return CodeChatbot("gpt-4-1106-preview")
    if model_name=="gpt-4-vision-preview" and chatbot_type=="simple_chatbot":
        return Chatbot("gpt-4-vision-preview")


# Usage:
bot = get_chatbot("gpt-4-vision-preview", "simple_chatbot")
#bot = get_chatbot("gpt-3.5-turbo", "simple_chatbot")
#response = bot.chat("salut mec")
# 
response = bot.chat("ya quoi sur cette photo ?", 
                    images=["https://plus.unsplash.com/premium_photo-1676637000058-96549206fe71?q=80&w=2340&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"]
                    )
#response = bot.chat("Please write a javascript program that:", r"C:\Users\simeo\OneDrive - Vrije Universiteit Brussel\Documenten\Developpement\PERSO\Camilia\test.js")
print(response)  # This should display the bot's response

#history = bot.get_conversation_history()
#print(history) 