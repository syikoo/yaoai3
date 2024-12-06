# 自動車レビューにおけるAI技術評価
TEMPLATES = {
    "正確性": [
        {
            "title": "1-1 正確性：指定項目抽出 (テキスト文)",
            "description": "(基本的な技術検証) あらかじめ用意したモデルのテキスト文に対して、指定項目に沿って正確な情報を収集する",
            "variables": {
                "company": { "description": "会社名", "default": "ヤマハ" },
                "model": { "description": "モデル", "default": "MT-09" }
            },
            "system_prompt": """ 略 """,
            "initial_prompt": "略",
            "dify_config": {
                "iframe_url": "https://udify.app/chatbot/Ggjt9ahkeh3XaSGu",
                "base_url": "https://api.dify.ai/v1",
                "token": "Ggjt9ahkeh3XaSGu"
            }
        },
        {
            "title": "1-2 正確性：指定項目抽出 (ネット検索)",
            "description": """特定車種の最新モデルについて、ネット検索にて、指定項目に沿って正確な情報を収集する。
              サイト名：https://www.bikebros.co.jp/catalog/""",
            "variables": {
                "company": { "description": "会社名", "default": "ヤマハ" },
                "model": { "description": "モデル", "default": "MT-09" }
            },
            "system_prompt": """ 略 """,
            "initial_prompt": "略",
            "dify_config": {
                "iframe_url": "https://udify.app/chatbot/fESPc0M1LRes8lNB",
                "base_url": "https://api.dify.ai/v1",
                "token": "fESPc0M1LRes8lNB"
            }
        },
        {
            "title": "1-3 正確性：項目抽出立案",
            "description": """競合他社ごとに、**特定車種と競合する可能性のあるモデル**を、競合になりうる順に順位付けする。""",
            "variables": {
                "company": { "description": "会社名", "default": "ヤマハ" },
                "model": { "description": "モデル", "default": "MT-09/Y-AMT（2024年モデル）" }
            },
            "system_prompt": """ 略 """,
            "initial_prompt": "略",
            "dify_config": {
                "iframe_url": "https://udify.app/chatbot/Esg59l58dpBfU2Iy",
                "base_url": "https://api.dify.ai/v1",
                "token": "app-SpFkoCb88fAfK1HWZZMsCdwQ"
            }
        }
    ],
    "ゆらぎ・要約・翻訳": [
        {
            "title": "2 類似名検索",
            "description": "対象車種の部品に関するレビュー情報を検索し、指定された用語について以下の条件に従い情報を抜き出す",
            "variables": {
                "company": { "description": "会社名", "default": "ヤマハ" },
                "model": { "description": "モデル", "default": "MT-09/Y-AMT（2024年モデル）  " },
                "part_name": { "description": "部品名", "default": "Radiator" }
            },
            "system_prompt": """ 略 """,
            "initial_prompt": "略",
            "dify_config": {
                "iframe_url": "https://udify.app/chatbot/40cFSdfIOiNjWfJM",
                "base_url": "https://api.dify.ai/v1",
                "token": "40cFSdfIOiNjWfJM"
            }
        }
    ],
    "要約・翻訳": [
        {
            "title": "3 要約：長文レビューの要約 (MT-09固定テキスト)",
            "description": "入力されたテキスト文を指定字数以内で要約する。想定シナリオ：あるモデルのレビュー情報テキストを設計者が新しいモデルの設計に活かせる部分を抜粋する",
            "variables": {
                "Charactor_count": { "description": "要約した結果の文字数", "default": "200" }
            },
            "system_prompt": """ 略 """,
            "initial_prompt": "略",
            "dify_config": {
                "iframe_url": "https://udify.app/chatbot/WDYGyjkBYCdzjX2a",
                "base_url": "https://api.dify.ai/v1",
                "token": "WDYGyjkBYCdzjX2a"
            }
        },
        {
            "title": "4 翻訳：インドネシア語の翻訳)",
            "description": "インドネシア語を自然な日本語になるように翻訳する",
            "variables": {
                "Charactor_count": { "description": "要約した結果の文字数", "default": "200" }
            },
            "system_prompt": """ 略 """,
            "initial_prompt": "略",
            "dify_config": {
                "iframe_url": "https://udify.app/chatbot/2RY8YDGM6aS4tmGz",
                "base_url": "https://api.dify.ai/v1",
                "token": "2RY8YDGM6aS4tmGz"
            }
        }
    ]
}