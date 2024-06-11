# openai_callbacks.py

class OpenAICallback:
    def __init__(self):
        self.total_tokens = 100  # Initialize total_tokens attribute

    def __enter__(self):
        # Your setup code here, if needed
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Your cleanup code here, if needed
        pass

    def update_tokens(self, tokens):
        self.total_tokens += tokens

def get_openai_callback():
    return OpenAICallback()