import streamlit as st
from translation import translate



st.sidebar.title('日英翻訳アプリ')
st.sidebar.write('日本語の文章を英語に翻訳します。')
st.sidebar.write('')
st.sidebar.write('右の枠に日本語の文章を入力してください。')

# 内容入力画面
content = st.text_area('日本語の文章を入力してください。')

button = st.button('翻訳開始')

# ボタンが押され、かつ内容が入力されている場合
if button and content is not None:
    with st.spinner('翻訳中...'):
        translated_texts = translate(content)
        st.text_area(
            '翻訳結果',
            value=f'候補1: {translated_texts[0]}\n候補2: {translated_texts[1]}\n候補3: {translated_texts[2]}',
            height=300,
        )
