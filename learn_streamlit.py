# streamlit run c:\Users\xzhouzeng\Desktop\myproject\ACcode\web\Learning-Note\learn_streamlit.py
import streamlit as st
import pandas as pd
import numpy as np
import cv2
st.text('This is some text.')
st.markdown('Streamlit is **_really_ cool**.')
st.write(1234)
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40],
}))
st.json({
    'foo': 'bar',
     'baz': 'boz',
     'stuff': [
         'stuff 1',
         'stuff 2',
        'stuff 3',
         'stuff 5',
    ],
})
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])
st.line_chart(chart_data)

if st.button('Say hello'):
    st.write('Why hello there')
agree = st.checkbox('I agree')


option = st.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone'))

st.write('You selected:', option)

age = st.slider('How old are you?', 0, 130, 25)
st.write("I'm ", age, 'years old')

siderbar = st.sidebar
siderbar.markdown('我是一个sidebar')
image = cv2.imread('000000000785.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
print(image.shape)
st.image(image, caption='1',
        use_column_width=True)
# cap = cv2.VideoCapture("Arrow_step.mp4")
# while cap.isOpened():
#     ret, image = cap.read()
    
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     st.image(image, caption='1',
#          use_column_width=True)

# cap.release()