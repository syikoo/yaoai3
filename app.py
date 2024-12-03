import streamlit as st
from streamlit.components.v1 import html
import json
import gzip
import base64
from urllib.parse import quote

from templates import TEMPLATES

# 変数をエンコードする関数
def urlencode_difi_variable(value):
    """
    値をGZIP圧縮してbase64エンコードする
    1. 文字列をUTF-8でバイトに変換
    2. GZIPで圧縮
    3. base64でエンコード
    4. URLエンコード
    """
    # 文字列をGZIP圧縮
    compressed = gzip.compress(value.encode('utf-8'))
    # base64エンコード
    b64 = base64.b64encode(compressed)
    # URLエンコード
    return quote(b64.decode('utf-8'))


# ページ設定
st.set_page_config(
    page_title="Auto Repair AI Assistant",
    layout="wide"
)

# カスタムCSS
st.markdown("""
    <style>
        /* メニューアイテムのコンテナスタイル */
        .menu-item-container {
            border: 1px solid #dee2e6;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 0.8rem;
            background-color: #ffffff;
        }
        
        /* メニュータイトルと説明のスタイル */
        .menu-title {
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .menu-description {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 0.8rem;
        }

        /* チャットコンテナのスタイル */
        .chat-container {
            height: calc(100vh - 80px);  /* ビューポートの高さから上部マージンを引く */
            width: 100%;
            margin-top: 1rem;
        }
        
        .placeholder-container {
            height: calc(100vh - 80px);
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #f8f9fa;
            border-radius: 0.5rem;
            margin: 1rem;
        }

        /* iframeのスタイル */
        .chat-container iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
    </style>
""", unsafe_allow_html=True)


# セッション状態の初期化
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = None
if 'chat_started' not in st.session_state:
    st.session_state.chat_started = False

# コールバック関数
def select_template(template):
    st.session_state.selected_template = template
    st.session_state.chat_started = False

# メインコンテンツエリアを2:3:5の比率で分割
menu_col, detail_col, chat_col = st.columns([2, 3, 5])

# 左列：メニューエリア
with menu_col:
    st.markdown("## メニュー")
    for category, templates in TEMPLATES.items():
        with st.expander(category, expanded=True):
            for idx, template in enumerate(templates):
                container = st.container()
                with container:
                    st.markdown(f"""
                        <div class="menu-item-container">
                            <div class="menu-title">{template['title']}</div>
                            <div class="menu-description">{template['description']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("選択", key=f"btn_{idx}_{template['title']}", use_container_width=True):
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
                for var_name, var_info in template['variables'].items():
                    default_value = var_info.get('default', '') if isinstance(var_info, dict) else ''
                    description = var_info.get('description', var_info) if isinstance(var_info, dict) else var_info
                    
                    input_values[var_name] = st.text_input(
                        description,
                        value=default_value,
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
                    'variables': input_values
                }
                st.session_state.chat_started = True
    else:
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
        
        # ベースURLの取得
        chat_url = template['dify_config']['iframe_url']
        
        # 変数のエンコードと追加
        params = []
        if 'variables' in template:
            for var_name, var_info in template['variables'].items():
                # 入力値の取得（入力値があればそれを使用、なければデフォルト値を使用）
                value = (template.get('variables', {}).get(var_name) or 
                        var_info.get('default', ''))
                if value:  # 値が存在する場合
                    encoded_value = urlencode_difi_variable(value)
                    params.append(f"{var_name}={encoded_value}")

        # URLの組み立て
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
                    allow="microphone">
                </iframe>
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

