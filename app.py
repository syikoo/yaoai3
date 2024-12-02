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
if 'selected_template_url' not in st.session_state:
    st.session_state.selected_template_url = None

# メインコンテンツエリアを2:8の比率で分割
menu_col, main_col = st.columns([2, 8])

# 左側メニューエリア
with menu_col:
    # カテゴリごとのアコーディオンメニュー
    for category, templates in TEMPLATES.items():
        with st.expander(category, expanded=True):
            for template in templates:
                # リンク形式でテンプレートを表示
                if st.markdown(
                    f"""<a href="#" class="menu-link" 
                    onclick="parent.postMessage('{template['dify_url']}', '*')">{template['title']}</a>""",
                    unsafe_allow_html=True
                ):
                    st.session_state.selected_template_url = template['dify_url']

# 右側チャットエリア
with main_col:
    if st.session_state.selected_template_url:
        # iframeでチャットボットを表示
        st.markdown(
            f"""
            <div class="chat-container">
                <iframe
                    src="{st.session_state.selected_template_url}"
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

# JavaScriptでURLの更新を処理
st.markdown("""
<script>
window.addEventListener('message', function(e) {
    if (typeof e.data === 'string' && e.data.startsWith('http')) {
        window.location.hash = e.data;
        location.reload();
    }
}, false);
</script>
""", unsafe_allow_html=True)