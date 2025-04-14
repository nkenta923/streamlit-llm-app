import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.callbacks import get_openai_callback

# 環境変数の読み込み
load_dotenv()

# Streamlitアプリの設定
st.title("AIチャットアプリ")
st.write("AIとの会話を開始します。")

# ChatOpenAIのインスタンスを作成
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# セッション状態で会話履歴を管理
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content="あなたは親切なアシスタントです。")
    ]

# 会話履歴を表示
st.write("### 会話履歴")
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        st.write(f"**あなた:** {message.content}")
    elif isinstance(message, SystemMessage):
        st.write(f"**AI:** {message.content}")

# ユーザー入力
user_input = st.text_input("あなた: ", key="user_input")

if user_input:
    # 会話履歴にユーザーの入力を追加
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    # AIの応答を取得
    with get_openai_callback() as cb:
        result = llm.invoke(st.session_state.chat_history)
        ai_response = result.content

        # 応答を表示
        st.write(f"**AI:** {ai_response}")
        st.write(f"  プロンプトの消費トークン数: {cb.prompt_tokens}")
        st.write(f"  完了の消費トークン数: {cb.completion_tokens}")
        st.write(f"  合計消費トークン数: {cb.total_tokens}")
        st.write(f"  合計費用 (USD): ${cb.total_cost}")

    # 会話履歴にAIの応答を追加
    st.session_state.chat_history.append(SystemMessage(content=ai_response))