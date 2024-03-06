import argparse

from pyfiglet import Figlet
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
        "--model",
        "-m",
        help="Selection of an OpenAI model for data generation",
        default="gpt-4-turbo-preview",
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
        default="json",
    )
    parser.add_argument(
        "--engine",
        "-e",
        type=str,
        help="The backend used to generate data. More engines coming soon",
        choices=["native"],
        default="native",
    )
    parser.add_argument(
        "--threads",
        "-th",
        type=int,
        help="""An integer to indicate how many chats to be created on the topic.
        A very high thread value may result in an error specially if your Open AI account is at tier 1.""",
        default=1,
    )
    parser.add_argument(
        "--length",
        "-l",
        type=int,
        help="The conversation length of a chat topic",
        default=1,
    )
    parser.add_argument(
        "--system_prompt",
        "-sp",
        type=str,
        help="The system prompt that is to be given to the assistant.",
        default="You are a helpful assistant.",
    )
    args = parser.parse_args()

    if args.engine == "native":
        text_obj = Figlet("dos_rebel", width=200)
        print("\n", text_obj.renderText("Auto Data"))
        data_generator = Native(
            args.topic,
            args.threads,
            args.length,
            args.model,
            args.format,
            args.system_prompt,
        )

        print(TextColor.YELLOW + str(data_generator("./output")) + TextColor.RESET)


if __name__ == "__main__":
    main()
