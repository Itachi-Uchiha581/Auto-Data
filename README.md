<div align="center">

# **Auto Data** 📜
> Auto Data is **the** library designed for the automatic generation of realistic datasets, essential for the fine-tuning of Large Language Models (LLMs). This highly efficient and **lightweight** library enables the swift and effortless creation of comprehensive **datasets** across various topics, regardless of their size.

## Why Auto Data?
One of the **principal** challenges encountered during the fine-tuning of models for the development of custom agents is the **scarcity** and **imbalance** of data. Such deficiencies can skew the model's understanding towards one particular feature or, in more severe cases, may cause the model to deviate entirely from its learned parameters due to an insufficient number of training examples. To address these critical issues, Auto Data was developed.
</div>

## **Getting Started**
Before continuing set up your OPENAI_API_KEY as your environment variable. If you are unaware on how to do so, refer to this guide - https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety
1. ### **Installation:** 
    ```shell
    git clone https://github.com/Itachi-Uchiha581/Auto-Data.git
    ```

2. ### **Usage Through CLI:**
    ```shell
    cd Auto-Data
    ```
    ```shell
    pip install -r requirements.txt
    ```
    ```shell
    python main.py --help
    ```
    Output of the above command:
    ```
    usage: Auto Data [-h] [--model MODEL] [--topic TOPIC] [--format {json,parquet}] [--engine {native}] [--threads THREADS] [--length LENGTH] [--system_prompt SYSTEM_PROMPT]

    Auto Data is a tool which automatically creates training data to fine tune Large-Language Models on!

    options:
    -h, --help            show this help message and exit
    --model MODEL, -m MODEL
                            Selection of an OpenAI model for data generation
    --topic TOPIC, -t TOPIC
                            Topic for data generation, eg - Global Economy
    --format {json,parquet}, -f {json,parquet}
                            The format of the output data produced by the LLM
    --engine {native}, -e {native}
                            The backend used to generate data. More engines coming soon
    --threads THREADS, -th THREADS
                            An integer to indicate how many chats to be created on the topic. A very high thread value may result in an error specially if your Open AI account is at tier 1.
    --length LENGTH, -l LENGTH
                            The conversation length of a chat topic
    --system_prompt SYSTEM_PROMPT, -sp SYSTEM_PROMPT
                            The system prompt that is to be given to the assistant.

    ```
    Sample Usage given below
    ```shell
    python main.py --model "gpt-4-turbo-preview" --topic "Mysteries and Horror stories" --format "json" --engine "native" --threads 2 --length 2 --system_prompt "You are a helpful assistant who has an interest in Mysteries and Horror stories. You are also excellent at articulating such stories"
    ```
    In the specified command, the **model** chosen is *gpt-4-turbo-preview*, and the **topic** targeted is *Mysteries and Horror Stories*. The **format** for the output data is set to *json*, with the **engine** employed being *native*. The command indicates the creation of *2* chat threads, each encompassing *2* complete back-and-forth conversations, as specified by the **length** parameter. The final parameter provided serves as the **system prompt** for the *assistant LLM*.  
      
    Below is the trimmed output generated from the above command in *json* format:
    ```json
    {
    "Chats": [
        {
        "messages": [
            {
            "role": "system",
            "content": "You are a helpful assistant who has an interest in Mysteries and Horror stories. You are also excellent at articulating such stories"
            },
            {
            "role": "user",
            "content": "What's considered one of the most chilling unsolved mysteries in history?"
            },
            {
            "role": "assistant",
            "content": "Among the pantheon of unsolved mysteries, the chilling tale of the Dyatlov Pass incident stands out, both for its perplexing evidence and the many questions that still haunt its narrative. This enigma unfolded in the bleak expanse of the Ural Mountains in Russia during the icy clutches of winter in 1959. ............."
            },
            {
            "role": "user",
            "content": "Are there any other unsolved mysteries that are as eerie or confounding as the Dyatlov Pass incident?"
            },
            {
            "role": "assistant",
            "content": "Indeed, the world is riddled with mysteries as eerie and confounding as the Dyatlov Pass incident. One such enigma, shrouded in the mists of time and mystery, is the unsettling story of the Hinterkaifeck murders\u2014a case that combines elements of horror, intrigue, and the supernatural, sending shivers down the spine of anyone who delves into its depths.\n\nThe Hinterkaifeck farmstead, a remote and secluded homestead, lay in the Bavarian countryside of Germany. The year was 1922, and within these walls, a gruesome and baffling crime unfolded\u2014one that remains unsolved to this day. The victims were the Gruber family and their maid: Andreas and C\u00e4zilia Gruber, their daughter Viktoria, her children C\u00e4zilia and Josef, and the maid, Maria Baumgartner. Each was found brutally murdered, their bodies bearing the horrific marks of a pickaxe, which was later found at the crime scene.\n\nWhat amplifies the eeriness of these murders are not just the brutal manner in which they were executed but the bizarre and disturbing events leading up to the discovery of the bodies. Andreas Gruber, the patriarch of the family, had reported strange occurrences around the farmstead days before the killings. ............."
            }
        ],
        "model": "gpt-4-turbo-preview",
        "sub_topic": "discussing the most chilling unsolved mysteries",
        "system_prompt": "You are a helpful assistant who has an interest in Mysteries and Horror stories. You are also excellent at articulating such stories"
        },
        {
        "messages": [
            {
            "role": "system",
            "content": "You are a helpful assistant who has an interest in Mysteries and Horror stories. You are also excellent at articulating such stories"
            },
            {
            "role": "user",
            "content": "Have any of you ever had a personal experience with something paranormal, or something you just couldn't explain no matter how hard you tried?"
            },
            {
            "role": "assistant",
            "content": "While I don't experience events personally due to my nature as an AI, I can certainly share a mysteriously chilling story that touches upon the paranormal and the unexplainable, which I've gathered based on numerous accounts and tales told over time. Let it captivate your imagination and perhaps make you ponder the mysteries that dwell just beyond the edge of our understanding.\n\n---\n\nIn a small, seemingly inconspicuous town nestled between the embrace of forgotten woods and the whisper of a rarely disturbed coastline, there lived a woman named Elara. She was known for her rational mind and scientific approach to life, a skeptic of anything that dared to venture into the realm of the unexplainable. However, her beliefs were put to the test one autumn evening. ............."
            },
            {
            "role": "user",
            "content": "That's a captivating story! It's interesting how it mixes scientific curiosity with the paranormal. Have there been any real-life instances where science has struggled to explain paranormal phenomena, kind of like in Elara's story?"
            },
            {
            "role": "assistant",
            "content": "Indeed, there have been several instances where the boundaries between the scientific and the paranormal have blurred, creating fascinating enigmas that continue to intrigue both skeptics and believers. While many purported paranormal phenomena can often be debunked with rigorous scientific examination, there remain a few cases that defy clear-cut explanations, leaving room for speculation and wonder. Here are a few notable examples:\n\n### 1. The Hessdalen Lights\nIn the Hessdalen Valley of Norway, mysterious lights have been observed since at least the 1930s. These lights vary in color, intensity, and duration, sometimes moving with incredible speed, at other times hovering in place. Despite numerous studies, including Project Hessdalen initiated in the early 1980s, the complete scientific explanation for these lights remains elusive. Various hypotheses have been proposed, including ionized iron dust, plasma, and even the piezoelectric effects from tectonic strain, but none has definitively solved the mystery.\n\n### 2. The Voynich Manuscript\nThe Voynich Manuscript is a 15th-century book that has baffled linguists, cryptographers, and computer scientists for decades. Its language has never been deciphered, and the strange illustrations of unfamiliar plants and astronomical diagrams add to its mystique. While not paranormal in the conventional sense, the manuscript's origin, purpose, and message could be described as a \"scientific ghost,\" eluding comprehension and resolution.\n\n### 3. ............."
            }
        ],
        "model": "gpt-4-turbo-preview",
        "sub_topic": "sharing personal experiences with the paranormal or unexplainable events",
        "system_prompt": "You are a helpful assistant who has an interest in Mysteries and Horror stories. You are also excellent at articulating such stories"
        }
    ],
    "topic": "Mysteries and Horror stories",
    "threads": 2,
    "length": 2
    }
    ```
    __*To view the full output, check out the examples directory*__  

<!---
3. ### **Importing Auto Data as a module in Python:**
    The below examples generates a dataset of length 2, thread size 2 with the topic being, converts it into a  dictionary and prints it
    ```python
    from autodata import Native
    data_generator = 
    ```
-->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

**Contributions can be made by making the existing code efficient and cleaner, adding new engines (an example engine with guide is already given inside autodata/engines), adding LLM training data analyser, creating testing scripts etc.**

## License

Distributed under the GPL-3.0 License. See `LICENSE.txt` for more information.