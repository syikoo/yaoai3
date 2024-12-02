import streamlit as st
from templates import TEMPLATES

# ページ設定
st.set_page_config(
    page_title="Auto Repair AI Assistant",
    layout="wide"
)

# カスタムCSS
st.markdown("""
    <style>
        /* アコーディオンメニューのスタイル */
        .streamlit-expanderHeader {
            font-weight: bold;
            background-color: #f8f9fa;
        }
        
        /* チャット画面のスタイル */
        .chat-container {
            height: 90vh;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #f8f9fa;
            border-radius: 0.5rem;
        }
        
        .placeholder-text {
            color: #666;
            font-size: 1.2rem;
        }
    </style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = None

# メインコンテンツエリアを2:8の比率で分割
menu_col, main_col = st.columns([2, 8])

# 左側メニューエリア
with menu_col:
    # カテゴリごとのアコーディオンメニュー
    for category, templates in TEMPLATES.items():
        with st.expander(category, expanded=True):
            for template in templates:
                if st.button(template['title'], key=f"select_{template['title']}", use_container_width=True):
                    st.session_state.selected_template = template

# 右側チャットエリア
with main_col:
    if st.session_state.selected_template:
        template = st.session_state.selected_template
        chat_url = template['dify_url']
        
        # iframeでチャットボットを表示
        st.markdown(
            f"""
            <div class="chat-container">
                <iframe
                    src="{chat_url}"
                    style="width: 100%; height: 100%;"
                    frameborder="0"
                    allow="microphone">
                </iframe>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # 初期画面のプレースホルダー
        st.markdown(
            """
            <div class="chat-container">
                <div class="placeholder-text">(チャット画面)</div>
            </div>
            """,
            unsafe_allow_html=True
        )
