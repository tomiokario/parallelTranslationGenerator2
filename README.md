# parallelTranslationGenerator2

### 概要
英日対訳を作成するWebアプリケーション
1. 長い文章を一文ごとに分割
2. 一文ごとに原文と翻訳文が対応した対訳を作成
3. 対訳を対応エディタで閲覧・記録・編集可能（Scrapbox，Markdown，プレーンテキスト）

#### ブラウザで使用する方法： Streamlit app
- https://paralleltranslationgenerator2.streamlit.app/
- DeepL APIが必要です
  - [DeepL API Free](https://support.deepl.com/hc/ja/articles/360021200939-DeepL-API-Free)プランで取得できます
  - APIを用意できない場合は[parallelTranslationGenerator(旧版)](https://github.com/tomiokario/parallelTranslationGenerator)を使用してください


### 使用例

https://github.com/tomiokario/parallelTranslationGenerator2/assets/30111767/b862073f-aef6-41ea-a683-6ba213a60982


### ローカルで動かす方法
```
streamlit run paralellTranslationGenerator.py
```

必要ライブラリ
```
pip install streamlit
pip install requests
pip install re
```
