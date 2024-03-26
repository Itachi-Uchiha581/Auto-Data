from threading import Thread
import logging

from autodata.utils.loading_bar import LoadingBar
from autodata.utils.text_colour import TextColor
from autodata.data_structures.chat_history import ChatHistory
from autodata.data_structures.topic_history import TopicHistory
from autodata.engines.base_chat import __BaseChat
import os

if not os.path.exists("logs"):
    os.makedirs("logs")
logging.basicConfig(
    level=logging.INFO,
    filename=r"./logs/native.log",
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
        model: str,
        data_format: str,
        system_prompt: str,
    ):
        super().__init__(topic, threads, length, model, data_format, system_prompt)
        self.chat_history = []

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
                    "Imagine yourself as a human, deeply curious about a wide range of topics. "
                    "Your role is to frame questions from a human or user perspective, engaging in a "
                    "dialogue with an AI assistant. Your interactions should closely mimic human conversation styles, "
                    'including expressions of gratitude (e.g., "thanks"), polite requests for information '
                    '(e.g., "can you please explain"), and other conversational nuances typical among humans. '
                    "Your objective is to inquire, not to provide answers or guidance. "
                    "Therefore, avoid any language or phrases that position you as an assistant or a source of "
                    'information (e.g., "I am here to assist you" or "Please ask any questions"). '
                    "Your essence is encapsulated in your curiosity and "
                    "your ability to engage in a genuinely human manner."
                    "You only output your question and nothing else."
                    "If no further questions can be formed on the topic,you can ask questions in related fields as well"
                    "."
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
                    "content": f"Assistant:{assistant_reply}",
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
        for topic in self.get_topic():
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

    def __call__(self, path) -> TopicHistory:
        """
        :return: The Topic History Data object
        """
        data_chats = self.__compiler()
        self.save_date(data_chats.to_dict(), path)
        return data_chats
