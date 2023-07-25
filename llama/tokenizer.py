# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

import os
from logging import getLogger
from typing import List

from sentencepiece import SentencePieceProcessor

# 这段代码实现了一个基于SentencePiece的Tokenizer类，用于将文本转换成一系列标记（tokens）的整数表示，并将整数表示转换回文本。
#
# 以下是Tokenizer类的主要功能解释：
#
# 1. `Tokenizer.__init__`: 这是Tokenizer类的构造函数。它接收一个模型文件的路径，并使用SentencePieceProcessor从模型文件加载SentencePiece模型。模型文件通常包含预训练的词汇表和模型参数。构造函数还初始化了一些参数，如词汇表大小（`n_words`）、BOS（Beginning of Sentence）和EOS（End of Sentence）标记的整数ID。
#
# 2. `Tokenizer.encode`: 这是将输入文本字符串转换为整数标记序列的方法。它接收一个字符串`s`，并根据参数`bos`（是否添加BOS标记）和`eos`（是否添加EOS标记）将字符串转换为整数标记列表。
#
# 3. `Tokenizer.decode`: 这是将整数标记序列转换回原始文本字符串的方法。它接收一个整数标记列表`t`，并将其解码为原始文本字符串。
#
# Tokenizer类的主要作用是将文本转换为适合输入Transformer模型的整数标记序列，并将模型的输出（整数标记序列）转换回文本。这对于将文本传递给Transformer模型进行处理以及解码生成的结果都是很有用的。

logger = getLogger()


class Tokenizer:
    def __init__(self, model_path: str):
        # reload tokenizer
        assert os.path.isfile(model_path), model_path
        self.sp_model = SentencePieceProcessor(model_file=model_path)
        logger.info(f"Reloaded SentencePiece model from {model_path}")

        # BOS / EOS token IDs
        self.n_words: int = self.sp_model.vocab_size()
        self.bos_id: int = self.sp_model.bos_id()
        self.eos_id: int = self.sp_model.eos_id()
        self.pad_id: int = self.sp_model.pad_id()
        logger.info(
            f"#words: {self.n_words} - BOS ID: {self.bos_id} - EOS ID: {self.eos_id}"
        )
        assert self.sp_model.vocab_size() == self.sp_model.get_piece_size()

    def encode(self, s: str, bos: bool, eos: bool) -> List[int]:
        assert type(s) is str
        t = self.sp_model.encode(s)
        if bos:
            t = [self.bos_id] + t
        if eos:
            t = t + [self.eos_id]
        return t

    def decode(self, t: List[int]) -> str:
        return self.sp_model.decode(t)
