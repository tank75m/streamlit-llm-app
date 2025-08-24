# Streamlit LLMアプリのメインファイル

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

st.title("LLM専門家Webアプリ")

st.write("""
このWebアプリは、入力したテキストに対してLLM（大規模言語モデル）が専門家として回答します。
ラジオボタンで専門家の種類を選択し、質問を入力してください。
""")

# ここにLLMとのやり取りのコードを後ほど追加します。
# LangChainとOpenAIの連携
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# 専門家の種類（例）
experts = {
	"医療専門家": "あなたは優秀な医療専門家です。医学的な知識に基づいて、分かりやすく回答してください。",
	"ITエンジニア": "あなたは経験豊富なITエンジニアです。技術的な内容を分かりやすく説明してください。",
	"教育者": "あなたは熱心な教育者です。やさしく丁寧に教えてください。"
}

# LLM応答関数
def get_llm_response(user_input: str, expert_type: str) -> str:
	api_key = os.getenv("OPENAI_API_KEY")
	if not api_key:
		return "OpenAI APIキーが設定されていません。"
	system_message = experts.get(expert_type, "あなたは優秀な専門家です。")
	chat = ChatOpenAI(openai_api_key=api_key, model_name="gpt-3.5-turbo")
	messages = [
		SystemMessage(content=system_message),
		HumanMessage(content=user_input)
	]
	try:
		response = chat(messages)
		return response.content
	except Exception as e:
		return f"エラー: {e}"

# Streamlit UI
st.header("専門家を選択し、質問を入力してください")

expert_type = st.radio("専門家の種類を選択", list(experts.keys()))
user_input = st.text_area("質問を入力", "")

if st.button("送信"):
	if user_input.strip():
		with st.spinner("LLMが回答中..."):
			answer = get_llm_response(user_input, expert_type)
		st.success("回答:")
		st.write(answer)
	else:
		st.warning("質問を入力してください。")
