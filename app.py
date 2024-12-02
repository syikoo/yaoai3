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
        /* メニューリンクのスタイル */
        .template-link {
            display: block;
            padding: 0.5rem 0;
            color: #1f2937;
            text-decoration: none;
            cursor: pointer;
        }
        .template-link:hover {
            color: #2563eb;
            background-color: #f3f4f6;
        }
        
        /* プレースホルダーコンテナ */
        .placeholder-container {
            height: 80vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #f8f9fa;
            border-radius: 0.5rem;
            margin: 1rem;
        }
        
        .placeholder-text {
            color: #666;
            font-size: 1.2rem;
            text-align: center;
        }

        /* チャットコンテナ */
        .chat-container {
            height: 80vh;
            width: 100%;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = None
if 'chat_started' not in st.session_state:
    st.session_state.chat_started = False

# テンプレート選択のコールバック
def select_template(template):
    st.session_state.selected_template = template
    st.session_state.chat_started = False

# メインコンテンツエリアを2:3:5の比率で分割
menu_col, detail_col, chat_col = st.columns([2, 3, 5])

# 左列：メニューエリア
with menu_col:
    st.markdown("## メニュー")
    # カテゴリごとのアコーディオンメニュー
    for category, templates in TEMPLATES.items():
        with st.expander(category, expanded=True):
            for template in templates:
                if st.button(template['title'], key=f"btn_{template['title']}", use_container_width=True):
                    select_template(template)

# 中央列：テンプレート詳細と入力フォーム
with detail_col:
    if st.session_state.selected_template:
        template = st.session_state.selected_template
        st.markdown("## テンプレート詳細")
        st.markdown(f"### {template['title']}")
        st.markdown(template['description'])
        
        # 変数入力フォーム
        st.markdown("### 入力項目")
        with st.form("template_form"):
            input_values = {}
            if 'variables' in template:
                for var_name, var_desc in template['variables'].items():
                    input_values[var_name] = st.text_input(
                        var_desc,
                        key=f"input_{var_name}"
                    )
            
            submit_button = st.form_submit_button(
                "会話を始める",
                use_container_width=True,
                type="primary"
            )
            if submit_button:
                st.session_state.selected_template = {
                    **template,
                    'input_variables': input_values
                }
                st.session_state.chat_started = True
    else:
        # 初期表示
        st.markdown(
            """
            <div class="placeholder-container">
                <div class="placeholder-text">メニューを選択してください</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# 右列：チャットエリア
with chat_col:
    if st.session_state.chat_started and st.session_state.selected_template:
        template = st.session_state.selected_template
        
        # URLパラメータの構築
        chat_url = template['dify_url']
        if 'input_variables' in template:
            params = []
            for var_name, var_value in template['input_variables'].items():
                if var_value:
                    params.append(f"{var_name}={var_value}")
            if params:
                chat_url += "?" + "&".join(params)
        
        # iframeの表示
        st.markdown(
            f"""
            <div class="chat-container">
                <iframe
                    src="{chat_url}"
                    width="100%"
                    height="100%"
                    frameborder="0"
                    allow="microphone"
                ></iframe>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # 初期表示
        st.markdown(
            """
            <div class="placeholder-container">
                <div class="placeholder-text">(チャット画面)</div>
            </div>
            """,
            unsafe_allow_html=True
        )