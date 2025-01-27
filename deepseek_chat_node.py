import requests
import logging
import os
import json
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")
        self.api_key = None
        self.last_request_time = 0
        self.min_request_interval = 1.0
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.api_key = config.get('deepseek_api_key', '')
            except Exception as e:
                logger.error(f"Error loading config: {e}")
                self.api_key = ''
        else:
            self.save_config()

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        config = {'deepseek_api_key': self.api_key or ''}
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)  # Save with non-ASCII characters
        except Exception as e:
            logger.error(f"Error saving config: {e}")

config = Config()

class ComfyUIDeepSeekChat:
    def __init__(self):
        self.conversation_history = []
        self.chat_history_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "chat_history.json")
        self.load_chat_history()

    def load_chat_history(self):
        if os.path.exists(self.chat_history_file):
            try:
                with open(self.chat_history_file, 'r', encoding='utf-8') as f:
                    self.conversation_history = json.load(f)
            except Exception as e:
                logger.error(f"Error loading chat history: {e}")
                self.conversation_history = []

    def save_chat_history(self):
        try:
            with open(self.chat_history_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=4, ensure_ascii=False)  # Save with non-ASCII characters
        except Exception as e:
            logger.error(f"Error saving chat history: {e}")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (["chat", "instruct"], {"default": "chat"}),
                "prompt": ("STRING", {"default": "Hello, how can I help you?"}),
                "max_tokens": ("INT", {"default": 4096, "min": 1, "max": 8192, "step": 1}),
                "show_reasoning": ("BOOLEAN", {"default": True}),
                "clear_history": ("BOOLEAN", {"default": False}),  # Option to clear conversation history
                "remember_chat": (["yes", "no"], {"default": "yes"}),  # Option to remember chat history
            },
            "optional": {
                "vision_description": ("STRING", {"default": ""}),  # Optional image description input
            }
        }

    RETURN_TYPES = ("STRING", "STRING")  # Return both the latest response and the full chat history
    RETURN_NAMES = ("latest_response", "full_chat_history")  # Names for the outputs
    FUNCTION = "process"
    CATEGORY = "ComfyUI/DeepSeek Chat"

    def process(self, mode, prompt, max_tokens, show_reasoning, clear_history, remember_chat, vision_description=""):
        try:
            if clear_history:
                self.conversation_history = []  # Clear conversation history if requested
                if remember_chat == "yes":
                    self.save_chat_history()  # Save the cleared history to file

            if not config.api_key:
                return ("Please add your DeepSeek API key to config.json", "No history available.")

            headers = {
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json"
            }

            # Prepare messages based on mode
            if mode == "chat":
                # If vision_description is provided, prepend it to the prompt
                if vision_description:
                    prompt = f"Image description: {vision_description}\n\nUser question: {prompt}"

                # Append new user message to conversation history
                self.conversation_history.append({"role": "user", "content": prompt})
                messages = self.conversation_history
            else:  # instruct mode
                messages = [{"role": "user", "content": prompt}]

            data = {
                "model": "deepseek-reasoner",
                "messages": messages,
                "max_tokens": max_tokens,
            }

            # Rate limiting
            current_time = time.time()
            time_since_last_request = current_time - config.last_request_time
            if time_since_last_request < config.min_request_interval:
                time.sleep(config.min_request_interval - time_since_last_request)

            # Send request to DeepSeek API
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            config.last_request_time = time.time()

            if response.status_code == 200:
                result = response.json()
                if "choices" in result and result["choices"]:
                    content = result["choices"][0]["message"]["content"]

                    if mode == "chat":
                        # Append assistant's response to conversation history
                        self.conversation_history.append({"role": "assistant", "content": content})
                        if remember_chat == "yes":
                            self.save_chat_history()  # Save updated history to file

                    # Format the full chat history as a readable string
                    full_chat_history = self.format_chat_history(self.conversation_history)

                    if show_reasoning:
                        reasoning = result["choices"][0]["message"].get("reasoning_content", "")
                        latest_response = f"Reasoning:\n{reasoning}\n\nResponse:\n{content}"
                    else:
                        latest_response = content

                    return (latest_response, full_chat_history)
                return ("No content in response", "No history available.")
            else:
                error = f"API Error {response.status_code}: {response.text}"
                logger.error(error)
                return (error, "No history available.")

        except Exception as e:
            error = f"Error: {str(e)}"
            logger.exception(error)
            return (error, "No history available.")

    def format_chat_history(self, history):
        """Format the conversation history into a readable string."""
        formatted_history = []
        for message in history:
            role = message["role"]
            content = message["content"]
            formatted_history.append(f"{role.capitalize()}: {content}")
        return "\n\n".join(formatted_history)

NODE_CLASS_MAPPINGS = {
    "ComfyUIDeepSeekChat": ComfyUIDeepSeekChat,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUIDeepSeekChat": "DeepSeek-R1 Chat/Instruct"
}