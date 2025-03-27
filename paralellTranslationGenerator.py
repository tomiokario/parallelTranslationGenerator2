import streamlit as st
import requests
import re

import streamlit.components.v1 as components

# Set page title and favicon
st.set_page_config(page_title="対訳作成補助ソフト", page_icon=":books:")

# Escape characters
escape = [
    ['e.g.', 'ESCEGEGEGESC'],
    ['i.e.', 'ESCIEIEIEESC'],
    ['Eq.', 'ESCEQEQEQESC'],
    ['vs.', 'ESCVSVSVSESC'],
    ['et al.', 'ETALETALETAL'],
    ['Fig.', 'ESCFIGFIGESC']
]

# Get DEEPL_KEY from sidebar
DEEPL_KEY = st.sidebar.text_input("Enter DeepL API Key", type="password")
st.sidebar.write("DeepL API: https://www.deepl.com/ja/your-account/keys")

# English to Japanese translation using DeepL API
def en2jp_deepl(translate_text):

    if DEEPL_KEY:
        params = {
            "auth_key": DEEPL_KEY,
            "text": [translate_text],
            "source_lang": 'EN',
            "target_lang": 'JA'
        }

        request = requests.post("https://api-free.deepl.com/v2/translate", json=params)
        result = request.json()
        
        # APIレスポンスのデバッグ出力（デバッグ時のみ有効化）
        # st.write("API Response:", result)
        
        # エラーハンドリングを追加
        if "translations" in result:
            return result["translations"][0]["text"]
        elif "error" in result:
            error_msg = f"DeepL API Error: {result['error'].get('message', 'Unknown error')}"
            st.error(error_msg)
            return ""
        else:
            st.error(f"Unexpected API response format: {result}")
            return ""
    else:
        st.warning("Please enter the DeepL API Key in the sidebar.")
        return ""

def main():
    output = ""
    st.title("対訳作成")
    st.caption("英文と日本語訳を一文ごとに組み合わせて出力します。")

    # セッションステートでテキストデータを管理
    if 'text' not in st.session_state:
        st.session_state.text = ""

    # テキストエリアの定義
    st.session_state.text = st.text_area("翻訳したい文章を入力してください", height=200, value=st.session_state.text)

    col1, col2, col3 = st.columns(3)

    with col1:
        auto_split = st.checkbox("自動整形", value=True)
        if auto_split:
            st.write("自動で改行位置を設定します")
        else:
            st.write("改行を維持します")

    with col2:
        output_type = st.selectbox("出力形式", ("Scrapbox", "Markdown", "Plain text"))

    with col3:
        with st.popover("settings"):
            punctuation_type = st.selectbox("句読点", ("「 ，．」", "「 、。」"))
            replace_substitution = False
            newline2blank = False
            if output_type == "Scrapbox":
                replace_substitution = st.checkbox("[]を全角に自動置換（リンク化の回避）", value=True)
            if auto_split:
                newline2blank = st.checkbox("原文の改行を空行に変換", value=False)
        #if st.button("クリア"):
        #    st.session_state.text = ""  # テキストエリアを空にする

    english_str = st.session_state.text
    if auto_split:
        if newline2blank:
            english_str = english_str.replace('\n', '\n<BLANKBLANKBLANK>\n')
            english_str = english_str.replace('\r', '\n<BLANKBLANKBLANK>\n')
        else:
            english_str = english_str.replace('-\n', '')
            english_str = english_str.replace('-\r', '')
            english_str = english_str.replace('\n', ' ')
            english_str = english_str.replace('\r', ' ')
        english_str = english_str.replace('\u3000', ' ')
        english_str = re.sub(r"\.\s+", ".", english_str)
        english_str = re.sub(r"^\s+", "", english_str)
        english_str = english_str.replace('<BLANKBLANKBLANK>', ' ')
        for i in range(len(escape)):
            english_str = english_str.replace(escape[i][0], escape[i][1])
        array_dicimal = re.findall(r"\d+\.\d+", english_str)
        english_str = re.sub(r"\d+\.\d+", "<DICIMALDICIMALDICIMAL>", english_str)
        numbers = re.findall(r"\.\d+", english_str)
        english_str = re.sub(r"\.[0-9]+", "<DOTPLUSNUMBERSPATTERN>", english_str)
        brackets_numbers = re.findall(r"\.\[\d+\]", english_str)
        english_str = re.sub(r"\.\[[0-9]+\]", "<DOTPLUSBRACKETSNUMBERSPATTERN>", english_str)
        english_str = english_str.replace('.', '.\n')
        english_str = english_str.replace("<DOTPLUSNUMBERSPATTERN>", "<DOTPLUSNUMBERSPATTERN>\n")
        english_str = english_str.replace("<DOTPLUSBRACKETSNUMBERSPATTERN>", "<DOTPLUSBRACKETSNUMBERSPATTERN>\n")
        for i in range(len(escape)):
            english_str = english_str.replace(escape[i][1], escape[i][0])
        for dicimal in array_dicimal:
            english_str = english_str.replace("<DICIMALDICIMALDICIMAL>", str(dicimal), 1)
        for number in numbers:
            english_str = english_str.replace("<DOTPLUSNUMBERSPATTERN>", str(number), 1)
        for brackets_number in brackets_numbers:
            english_str = english_str.replace("<DOTPLUSBRACKETSNUMBERSPATTERN>", str(brackets_number), 1)

    if st.button("翻訳"):
        input_str = en2jp_deepl(english_str)
        array_jp = input_str.split('\n')
        array_en = english_str.split('\n')

        for j in range(len(array_jp)):
            if array_en[j] == "" or array_en[j] == " ":
                output += '\n'
                continue
            if output_type == 'Scrapbox':
                en_top = ">"
                jp_top = "\t "
            elif output_type == 'Markdown':
                en_top = ">"
                jp_top = "- "
            else:
                en_top = ""
                jp_top = " ・"
            output += en_top + array_en[j] + "\n"
            output += jp_top + array_jp[j] + "\n"

        output = output.replace('\n\n\n', '\n\n')

        if replace_substitution:
            output = output.replace('[', '［')
            output = output.replace(']', '］')

        if punctuation_type == "「 、。」":
            output = output.replace('，', '、')
            output = output.replace('．', '。')
        else:
            output = output.replace('、', '，')
            output = output.replace('。', '．')

    if not(output==""):
        st.subheader("翻訳結果")
        st.code(output, language='markdown', line_numbers=True)

if __name__ == '__main__':
    main()
