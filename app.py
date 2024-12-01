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
        /* 上下分割用のコンテナスタイル */
        .split-container {
            height: 45vh;
            overflow-y: auto;
            padding: 1rem;
            margin-bottom: 1rem;
            background-color: white;
        }
        
        /* テンプレートカードのスタイル */
        .template-card {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        /* iframeコンテナのスタイル */
        .iframe-container {
            height: 100%;
            min-height: 45vh;
        }
        
        /* スクロールバーのカスタマイズ */
        .split-container::-webkit-scrollbar {
            width: 5px;
        }
        .split-container::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        .split-container::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = list(TEMPLATES.keys())[0]
if 'selected_template' not in st.session_state:
    st.session_state.selected_template = None

# サイドバー（カテゴリ選択）
with st.sidebar:
    st.title("AI アシスタント")
    for category in TEMPLATES.keys():
        if st.button(category, use_container_width=True):
            st.session_state.selected_category = category
            st.session_state.selected_template = None

# メインコンテンツエリアを2:8の比率で分割
menu_col, main_col = st.columns([2, 8])

# 左側メニューエリア
with menu_col:
    st.subheader("テンプレート一覧")
    
    # 選択されたカテゴリのテンプレートを表示
    templates = TEMPLATES[st.session_state.selected_category]
    
    for template in templates:
        with st.container():
            st.markdown(
                f"""
                <div class="template-card">
                    <h3>{template['title']}</h3>
                    <p>{template['description']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("選択", key=f"select_{template['title']}", use_container_width=True):
                st.session_state.selected_template = template

# 右側メインエリア
with main_col:
    # 上部：選択されたテンプレートの入力フォーム
    st.markdown('<div class="split-container">', unsafe_allow_html=True)
    if st.session_state.selected_template:
        template = st.session_state.selected_template
        st.markdown(f"## {template['title']}")
        
        # 変数入力フォーム
        with st.form(key="template_form"):
            variables = {}
            if 'variables' in template:
                for var_name, var_desc in template['variables'].items():
                    variables[var_name] = st.text_input(var_desc)
            
            if st.form_submit_button("チャットを開始", use_container_width=True):
                st.session_state.selected_template = {
                    **template,
                    'input_variables': variables
                }
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 下部：チャットフレーム
    st.markdown('<div class="split-container">', unsafe_allow_html=True)
    if st.session_state.selected_template and 'input_variables' in st.session_state.selected_template:
        template = st.session_state.selected_template
        
        # プロンプト情報の表示（折りたたみ可能）
        with st.expander("プロンプト情報", expanded=False):
            st.markdown("**システムプロンプト:**")
            st.markdown(template['system_prompt'])
            st.markdown("**初期プロンプト:**")
            st.markdown(template['initial_prompt'])
        
        # チャットボットの表示
        chat_url = template['dify_url']
        if 'input_variables' in template:
            for var_name, var_value in template['input_variables'].items():
                if var_value:
                    chat_url += f"&{var_name}={var_value}"
        
        # iframeでチャットボットを表示
        st.markdown(
            f"""
            <div class="iframe-container">
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
    st.markdown('</div>', unsafe_allow_html=True)
