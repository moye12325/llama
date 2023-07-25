# Llama 2

我们正在释放大型语言模型的力量。我们最新版本的Llama现在对所有个人、创作者、研究人员和企业开放，以便他们可以负责地进行实验、创新和扩展他们的想法。

这次发布包括预训练和微调的Llama语言模型的权重和起始代码，参数规模从7B到70B。

这个存储库旨在提供一个最小的例子，用于加载[Llama 2](https://ai.meta.com/research/publications/llama-2-open-foundation-and-fine-tuned-chat-models/)模型并进行推理。有关更详细的利用HuggingFace的示例，请参见[llama-recipes](https://github.com/facebookresearch/llama-recipes/)。

## 下载

⚠️ **7/18: 我们注意到今天有人遇到了许多下载问题。如果任何人仍然遇到问题，请删除所有本地文件，重新克隆存储库，并[请求新的下载链接](https://ai.meta.com/resources/models-and-libraries/llama-downloads/)。这是至关重要的，以防本地文件损坏。当您收到电子邮件时，只复制链接文本本身 - 它应该以https://download.llamameta.net开头，而不是以https://l.facebook.com开头，否则会出现错误。**

为了下载模型权重和分词器，请访问[Meta AI网站](https://ai.meta.com/resources/models-and-libraries/llama-downloads/)并接受我们的许可协议。

一旦您的请求被批准，您将收到一封带有签名的电子邮件URL。然后运行download.sh脚本，在提示时传递提供的URL以开始下载。确保直接复制URL文本本身，**不要使用'复制链接地址'选项**，右键单击URL时。如果复制的URL文本以：https://download.llamameta.net开头，那么您复制正确了。如果复制的URL文本以：https://l.facebook.com开头，那么您复制错误了。

先决条件：确保您已安装`wget`和`md5sum`。然后运行脚本：`./download.sh`。

请注意，链接在24小时内和一定数量的下载后会过期。如果出现`403: Forbidden`等错误，您可以随时重新请求链接。

### 在Hugging Face上访问

我们还在[Hugging Face](https://huggingface.co/meta-llama)上提供下载。您必须先使用与Hugging Face帐户相同的电子邮件地址从Meta AI网站请求下载。之后，您可以请求访问Hugging Face上的任何模型，您的帐户将在1-2天内获得访问所有版本的权限。

## 设置

在具有PyTorch / CUDA的conda环境中，克隆存储库并在顶层目录中运行：

```
pip install -e .
```

## 推理

不同的模型需要不同的模型并行（MP）值：

|  模型  | MP |
|--------|----|
| 7B     | 1  |
| 13B    | 2  |
| 70B    | 8  |

所有模型支持序列长度高达4096个标记，但我们根据`max_seq_len`和`max_batch_size`的值预先分配缓存。因此，请根据您的硬件设置这些值。

### 预训练模型

这些模型未进行聊天或问答的微调。必须对其进行提示，以便预期的答案是提示的自然延续。

请参见`example_text_completion.py`中的一些示例。为了说明，以下命令演示如何使用llama-2-7b模型运行它（`nproc_per_node`需要设置为`MP`值）：

```
torchrun --nproc_per_node 1 example_text_completion.py \
    --ckpt_dir llama-2-7b/ \
    --tokenizer_path tokenizer.model \
    --max_seq_len 128 --max_batch_size 4
```

### 微调的聊天模型

微调的模型用于对话应用。为了获得预期的特性和性能，需要遵循[`chat_completion`](https://github.com/facebookresearch/llama/blob/main/llama/generation.py#L212)中定义的特定格式，包括`INST`和`<<SYS>>`标签，`BOS`和`EOS`标记，以及它们之间的空格和换行符（我们建议在输入上调用`strip()`以避免双空格）。

您还可以为筛选认为不安全的输入和输出部署额外的分类器。请参阅llama-recipes repo中的[示例](https://github.com/facebookresearch/llama-recipes/blob/main/inference/inference.py)，了解如何将安全检查器添加到推理代码的输入和输出中。

使用llama-2-7b-chat的示例：

```
torchrun --nproc_per_node 1 example_chat_completion.py \
    --ckpt_dir llama-2-7b-chat/ \
    --tokenizer_path tokenizer.model \
    --max_seq_len 512 --max_batch_size 4
```

Llama 2是一项带有潜在风险的新技术。到目前为止进行的测试并不能覆盖所有情况。
为了帮助开发人员解决这些风险，我们创建了[Responsible Use Guide](Responsible-Use-Guide.pdf)。更多细节也可以在我们的研究论文中找到。

## 问题

请通过以下方式之一报告模型的任何软件“bug”或其他问题：
- 报告模型问题：[github.com/facebookresearch/llama](http://github.com/facebookresearch/llama)
- 报告模型生成的风险内容：[developers

.facebook.com/llama_output_feedback](http://developers.facebook.com/llama_output_feedback)
- 报告错误和安全问题：[facebook.com/whitehat/info](http://facebook.com/whitehat/info)

## 模型卡片

请参阅[MODEL_CARD.md](MODEL_CARD.md)。

## 许可证

我们的模型和权重面向研究人员和商业实体授权，秉承开放原则。我们的使命是通过这个机会赋予个人和行业权力，同时培育发现和道德人工智能进步的环境。

请参阅[LICENSE](LICENSE)文件，以及我们的附带[接受使用政策](USE_POLICY.md)。

## 参考资料

1. [研究论文](https://ai.meta.com/research/publications/llama-2-open-foundation-and-fine-tuned-chat-models/)
2. [Llama 2技术概述](https://ai.meta.com/resources/models-and-libraries/llama)
3. [开放创新AI研究社区](https://ai.meta.com/llama/open-innovation-ai-research-community/)

## 原始的LLaMA

原始llama发布的存储库位于[`llama_v1`](https://github.com/facebookresearch/llama/tree/llama_v1)分支中。