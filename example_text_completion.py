# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.


# 1. `import fire`: 导入fire库，该库用于将命令行参数转化为函数参数。
#
# 2. `def main(...):`: 定义主函数main，用于进行文本生成。函数的参数包括：
#    - `ckpt_dir`: 指定Llama 2模型的文件夹路径。
#    - `tokenizer_path`: 指定tokenizer文件的路径。
#    - `temperature`: 生成文本的温度参数，用于控制生成文本的随机性，默认值为0.6。
#    - `top_p`: 用于Nucleus Sampling（Top-p Sampling）的p参数，默认值为0.9。
#    - `max_seq_len`: 输入的文本序列的最大长度，默认值为128。
#    - `max_gen_len`: 生成文本的最大长度，默认值为64。
#    - `max_batch_size`: 生成文本的最大批次大小，默认值为4。
#
# 3. `generator = Llama.build(...)`：使用Llama类的build方法创建一个生成器(generator)对象。该生成器将使用指定的模型和tokenizer。
#
# 4. `prompts = [...]`: 定义一组文本生成的示例，每个示例是一个字符串表示的文本生成提示。
#
# 5. `results = generator.text_completion(...)`: 使用生成器对象对文本生成示例进行生成。text_completion方法接受文本生成示例列表以及生成相关的参数（如温度、p值等），并返回生成的文本结果。
#
# 6. `for prompt, result in zip(prompts, results):`: 使用zip函数将文本生成示例和生成结果列表进行匹配，以便遍历每个示例及其生成结果。
#
# 7. 在循环中，首先输出每个文本生成示例的内容，然后输出生成的回复文本。
#
# 8. `if __name__ == "__main__": fire.Fire(main)`: 当脚本作为主程序运行时，调用fire库的Fire方法将命令行参数传递给main函数，实现文本生成的功能。
#
# 总体而言，这段代码的功能是使用Llama 2模型对给定的文本生成示例进行文本生成，并输出生成的文本结果。生成的结果将包含对每个文本生成示例的回复文本，以及对整个示例的生成结果。

import fire

from llama import Llama


def main(
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 128,
    max_gen_len: int = 64,
    max_batch_size: int = 4,
):
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    prompts = [
        # For these prompts, the expected answer is the natural continuation of the prompt
        "I believe the meaning of life is",
        "Simply put, the theory of relativity states that ",
        """A brief message congratulating the team on the launch:

        Hi everyone,
        
        I just """,
        # Few shot prompt (providing a few examples before asking model to complete more);
        """Translate English to French:
        
        sea otter => loutre de mer
        peppermint => menthe poivrée
        plush girafe => girafe peluche
        cheese =>""",
    ]
    results = generator.text_completion(
        prompts,
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )
    for prompt, result in zip(prompts, results):
        print(prompt)
        print(f"> {result['generation']}")
        print("\n==================================\n")


if __name__ == "__main__":
    fire.Fire(main)
