import io
import os
import streamlit as st
import requests
from PIL import Image
from model import get_caption_model, generate_caption
import webbrowser
from gtts import gTTS

def generate_audio(caption):
    tts = gTTS(text=caption, lang='en')
    audio_path = 'caption_audio.mp3'
    tts.save(audio_path)
    return audio_path

@st.cache_resource
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://cdn.pixabay.com/photo/2017/03/02/16/54/iceland-2111811_960_720.jpg");
            background-attachment: fixed;
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_url()

def get_model():
    return get_caption_model()

caption_model = get_model()

def predict():
    captions = []
    pred_caption = generate_caption('tmp.jpg', caption_model)

    st.markdown('#### Predicted Captions:')
    captions.append(pred_caption)

    for _ in range(4):
        pred_caption = generate_caption('tmp.jpg', caption_model, add_noise=True)
        if pred_caption not in captions:
            captions.append(pred_caption)

    for c in captions:
        st.write(c)

    audio_path = generate_audio(c)
    st.audio(audio_path, format='audio/mp3')

st.title('Image Caption Generator')
img_url = st.text_input(label='Enter Image URL')

if (img_url != "") and (img_url != None):
    img = Image.open(requests.get(img_url, stream=True).raw)
    img = img.convert('RGB')
    st.image(img)
    img.save('tmp.jpg')
    predict()
    os.remove('tmp.jpg')

st.markdown('<center style="opacity: 70%">OR</center>', unsafe_allow_html=True)
img_upload = st.file_uploader(label='Upload Image', type=['jpg', 'png', 'jpeg'])

if img_upload is not None:
    img = img_upload.read()
    img = Image.open(io.BytesIO(img))
    img = img.convert('RGB')
    img.save('tmp.jpg')
    st.image(img)
    predict()
    os.remove('tmp.jpg')

st.markdown(""" Meet our team""", unsafe_allow_html=True)
st.markdown("""<a href="https://www.linkedin.com/in/mathews-benny-b29ab8241/">Mathews Benny</a>""", unsafe_allow_html=True)
st.markdown("""<a href="https://www.linkedin.com/in/mhdjaseemek/">MOHAMMED JASEEM EK</a>""", unsafe_allow_html=True)
st.markdown("""<a href="https://www.linkedin.com/in/yedhu-krishnan-495aa8234/">Yedhu krishnan PG</a>""", unsafe_allow_html=True)