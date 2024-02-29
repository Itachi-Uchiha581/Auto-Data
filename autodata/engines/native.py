from threading import Thread
import json
import logging

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pyfiglet import Figlet
from tenacity import stop_after_attempt, wait_random_exponential, retry

from autodata.utils.loading_bar import LoadingBar
from autodata.utils.text_colour import TextColor
from autodata.data_structures.chat_history import ChatHistory
from autodata.data_structures.topic_history import TopicHistory
from autodata.engines.base_chat import __BaseChat

logging.basicConfig(
    level=logging.INFO,
    filename=r"logs/engine.log",
    filemode="w",
    encoding="utf-8",
    format="%(filename)s , %(funcName)s , %(lineno)d , %(levelname)s , %(message)s",
)


class Native(__BaseChat):
    def __init__(
        self,
        topic: str,
        threads: int,
        length: int,
        key: str,
        model: str,
        data_format: str,
        system_prompt: str,
    ):
        super().__init__(topic, threads, length, key, model, data_format, system_prompt)
        self.chat_history = []

    def __get_topic(self) -> list:
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

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def __user_proxy_agent(self, history_user) -> str:
        """
        This function using the gpt-4-turbo-preview model generates questions/queries like the user in a conversation
        :param history_user: This is the history of messages in the "perspective" of a user
        :return: The user query/question is returned
        """
        completion = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=history_user,
            temperature=0.75,
            stream=False,
        )
        user_reply = completion.choices[0].message.content
        logging.info("The user generated question:- " + str(user_reply))
        return user_reply

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def __assistant_proxy_agent(self, history_assistant) -> str:
        """
        This function using a model given, generates responses for the user queries
        :param history_assistant: This is the history of messages in the "perspective" of an assistant
        :return: the assistant's reply is returned
        """
        completion = self.client.chat.completions.create(
            model=self.MODEL, messages=history_assistant, temperature=1, stream=False
        )
        return completion.choices[0].message.content

    def __chat_manager(self, topic):
        """
        This function acts as the manager between the user and the assistant. It passes the queries of the user llm
        to the assistant llm.
        :param topic: The topic on which the fragmented chat topics were generated
        :return: It returns the whole chat history between the user and the assistant
        """
        # if nothing works fix the prompt given as last hope
        history_user = [
            {
                "role": "system",
                "content": (
                    "You are a human designed to ask questions on specific topics. You ask questions from the "
                    "perspective of a human or a user of the AI assistant. You never answer as an assistant."
                    "You not only ask question but you behave like one as well by using human expressions "
                    "like thanks, can you please explain, etc. You always produce a question"
                ),
            },
            {
                "role": "user",
                "content": (
                    "The following is a conversation with an AI assistant. "
                    f"The humans asks intuitive and pragmatic questions on the topic - {topic}. "
                    "Your job is to produce questions from the perspective of a human now, Human:"
                ),
            },
        ]
        history_assistant = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        for i in range(0, self.CONVERSATION_LENGTH):
            input_string = self.__user_proxy_agent(history_user)
            if "Human:" in input_string:
                human_index = input_string.find("Human:")

                # Extract the text after "Human:"
                input_string = input_string[human_index + len("Human:") :].strip()
                logging.info("Formatted the user's (bot) question")

            history_user.append(
                {"role": "assistant", "content": "Human:" + str(input_string)}
            )

            history_assistant.append(
                {
                    "role": "user",
                    "content": f"{input_string}",
                }
            )

            assistant_reply = self.__assistant_proxy_agent(history_assistant)
            logging.info("Attained the Assistants reply")
            history_user.append(
                {
                    "role": "user",
                    "content": f"Assistant{assistant_reply}",
                }
            )
            history_assistant.append(
                {"role": "assistant", "content": str(assistant_reply)}
            )

        self.chat_history.append(
            ChatHistory(
                messages=history_assistant,
                model=self.MODEL,
                sub_topic=topic,
                system_prompt=self.SYSTEM_PROMPT,
            )
        )

    def __save_date(self, data):
        """
        This function saves the chat history in the desired format
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

                parquet_file = f"./output/{self.TOPIC}_chat.parquet"
                pq.write_table(table, parquet_file)
                logging.info("Successfully saved the data as parquet")
        except:
            logging.exception(
                f"""An error occurred while saving the data as {self.FORMAT}. Refer to the log 
            ./logs/engine.log for more information"""
            )

    def __compiler(self) -> TopicHistory:
        """
        This function calls the chat_manager through the collector asynchronously to improve speed
        :return: The organised and cleaned chat history
        """
        threads = []
        chat_complete = 0
        print(
            TextColor.CYAN + f"Generating Chats on '{self.TOPIC}'" + TextColor.RESET,
            "\n",
        )
        LoadingBar.loading_bar(chat_complete, self.THREADS)
        for topic in self.__get_topic():
            threads.append(Thread(target=self.__chat_manager, args=[topic]))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
            chat_complete += 1
            LoadingBar.loading_bar(chat_complete, self.THREADS)
        print()
        print(
            TextColor.GREEN + "All Chats Successfully created!" + TextColor.RESET,
            "\n",
            TextColor.MAGENTA
            + f"Saving Chats as {self.FORMAT}. Checkout the output directory to view the generated chats."
            + TextColor.RESET,
        )

        return TopicHistory(
            Chats=self.chat_history,
            topic=self.TOPIC,
            threads=self.THREADS,
            length=self.CONVERSATION_LENGTH,
        )

    def __call__(self) -> TopicHistory:
        """
        :return: The Topic History Data object
        """
        text_obj = Figlet("dos_rebel", width=200)
        print("\n", text_obj.renderText("Auto Data"))
        data_chats = self.__compiler()
        self.__save_date(data_chats.to_dict())
        return data_chats