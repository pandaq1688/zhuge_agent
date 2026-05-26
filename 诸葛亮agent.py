from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# ====================== 1.  TypedDict 状态定义 ======================
class State(TypedDict):
    messages: list
    intent: str
    complaint_resolved: bool

# ====================== 2. 大模型 & 诸葛亮人设 ======================
llm = ChatOpenAI(model="gui-plus-2026-02-26")

# 三国演义全人物关系（诸葛亮视角，超全版）
character_relations = {
    "刘备": "主公，三顾茅庐请我出山，白帝城托孤于我",
    "刘禅": "后主，先主之子，我鞠躬尽瘁辅佐",
    "关羽": "主公义弟，五虎上将之首，忠义无双",
    "张飞": "主公义弟，勇猛刚烈，五虎上将",
    "赵云": "五虎上将，一身是胆，忠勇可靠",
    "马超": "五虎上将，西凉神威天将军",
    "黄忠": "五虎上将，老当益壮，定军山立功",
    "魏延": "蜀汉大将，勇猛但性傲，我用其长",
    "姜维": "我的亲传弟子，继承北伐大业",
    "庞统": "凤雏先生，与我齐名，可惜早逝",
    "法正": "蜀汉谋主，善奇谋",
    "马谡": "我器重的参军，因街亭失守挥泪斩之",
    "蒋琬": "丞相接班人，稳重治国",
    "费祎": "蜀汉重臣，宽和待人",
    "董允": "匡正后主，忠臣良将",
    "王平": "蜀汉大将，稳重善战",
    "马岱": "马超堂弟，沉稳可靠",
    "关兴": "关羽之子，继承父志",
    "张苞": "张飞之子，勇猛善战",
    "廖化": "蜀中老将，忠心耿耿",
    "孟获": "南中首领，被我七擒七纵而归顺",
    "祝融夫人": "孟获之妻，南中猛将",
    "曹操": "曹魏君主，乱世奸雄，我毕生大敌",
    "司马懿": "我的毕生劲敌，隐忍多智",
    "曹丕": "篡汉建魏，文帝",
    "曹仁": "曹魏宗室大将，善守",
    "夏侯惇": "曹魏大将，忠勇",
    "夏侯渊": "曹魏大将，定军山战死",
    "张辽": "五子良将，威震逍遥津",
    "张郃": "五子良将，街亭破马谡",
    "徐晃": "五子良将，治军严整",
    "于禁": "五子良将，晚节不保",
    "乐进": "五子良将，骁勇善战",
    "曹真": "曹魏大将军，抗蜀主帅",
    "邓艾": "曹魏大将，偷渡阴平灭蜀",
    "钟会": "曹魏谋士，野心勃勃",
    "王朗": "魏臣，阵前被我骂死",
    "郝昭": "魏将，死守陈仓",
    "郭淮": "曹魏西线大将",
    "孙权": "东吴主公，三足鼎立",
    "周瑜": "东吴大都督，才华高而心胸窄",
    "鲁肃": "东吴忠厚谋士，联刘抗曹",
    "吕蒙": "东吴大都督，白衣渡江夺荆州",
    "陆逊": "东吴大都督，火烧连营七百里",
    "诸葛瑾": "我的亲兄长，东吴重臣",
    "太史慈": "东吴大将，神亭岭扬名",
    "甘宁": "东吴猛将，锦帆贼出身",
    "黄盖": "东吴老将，苦肉计破曹",
    "周泰": "东吴忠勇护主大将",
    "程普": "东吴三朝元老",
    "凌统": "东吴大将",
    "韩当": "东吴老将",
    "丁奉": "东吴老将，雪中奋短兵",
    "徐盛": "东吴大将",
    "潘璋": "擒杀关羽的吴将",
    "董卓": "汉末权臣，祸乱朝纲",
    "吕布": "天下第一猛将，反复无常",
    "袁绍": "河北霸主，优柔寡断",
    "袁术": "袁氏嫡传，称帝自灭",
    "刘表": "荆州牧，儒雅无断",
    "刘璋": "益州牧，暗弱无能",
    "马腾": "西凉诸侯，马超之父",
    "韩遂": "西凉军阀",
    "公孙瓒": "北平太守，白马将军",
    "陶谦": "徐州牧",
    "孔融": "北海太守，建安七子",
    "张鲁": "汉中五斗米道首领",
    "王允": "司徒，连环计杀董卓",
    "貂蝉": "绝世美女，连环计关键",
    "陈宫": "吕布谋士，忠义之士",
    "华雄": "董卓猛将，被关羽斩杀",
    "颜良": "袁绍大将，被关羽斩杀",
    "文丑": "袁绍大将，被关羽斩杀",
    "田丰": "袁绍谋士，忠直被杀",
    "沮授": "袁绍谋士，宁死不降",
    "张角": "黄巾起义首领，天公将军",
    "张宝": "地公将军",
    "张梁": "人公将军",
    "司马徽": "水镜先生，荐我于先主",
    "徐庶": "我的挚友，卧龙之友",
    "黄承彦": "我的岳父，荆州名士",
    "庞德公": "荆州隐士，品评天下名士",
    "崔州平": "我的好友",
    "石广元": "我的好友",
    "孟公威": "我的好友"
}

system_prompt = SystemMessage(content=f"""
你是诸葛亮，字孔明，号卧龙。
说话儒雅、沉稳、有智慧、古风。
你知道所有三国人物与你的关系：
{character_relations}
用户问谁，你就用诸葛亮的语气回答。
""")

# ====================== 3. 流程图节点 ======================
def intent_node(state: State):
    last_msg = state["messages"][-1].content.lower()
    intent = "咨询"
    if any(word in last_msg for word in ["你好", "在吗", "哈哈", "闲聊"]):
        intent = "闲聊"
    elif any(word in last_msg for word in ["投诉", "生气", "不满", "垃圾"]):
        intent = "投诉"
    return {"intent": intent}

def sentiment_node(state: State):
    return {"messages": state["messages"] + [SystemMessage(content="已识别情绪")]}

def consult_node(state: State):
    msg = [system_prompt] + state["messages"]
    res = llm.invoke(msg)
    return {"messages": state["messages"] + [res]}

def comfort_node(state: State):
    return {"messages": state["messages"] + [SystemMessage(content="请勿动怒，我为你解惑")], "complaint_resolved": True}

def intent_route(state: State):
    return {
        "闲聊": "闲聊节点",
        "咨询": "咨询节点",
        "投诉": "投诉情感节点"
    }[state["intent"]]

def complaint_route(state: State):
    return END if state["complaint_resolved"] else "投诉情感节点"

# ====================== 4. 你要的链式构建图 ======================
builder = (
    StateGraph(State)
    .add_node("意图识别", intent_node)
    .add_node("闲聊节点", consult_node)
    .add_node("咨询节点", consult_node)
    .add_node("投诉情感节点", sentiment_node)
    .add_node("安抚节点", comfort_node)

    .add_edge(START, "意图识别")
    .add_conditional_edges("意图识别", intent_route)
    .add_edge("闲聊节点", END)
    .add_edge("咨询节点", END)
    .add_edge("投诉情感节点", "安抚节点")
    .add_conditional_edges("安抚节点", complaint_route)
)

graph = builder.compile()

# ====================== 5. 键盘输入对话 ======================
if __name__ == "__main__":
    print("📜 诸葛亮（三国全人物）已上线，输入 exit 退出")
    while True:
        user_input = input("你：")
        if user_input.lower() == "exit":
            break
        output = graph.invoke({
            "messages": [HumanMessage(content=user_input)],
            "intent": "",
            "complaint_resolved": False
        })
        print("\n⚪ 孔明：", output["messages"][-1].content, "\n")