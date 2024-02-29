from openai import OpenAI


class __BaseChat:
    def __init__(
        self,
        topic: str,
        threads: int,
        length: int,
        key: str,
        model: str,
        data_format: str,
        system_prompt="Your are a helpful assistant.",
    ):
        """
        The function takes the following arguments:-
        :param topic: The topic on which the chat is intended to be generated
        :param threads: The number of chats to be generated
        :param length: The value to indicate how long a chat session will be
        :param key: The Open AI key
        :param model: The Open AI model through which data will be generated
        :param data_format: The format in which the generated data will be presented
        """
        # Validation of variables
        assert length > 0, f"Length passed - {length} should be greater than 0"
        assert threads > 0, f"Threads passed - {threads} should be greater than 0"
        assert "sk" in key, f"Invalid API KEY passed - {key}"

        # Variable declaration
        self.CONVERSATION_LENGTH = length
        self.TOPIC = topic
        self.THREADS = threads
        self.MODEL = model
        self.FORMAT = data_format
        self.KEY = key
        self.SYSTEM_PROMPT = system_prompt
        self.client = OpenAI(api_key=key)

    def initiate_chat(self) -> str:
        """
        This function is responsible for fragmenting a particular topic into N number of chat topics which might occur
        is real life during a chat session on that topic
        :return: A Python list in the form of a string containing the different chat topics
        """
        completion = self.client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an obedient and a helpful assistant. "
                        "Your every answer must be in the form of python list with different elements."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Based on this topic, {self.TOPIC} - "
                        f"Your job is to break this topic into {self.THREADS} articulate chat topics, "
                        "which might occur in real life. "
                        "You answer by making a Python list with no variable assigned to it. Elements shall be string."
                    ),
                },
            ],
            temperature=1,
            stream=False,
            seed=50,
        )
        return completion.choices[0].message.content.lower()
