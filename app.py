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
        /* タイルのスタイル */
        div[data-testid="stExpander"] {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
            height: 100%;
        }
        
        /* タイル内の文字スタイル */
        div[data-testid="stExpander"] h3 {
            margin-top: 0;
            color: #1f2937;
        }
        
        /* iframeコンテナのスタイル */
        .iframe-container {
            height: 100%;
            min-height: 500px;
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
            st.markdown(f"### {template['title']}")
            st.markdown(template['description'])
            
            if st.button("選択", key=f"select_{template['title']}", use_container_width=True):
                st.session_state.selected_template = template

# 右側メインエリア
with main_col:
    # 上下に分割（1:1の比率）
    top_section, bottom_section = st.container(), st.container()
    
    # 上部：選択されたテンプレートの入力フォーム
    with top_section:
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
    
    # 下部：チャットフレーム
    with bottom_section:
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
                        style="width: 100%; height: 100%; min-height: 500px"
                        frameborder="0"
                        allow="microphone">
                    </iframe>
                </div>
                """,
                unsafe_allow_html=True
            )