# parallelTranslationGenerator2

Streamlit app
- https://paralleltranslationgenerator2.streamlit.app/

英日対訳を作成するWebアプリケーション
1. 長い文章を一文ごとに分割
2. 原文と機械翻訳を一文ごとに対応づけた対訳文を作成
3. 対訳をエディタで閲覧・記録・編集が可能（Scrapbox，Markdown，プレーンテキスト）

ローカルで動かす方法
```
streamlit run paralellTranslationGenerator.py
```

必要ライブラリ
```
pip install streamlit
pip install requests
pip install re
```
