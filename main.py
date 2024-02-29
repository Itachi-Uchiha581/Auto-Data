import argparse
import os

from autodata.utils.text_colour import TextColor
from autodata import Native


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Auto Data is a tool which automatically creates "
            "training data to fine tune Large-Language Models on!"
        ),
        prog="Auto Data",
    )
    parser.add_argument(
        "--model", "-m", help="Selection of an OpenAI model for data generation"
    )
    parser.add_argument(
        "--topic", "-t", help="Topic for data generation, eg - Global Economy"
    )
    parser.add_argument(
        "--format",
        "-f",
        type=str,
        help="The format of the output data produced by the LLM",
        choices=["json", "parquet"],
    )
    parser.add_argument(
        "--engine",
        "-e",
        type=str,
        help="The backend used to generate data. More engines coming soon",
        choices=["native"],
    )
    parser.add_argument(
        "--threads",
        "-th",
        type=int,
        help="""An integer to indicate how many chats to be created on the topic.
        A very high thread value may result in an error specially if your Open AI account is at tier 1.""",
    )
    parser.add_argument(
        "--length",
        "-l",
        type=int,
        help="The conversation length of a chat topic",
    )
    parser.add_argument(
        "--system_prompt",
        "-sp",
        type=str,
        help="The system prompt that is to be given to the assistant.",
    )
    args = parser.parse_args()
    try:
        key = os.environ["OPENAI_API_KEY"]
    except:
        raise Exception(
            """No Open AI Api Key was found in the environment variables. To set it up refer - 
            https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety """
        )
    if args.engine == "native":
        data_generator = Native(
            args.topic,
            args.threads,
            args.length,
            key,
            args.model,
            args.format,
            args.system_prompt,
        )

        print(TextColor.YELLOW + str(data_generator()) + TextColor.RESET)


if __name__ == "__main__":
    main()
