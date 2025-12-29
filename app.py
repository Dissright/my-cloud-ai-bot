import streamlit as st
from openai import OpenAI

# 页面配置
st.set_page_config(page_title="云计算AI大作业", page_icon="☁️")
st.title("☁️ 基于云服务的智能机器人")

# 侧边栏配置
with st.sidebar:
    st.header("云端配置")
    st.info("模型：deepseek-v3\n平台：火山引擎Ark")
    if st.button("清除对话历史"):
        st.session_state.messages = []
        st.rerun()

# --- 关键修改：从云端机密管理读取 Key ---
# 在本地运行时，你需要在 .streamlit/secrets.toml 中配置它
# 在 Streamlit Cloud 部署时，在 Advanced Settings 中配置
try:
    api_key = st.secrets["API_KEY"]
except KeyError:
    st.error("未找到 API_KEY 配置。请在 Secrets 中设置。")
    st.stop()

# 初始化 API 客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示聊天记录
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 聊天输入
if prompt := st.chat_input("请输入您的问题..."):
    # 1. 用户提问
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. 调用云端 API
    with st.chat_message("assistant"):
        with st.spinner("云端服务器计算中..."):
            try:
                response = client.chat.completions.create(
                    model="deepseek-v3-2-251201",
                    messages=[
                        {"role": "system", "content": "你是一个由云计算技术驱动的智能助理。"},
                        *st.session_state.messages
                    ]
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                # 3. 保存回答
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"调用云服务出错: {str(e)}")