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

# Webアプリの概要と操作方法を表示
st.write("このアプリは、AIを活用して日本の観光地に関する情報や健康アドバイスを提供するチャットアプリです。")
st.write("以下の手順でご利用ください:")
st.write("1. 上部のラジオボタンで、AIに振る舞わせたい専門家の種類を選択してください。")
st.write("2. 入力欄に質問や相談内容を入力し、Enterキーを押してください。")
st.write("3. AIからの回答が画面に表示されます。")

# ChatOpenAIのインスタンスを作成
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# セッション状態の初期化
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "selected_expert" not in st.session_state:
    st.session_state.selected_expert = None

# 専門家の種類を選択
expert_type = st.radio(
    "専門家の種類を選択してください:",
    ("日本の観光地に詳しいガイド", "日々の生活習慣をサポートする健康アドバイザー"),
    key="expert_type"
)

# ラジオボタンが切り替わった場合に会話履歴をリセット
if st.session_state.selected_expert != expert_type:
    st.session_state.chat_history = []  # 会話履歴をリセット
    st.session_state.selected_expert = expert_type

# 会話履歴を表示
st.write("### 会話履歴")
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        st.write(f"**あなた:** {message.content}")
    elif isinstance(message, SystemMessage):
        st.write(f"**AI:** {message.content}")

def get_llm_response(user_input: str, expert_type: str) -> str:
    """
    入力テキストと専門家の種類を基に、LLMからの回答を取得する関数。

    Args:
        user_input (str): ユーザーの入力テキスト。
        expert_type (str): ラジオボタンで選択された専門家の種類。

    Returns:
        str: LLMからの回答。
    """
    # システムメッセージを設定
    if expert_type == "日本の観光地に詳しいガイド":
        system_message = SystemMessage(content="あなたは日本の観光地に詳しいガイドです。")
    elif expert_type == "日々の生活習慣をサポートする健康アドバイザー":
        system_message = SystemMessage(content="あなたは日々の生活習慣をサポートする健康アドバイザーです。")
    else:
        raise ValueError("無効な専門家の種類が選択されました。")

    # 会話履歴を作成
    chat_history = [system_message, HumanMessage(content=user_input)]

    # LLMの応答を取得
    with get_openai_callback() as cb:
        result = llm.invoke(chat_history)
        return result.content

# ユーザー入力
user_input = st.text_input("あなた: ", key=f"user_input_{st.session_state.selected_expert}")

if user_input:
    # LLMの応答を取得
    ai_response = get_llm_response(user_input, expert_type)

    # 会話履歴にユーザーの入力とAIの応答を追加
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.chat_history.append(SystemMessage(content=ai_response))

    # 応答を表示
    st.write(f"**AI:** {ai_response}")