import streamlit as st
from moviepy.editor import *
import tempfile
import os
from yt_dlp import YoutubeDL
from time import sleep
from yt_dlp.utils import DownloadError
st.image("imagens/pngwing.com.png")
st.set_page_config(layout='wide')

st.markdown("""
<style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
        text-align: center;
        color: cyan;
        text-shadow: 2px 2px 2px grey;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="big-font">📽️ VIDEO CONVERTER ONLINE 🎶</h1>', unsafe_allow_html=True)
st.markdown("___")


youtube_link = st.text_input('Insira um link do YouTube e aperte Enter:', help="Clique em compartilhar no vídeo do YouTube e copie o link que será colado aqui... Também funciona com vídeos do Facebook.")

video_file = st.file_uploader("Carregue um arquivo de vídeo:", type=['mp4', 'mov', 'avi', 'flv', 'wmv'],help="Selecione o arquivo de vídeo que você deseja converter para áudio.")

def download_youtube_video(url):
    try:
        ydl_opts = {'outtmpl': 'downloaded_videos/%(title)s.%(ext)s'}
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_url = ydl.prepare_filename(info_dict)
            return video_url
    except DownloadError:
        st.error("Ocorreu um erro ao tentar baixar o vídeo. Por favor, verifique o link e tente novamente ou insira um novo link..")
        return None

if video_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(video_file.read())
    
    video_clip = VideoFileClip(tfile.name)

    if st.button('Converter para MP3'):
        with st.spinner('Convertendo vídeo...'):
            audio_clip = video_clip.audio
            audio_file = f"{tfile.name}.mp3"
            audio_clip.write_audiofile(audio_file)
            audio_data = open(audio_file, 'rb').read()
            st.audio(audio_data, format='audio/mp3')
            st.download_button(label="Download MP3", data=audio_data, file_name="output.mp3", mime="audio/mpeg")

if youtube_link:
    video_file_path = download_youtube_video(youtube_link)
    if video_file_path is not None:
        video_clip = VideoFileClip(video_file_path)
        st.video(video_file_path)

        if st.button('Converter YouTube para MP3'):
            with st.spinner('Convertendo vídeo do YouTube...'):
                audio_clip = video_clip.audio
                audio_file = f"{video_file_path}.mp3"
                audio_clip.write_audiofile(audio_file)
                audio_data = open(audio_file, 'rb').read()
                st.audio(audio_data, format='audio/mp3')
                st.download_button(label="Download YouTube MP3", data=audio_data, file_name="youtube_output.mp3", mime="audio/mpeg")

        if st.button('Download YouTube Video'):
            with st.spinner('Preparando vídeo do YouTube para download...'):
                sleep(3)
                video_data = open(video_file_path, 'rb').read()
                
                st.info('Vídeo pronto para download, Clique no botão abaixo:')
                st.download_button(label="Clique aqui para baixar o vídeo ", data=video_data, file_name="youtube_video.mp4", mime="video/mp4")

st.markdown("___")
st.markdown("Developed by: Mauro Alves")
