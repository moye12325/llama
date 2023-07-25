#!/bin/bash

# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.


#总体而言，这段代码的功能是通过wget命令从指定URL下载Llama 2模型文件和tokenizer，并检查文件完整性。下载的文件将保存在指定的目标文件夹中。

#1. `read -p "Enter the URL from email: " PRESIGNED_URL`: 提示用户输入从电子邮件中获得的URL，并将其存储在变量PRESIGNED_URL中。
read -p "Enter the URL from email: " PRESIGNED_URL
echo ""

#2. `read -p "Enter the list of models to download without spaces (7B,13B,70B,7B-chat,13B-chat,70B-chat), or press Enter for all: " MODEL_SIZE`: 提示用户输入要下载的模型的列表（如果有多个模型）。如果用户按下Enter键，则默认下载全部模型。用户输入的模型列表将存储在变量MODEL_SIZE中。
read -p "Enter the list of models to download without spaces (7B,13B,70B,7B-chat,13B-chat,70B-chat), or press Enter for all: " MODEL_SIZE

#3. `TARGET_FOLDER="."`: 定义目标文件夹的路径，这里设置为当前目录。
TARGET_FOLDER="."             # where all files should end up

#4. `mkdir -p ${TARGET_FOLDER}`: 创建目标文件夹（如果不存在）。
mkdir -p ${TARGET_FOLDER}

#5. `if [[ $MODEL_SIZE == "" ]]; then ...`: 如果用户没有指定要下载的模型列表，则将模型列表设置为所有模型（7B、13B、70B、7B-chat、13B-chat和70B-chat）。
if [[ $MODEL_SIZE == "" ]]; then
    MODEL_SIZE="7B,13B,70B,7B-chat,13B-chat,70B-chat"
fi

#6. `echo "Downloading LICENSE and Acceptable Usage Policy"`: 打印下载许可证和可接受使用政策的提示信息。
echo "Downloading LICENSE and Acceptable Usage Policy"

#7. `wget ${PRESIGNED_URL/'*'/"LICENSE"} -O ${TARGET_FOLDER}"/LICENSE"`: 使用wget命令下载LICENSE文件，并将其保存到目标文件夹。
wget ${PRESIGNED_URL/'*'/"LICENSE"} -O ${TARGET_FOLDER}"/LICENSE"

#8. `wget ${PRESIGNED_URL/'*'/"USE_POLICY.md"} -O ${TARGET_FOLDER}"/USE_POLICY.md"`: 使用wget命令下载USE_POLICY.md文件，并将其保存到目标文件夹。
wget ${PRESIGNED_URL/'*'/"USE_POLICY.md"} -O ${TARGET_FOLDER}"/USE_POLICY.md"

#9. `echo "Downloading tokenizer"`: 打印下载tokenizer的提示信息。
echo "Downloading tokenizer"

#10. `wget ${PRESIGNED_URL/'*'/"tokenizer.model"} -O ${TARGET_FOLDER}"/tokenizer.model"`: 使用wget命令下载tokenizer.model文件，并将其保存到目标文件夹。
wget ${PRESIGNED_URL/'*'/"tokenizer.model"} -O ${TARGET_FOLDER}"/tokenizer.model"

#11. `wget ${PRESIGNED_URL/'*'/"tokenizer_checklist.chk"} -O ${TARGET_FOLDER}"/tokenizer_checklist.chk"`: 使用wget命令下载tokenizer_checklist.chk文件，并将其保存到目标文件夹。
#12. `(cd ${TARGET_FOLDER} && md5sum -c tokenizer_checklist.chk)`: 使用md5sum命令检查下载的tokenizer文件的完整性。
wget ${PRESIGNED_URL/'*'/"tokenizer_checklist.chk"} -O ${TARGET_FOLDER}"/tokenizer_checklist.chk"
(cd ${TARGET_FOLDER} && md5sum -c tokenizer_checklist.chk)



#13. `for m in ${MODEL_SIZE//,/ }`: 遍历模型列表。
#14. 在循环中，根据模型的大小（7B、13B、70B、7B-chat、13B-chat和70B-chat），设置相应的SHARD（用于构建下载URL）和MODEL_PATH（用于保存模型文件的文件夹路径）。

for m in ${MODEL_SIZE//,/ }
do
    if [[ $m == "7B" ]]; then
        SHARD=0
        MODEL_PATH="llama-2-7b"
    elif [[ $m == "7B-chat" ]]; then
        SHARD=0
        MODEL_PATH="llama-2-7b-chat"
    elif [[ $m == "13B" ]]; then
        SHARD=1
        MODEL_PATH="llama-2-13b"
    elif [[ $m == "13B-chat" ]]; then
        SHARD=1
        MODEL_PATH="llama-2-13b-chat"
    elif [[ $m == "70B" ]]; then
        SHARD=7
        MODEL_PATH="llama-2-70b"
    elif [[ $m == "70B-chat" ]]; then
        SHARD=7
        MODEL_PATH="llama-2-70b-chat"
    fi


#15. 在循环中，使用wget命令下载相应的模型文件，并将其保存到目标文件夹。

#16. 在循环中，使用md5sum命令检查下载的模型文件的完整性。
#
    echo "Downloading ${MODEL_PATH}"
    mkdir -p ${TARGET_FOLDER}"/${MODEL_PATH}"

    for s in $(seq -f "0%g" 0 ${SHARD})
    do
        wget ${PRESIGNED_URL/'*'/"${MODEL_PATH}/consolidated.${s}.pth"} -O ${TARGET_FOLDER}"/${MODEL_PATH}/consolidated.${s}.pth"
    done

    wget ${PRESIGNED_URL/'*'/"${MODEL_PATH}/params.json"} -O ${TARGET_FOLDER}"/${MODEL_PATH}/params.json"
    wget ${PRESIGNED_URL/'*'/"${MODEL_PATH}/checklist.chk"} -O ${TARGET_FOLDER}"/${MODEL_PATH}/checklist.chk"
    echo "Checking checksums"
    (cd ${TARGET_FOLDER}"/${MODEL_PATH}" && md5sum -c checklist.chk)
done

