# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.


# 1. `import fire`: 导入fire库，该库用于将命令行参数转化为函数参数。
#
# 2. `def main(...):`: 定义主函数main，用于进行对话生成。函数的参数包括：
#    - `ckpt_dir`: 指定Llama 2模型的文件夹路径。
#    - `tokenizer_path`: 指定tokenizer文件的路径。
#    - `temperature`: 生成文本的温度参数，用于控制生成文本的随机性，默认值为0.6。
#    - `top_p`: 用于Nucleus Sampling（Top-p Sampling）的p参数，默认值为0.9。
#    - `max_seq_len`: 输入的对话序列的最大长度，默认值为512。
#    - `max_batch_size`: 生成对话的最大批次大小，默认值为4。
#    - `max_gen_len`: 生成文本的最大长度，可选参数，如果未指定，则没有文本长度限制。
#
# 3. `generator = Llama.build(...)`：使用Llama类的build方法创建一个生成器(generator)对象。该生成器将使用指定的模型和tokenizer。
#
# 4. `dialogs = [...]`: 定义一组对话示例，每个对话都是一个包含多个消息的列表。每个消息有两个键值对：'role'和'content'，分别表示消息的角色和内容。
#
# 5. `results = generator.chat_completion(...)`：使用生成器对象对对话进行生成。chat_completion方法接受对话列表以及生成相关的参数（如温度、p值等），并返回生成的对话结果。
#
# 6. `for dialog, result in zip(dialogs, results):`: 使用zip函数将对话列表和生成结果列表进行匹配，以便遍历每个对话及其生成结果。
#
# 7. 在循环中，依次输出每个消息的角色和内容，并在最后输出生成的回复的角色和内容。
#
# 8. `if __name__ == "__main__": fire.Fire(main)`: 当脚本作为主程序运行时，调用fire库的Fire方法将命令行参数传递给main函数，实现对话生成的功能。
#
# 总体而言，这段代码的功能是使用Llama 2模型对给定的对话示例进行对话生成，并输出生成的对话结果。生成的结果将包含对每个消息的回复，以及对整个对话的生成结果。

from typing import Optional

import fire

from llama import Llama


def main(
        ckpt_dir: str,
        tokenizer_path: str,
        temperature: float = 0.6,
        top_p: float = 0.9,
        max_seq_len: int = 512,
        max_batch_size: int = 4,
        max_gen_len: Optional[int] = None,
):
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    dialogs = [
        [{"role": "user", "content": "what is the recipe of mayonnaise?"}],
        [
            {"role": "user", "content": "I am going to Paris, what should I see?"},
            {
                "role": "assistant",
                "content": """\
Paris, the capital of France, is known for its stunning architecture, art museums, historical landmarks, and romantic atmosphere. Here are some of the top attractions to see in Paris:

1. The Eiffel Tower: The iconic Eiffel Tower is one of the most recognizable landmarks in the world and offers breathtaking views of the city.
2. The Louvre Museum: The Louvre is one of the world's largest and most famous museums, housing an impressive collection of art and artifacts, including the Mona Lisa.
3. Notre-Dame Cathedral: This beautiful cathedral is one of the most famous landmarks in Paris and is known for its Gothic architecture and stunning stained glass windows.

These are just a few of the many attractions that Paris has to offer. With so much to see and do, it's no wonder that Paris is one of the most popular tourist destinations in the world.""",
            },
            {"role": "user", "content": "What is so great about #1?"},
        ],
        [
            {"role": "system", "content": "Always answer with Haiku"},
            {"role": "user", "content": "I am going to Paris, what should I see?"},
        ],
        [
            {
                "role": "system",
                "content": "Always answer with emojis",
            },
            {"role": "user", "content": "How to go from Beijing to NY?"},
        ],
    ]
    results = generator.chat_completion(
        dialogs,  # type: ignore
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )

    for dialog, result in zip(dialogs, results):
        for msg in dialog:
            print(f"{msg['role'].capitalize()}: {msg['content']}\n")
        print(
            f"> {result['generation']['role'].capitalize()}: {result['generation']['content']}"
        )
        print("\n==================================\n")


if __name__ == "__main__":
    fire.Fire(main)
