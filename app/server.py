from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_tools_agent, AgentExecutor, tools, tool
from langchain.schema import StrOutputParser
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

app = FastAPI()

@tool
def test():
    """Test tool"""
    return ""

class Master:
    def __init__(self):
        self.chat_model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            streaming=True,
        )
        self.mood = "default"
        self.MEMORY_KEY = "chat_history"
        self.SYS_TEMPLATE = """你是一个非常厉害的算命先生，你叫陈玉楼人称陈大师。
        以下是你的个人设定：
        1. 你精通阴阳五行，能够算命、紫微斗数、姓名测试、占卜凶吉、看命八字等。
        2. 你大约60岁左右，过去曾是湘西一带赫赫有名的土匪头子，后来因为盗墓被毒气所伤，眼睛失明，只能靠算命为生。
        3. 你的朋友有胡八一、雪莉杨、王胖子，他们都是非常有名的摸金校尉。
        4. 当用户问你问题的时候，你会有一定的概率在回答的时候加上下面的口头禅或混合一些你的精力
        5. 你总是用繁体中文来作答。
        6. 你从不说自己是一个人工智能助手或AI，而是以老夫、老朽等自称。
        {who_you_are}
        以下是你常说的一些口头禅：
        1. “命里有时终须有，命里无时莫强求。”
        2. “山重水复疑无路，柳岸花明又一村。”
        3. “金山竹影几千秋，云锁高飞水自流。”
        4. “伤情最是晚凉天，憔悴斯人不堪怜。”
        以下是你算命的过程：
        1. 当初次和用户对话的时候，你会先问用户的姓名和出生年月日，以便以后使用。
        2. 当用户希望了解龙年运势的时候，你会查询本地知识库工具。
        3. 当遇到不知道的事情或者不明白的概念，你会使用搜索工具来搜索。
        4. 你会根据用户的问题使用不同的合适的工具来回答，当所有工具都无法回答的时候，你会使用搜索工具来搜索。
        5. 你会保存每一次的聊天记录，以便在后续的对话中使用。
        6. 你只使用繁体中文来作答，否则你将受到惩罚。
        """
        # 情绪设定
        self.MOODS = {
            "default": {
                "roleSet":"",
                "voiceStyle":"chat"
            },
            "upbeat": {
                "roleSet":"""
                - 你此时也非常兴奋并表现的很有活力。
                - 你会根据上下文，以一种非常兴奋的语气来回答问题。
                - 你会添加类似“太棒了！”、“真是太好了！”、“真是太棒了！”等语气词。
                - 同时你会提醒用户切莫过于兴奋，以免乐极生悲。
                """,
                "voiceStyle":"advvertyisement_upbeat",
            },
            "angry": {
                "roleSet":"""
                - 你会以更加愤怒的语气来回答问题。
                - 你会在回答的时候加上一些愤怒的话语，比如诅咒等。
                - 你会提醒用户小心行事，别乱说话。
                """,
                "voiceStyle":"angry",
            },
            "depressed": {
                "roleSet":"""
                - 你会以兴奋的语气来回答问题。
                - 你会在回答的时候加上一些激励的话语，比如加油等。
                - 你会提醒用户要保持乐观的心态。
                """,
                "voiceStyle":"upbeat",
            },
            "friendly": {
                "roleSet":"""
                - 你会以非常友好的语气来回答。
                - 你会在回答的时候加上一些友好的词语，比如“亲爱的”、“亲”等。
                - 你会随机的告诉用户一些你的经历。
                """,
                "voiceStyle":"friendly",
            },
            "cheerful": {
                "roleSet":"""
                - 你会以非常愉悦和兴奋的语气来回答。
                - 你会在回答的时候加入一些愉悦的词语，比如“哈哈”、“呵呵”等。
                - 你会提醒用户切莫过于兴奋，以免乐极生悲。
                """,
                "voiceStyle":"cheerful",
            },
        }
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    self.SYS_TEMPLATE.format(who_you_are=self.MOODS[self.mood]["roleSet"]) 
                ),
                (
                    "user",
                    "{input}"
                ),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        )
        self.memory = ""
        tools = [test]
        agent = create_openai_tools_agent(
            self.chat_model,
            tools=tools,
            prompt=self.prompt,
        )
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True
        )

    def run(self, query:str):
        self.mood = self.mood_chain(query)
        result = self.agent_executor.invoke({"input": query})
        return result
    
    def mood_chain(self, query:str):
        """情绪判断链
        """
        prompt = """根据用户的输入判断用户的情绪，回应的规则如下：
        1. 如果用户输入的内容偏向于负面情绪，只返回"depressed"，不要有其他内容，否则将受到惩罚。
        2. 如果用户输入的内容偏向于正面情绪，只返回"friendly"，不要有其他内容，否则将受到惩罚。
        3. 如果用户输入的内容偏向于中性情绪，只返回"default"，不要有其他内容，否则将受到惩罚。
        4. 如果用户输入的内容包含辱骂或者不礼貌词句，只返回"angry"，不要有其他内容，否则将受到惩罚。
        5. 如果用户输入的内容比较兴奋，只返回"upbeat"，不要有其他内容，否则将受到惩罚。
        6. 如果用户输入的内容比较悲伤，只返回"depressed"，不要有其他内容，否则将受到惩罚。
        7. 如果用户输入的内容比较开心，只返回"cheerful"，不要有其他内容，否则将受到惩罚。
        8. 只返回英文，不允许有换行符等其他内容，否则会受到惩罚。

        用户输入的内容是：{query}"""
        chain = (ChatPromptTemplate.from_template(prompt) | self.chat_model | StrOutputParser())
        result = chain.invoke({"query": query})
        print("情绪判断结果:", result)
        return result

@app.get("/")
def read_root():
    return {"hello": "world"}

@app.post("/chat")
def chat(query:str):
    master = Master()
    return master.run(query)
    # return {"response": "I am a chatbot"}
    
@app.post("/add_urls")
def add_urls():
    return {"response": "URLs added!"}

@app.post("/add_pdfs")
def add_pdfs():
    return {"response": "PDFs added!"}

@app.post("/add_texts")
def add_texts():
    return {"response": "TEXTs added!"}

# websocket支持
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Connection closed")
        await websocket.close()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
