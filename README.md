# Mcp-ChatBI 

## 介绍

 基于 [Mcp](https://mcp-docs.cn/) 架构的 ChatBI，是一种数据分析智能体的解决方案。

本项目主要解决ChatBI常见的三个问题
 + 1、如何保障数据的100%的准确性？

    由于模型存在幻觉，无论是NL2SQL、NL2Code，都无法保障数据100%的准确。且数据的准确性又是BI系统的红线，因此，本项目使用NL2Tools的方案，Tools可以是Headless BI的服务，也可是API。

+  2、一次对话如何查询多个指标？

   过去一次对话只能查一个指标，若多个指标需要工程层面去拆解，架构的复杂度非常高，本项目，利用模型的任务规划、推理能力，模型自动拆解多个指标，并按照顺序调用Tools，并返回结果。

+ 3、如何让数据分析的链路自动化？

   常见的数据分析方法，如对比分析、多维钻取、归因运算等，它常常伴有复杂的逻辑推理，当前大模型能力突飞猛进，已经具有复杂问题的推理能力，因此，本项目，利用模型推理能力，自动生成数据链路，并逐次调用Tools，返回结果，最后总结分析。


## 部署

### 1. 环境配置

+ 确保你的机器安装了 Python 3.10 - 3.12
```shell
# 拉取仓库
$ git clone https://github.com/dynamiclu/Mcp-ChatBI.git

# 进入目录
$ cd Mcp-ChatBI

# 安装全部依赖
$ pip3 install -r requirements.txt 
```

+ 大模型配置
```shell
$ vim config/config.toml
[model]
qwen_api_key = "sk-**********"
qwen_model_name = "qwen-max"
```

### 2. 启动接口
```shell
# 启动API
$ python3 main-api.py
```

### 3. 启动Gradio
```shell
# 启动Gradio
$ python3 main-webui.py
```
### 4. 演示
[https://www.bilibili.com/video/BV1b95vzPEjf/](https://www.bilibili.com/video/BV1b95vzPEjf/)