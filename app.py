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
        
        /* メニューリンクのスタイル */
        .menu-link {
            display: block;
            padding: 0.5rem 0;
            color: #1f2937;
            text-decoration: none;
        }
        .menu-link:hover {
            color: #2563eb;
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
if 'chat_started' not in st.session_state:
    st.session_state.chat_started = False

# メインコンテンツエリアを2:3:5の比率で分割
menu_col, detail_col, chat_col = st.columns([2, 3, 5])

# 左列：メニューエリア
with menu_col:
    # カテゴリごとのアコーディオンメニュー
    for category, templates in TEMPLATES.items():
        with st.expander(category, expanded=True):
            for template in templates:
                # リンク形式でテンプレートを表示
                if st.markdown(
                    f"""<a href="#" class="menu-link">{template['title']}</a>""",
                    unsafe_allow_html=True
                ):
                    st.session_state.selected_template = template
                    st.session_state.chat_started = False
                    st.rerun()

# 中央列：テンプレート詳細と入力フォーム
with detail_col:
    if st.session_state.selected_template:
        template = st.session_state.selected_template
        
        # テンプレート情報の表示
        st.markdown(f"## {template['title']}")
        st.markdown(template['description'])
        
        # 変数入力フォーム
        with st.form("template_form"):
            variables = {}
            if 'variables' in template:
                for var_name, var_desc in template['variables'].items():
                    variables[var_name] = st.text_input(var_desc)
            
            if st.form_submit_button("会話を始める", use_container_width=True):
                st.session_state.chat_started = True
                st.session_state.selected_template = {
                    **template,
                    'input_variables': variables
                }
                st.rerun()
    else:
        st.markdown(
            """
            <div class="chat-container">
                <div class="placeholder-text">メニューを選択ください</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# 右列：チャットエリア
with chat_col:
    if st.session_state.chat_started and st.session_state.selected_template:
        template = st.session_state.selected_template
        chat_url = template['dify_url']
        
        # 変数をURLに追加
        if 'input_variables' in template:
            params = []
            for var_name, var_value in template['input_variables'].items():
                if var_value:
                    params.append(f"{var_name}={var_value}")
            if params:
                chat_url += "?" + "&".join(params)
        
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
        st.markdown(
            """
            <div class="chat-container">
                <div class="placeholder-text">(チャット画面)</div>
            </div>
            """,
            unsafe_allow_html=True
        )