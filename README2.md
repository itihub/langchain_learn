# 使用LangChain创建一个实例  

## 项目信息  
项目使用```pipenv```来管理依赖

首次初始化项目
```bash
pipenv install
```
进入虚拟环境 
```bash
pipenv shell
```
退出虚拟环境 
```bash
exit
```
安装依赖包 
```bash
pipenv install xxx
```
卸载依赖包 
```bash
pipenv uninstall xxx
```

项目已安装依赖：
- ```pipenv install jupyterlab```
- ```pipenv install langchain```
- ```pipenv install langchain_community```
- ```pipenv install langchain-openai```
- ```pip install openai```
- ```pip install google-generativeai```
- ```pip install python-dotenv```

1. 创建一个LLM  
- 自有算力平台+开源大模型（需要有庞大的GPU资源）
- 第三方大模型API (OpenAI/百度文心/阿里通义千问...)
- 让LLM给孩子起具有中国特色的名字

1. 自定义提词器模板
- 将提问上下文模块化
- 支持参数传入
- 让LLM给孩子起具有美国特殊的名字

1. 输出解释器
- 将LLM输出的结果各种格式化
- 支持类似JSON等结构化数据输出
- 让LLM给孩子起4个有中国特色的名字，并以数组格式输出而不是文本

1. 第一个实例
- 让LLM以人机对话的形式输出4个名字
- 名字和性别可以根据用户输出来相应输出
- 输出格式定义为数组