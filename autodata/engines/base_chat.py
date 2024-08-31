import logging
import json

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from openai import OpenAI
import os


class __BaseChat:
    def __init__(
        self,
        topic: str,
        threads: int,
        length: int,
        model: str,
        data_format: str,
        system_prompt: str,
    ):
        """
        The function takes the following arguments:-
        :param topic: The topic on which the chat is intended to be generated
        :param threads: The number of chats to be generated
        :param length: The value to indicate how long a chat session will be
        :param model: The Open AI model through which data will be generated
        :param data_format: The format in which the generated data will be presented
        """
        # Validation of variables
        assert length > 0, f"Length passed - {length} should be greater than 0"
        assert threads > 0, f"Threads passed - {threads} should be greater than 0"

        # Variable declaration
        self.CONVERSATION_LENGTH = length
        self.TOPIC = topic
        self.THREADS = threads
        self.MODEL = model
        self.FORMAT = data_format
        self.KEY = os.environ["OPENAI_API_KEY"]
        self.SYSTEM_PROMPT = system_prompt
        self.client = OpenAI(api_key=self.KEY, base_url=os.environ.get("OPENAI_API_BASE", None))

    def initiate_chat(self) -> str:
        """
        This function is responsible for fragmenting a particular topic into N number of chat topics which might occur
        is real life during a chat session on that topic
        :return: A Python list in the form of a string containing the different chat topics
        """
        completion = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
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

    def get_topic(self) -> list:
        """
        This function converts the list in string form to a valid list in python assigned to the variable chat_topic
        using the eval() function in python
        :return: A python list containing all chat topics
        """
        try:
            chat_topics = eval(self.initiate_chat())
            logging.info("The Chat Topic generated are: " + str(chat_topics))
            return chat_topics
        except:
            logging.exception(
                """The model was not able to produce a valid python list. 
                Try a different/better Open AI model. Below is the full error: """
            )
            raise Exception(
                """The model was not able to produce a valid python list. Try a different/better Open AI model. 
                Refer to the Log to view the full exception"""
            )

    def save_date(self, data: dict, path: str):
        """
        This function saves the chat history in the desired format
        :param path: the folder where the file is to be saved
        :param data: The Chat history
        """
        try:
            if self.FORMAT == "json":
                with open(f"./output/{self.TOPIC}_chat.json", "w") as json_file:
                    json.dump(data, json_file, indent=2)
                logging.info("Successfully saved the data as json")

            elif self.FORMAT == "parquet":
                df = pd.DataFrame(data)
                table = pa.Table.from_pandas(df=df, nthreads=2)

                parquet_file = f"{path}/{self.TOPIC}_chat.parquet"
                pq.write_table(table, parquet_file)
                logging.info("Successfully saved the data as parquet")
        except:
            logging.exception(
                f"""An error occurred while saving the data as {self.FORMAT}. Refer to the log 
            ./logs/engine.log for more information"""
            )
