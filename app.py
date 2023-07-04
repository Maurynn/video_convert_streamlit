import streamlit as st
from moviepy.editor import *
import tempfile
import os
from yt_dlp import YoutubeDL
from time import sleep
from yt_dlp.utils import DownloadError
from googletrans import Translator

# Configuração da página
st.set_page_config(layout="wide")

st.markdown("""
<style>
    .big-font {
        font-family: serif;
        font-size:35px !important;
        font-weight: bold;
        text-align: center;
        color: LightGray;
        border: 1px solid black;
        text-shadow: 2px 2px 2px grey;
    }
</style>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Home", "Ajuda"])

with tab1:
    st.image("Imagens/IMG_20230630_110827.png")
    #st.markdown('<h1 class="big-font">📽️ VIDEO CONVERTER ONLINE 🎶</h1>', unsafe_allow_html=True)
    st.divider()
    youtube_link = st.text_input('Insira um link do YouTube e aperte Enter:', placeholder="Cole o link aqui.", help="Clique em compartilhar no vídeo do YouTube e copie o link que será colado aqui... Também funciona com vídeos do Facebook.")
    video_file = st.file_uploader("Carregue um arquivo de vídeo:", type=['mp4', 'mov', 'avi', 'flv', 'wmv'],help="Selecione o arquivo de vídeo que você deseja converter para áudio.")

    def download_youtube_video(url):
        try:
            ydl_opts = {'outtmpl': 'downloaded_videos/%(title)s.%(ext)s'}
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                video_url = ydl.prepare_filename(info_dict)
                return video_url
        except DownloadError:
            st.error("⚠️ Ocorreu um erro ao tentar baixar o vídeo. Por favor, para evitar possíveis erros, clique em compartilhar na página do YouTube e copie o Link gerado... Caso persista o erro, tente um outro link...")
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

            if st.button('Converter vídeo para MP3'):
                with st.spinner('Convertendo vídeo do YouTube...'):
                    audio_clip = video_clip.audio
                    audio_file = f"{video_file_path}.mp3"
                    audio_clip.write_audiofile(audio_file)
                    audio_data = open(audio_file, 'rb').read()
                    st.audio(audio_data, format='audio/mp3')
                    st.info('Áudio pronto para download, Clique no botão abaixo:')
                    st.download_button(label="Download YouTube MP3", data=audio_data, file_name="youtube_output.mp3", mime="audio/mpeg")

            if st.button('Download YouTube Video'):
                with st.spinner('Preparando vídeo do YouTube para download...'):
                    sleep(3)
            
                    video_data = open(video_file_path, 'rb').read()

                    st.info('Vídeo pronto para download, Clique no botão abaixo:')
                    st.download_button(label="Clique aqui para baixar o vídeo ", data=video_data, file_name="youtube_video.mp4", mime="video/mp4")

    st.divider()
    st.markdown("Developed by: Mauro Alves")
    "[View the source code](https://github.com/Maurynn/video_convert_streamlit/blob/main/app.py)"

with tab2:
    st.header("Instruções de uso:")
    st.write("""
    1. **Carregar um arquivo de vídeo:** Clique no botão "Carregar um arquivo de vídeo" e escolha um arquivo de vídeo do seu dispositivo em um dos formatos suportados (.mp4, .mov, .avi, .flv, .wmv).
    
    2. **Inserir um link do YouTube:** Se você preferir, pode simplesmente inserir o link do vídeo do YouTube no campo de entrada "Insira um link do YouTube".
    
    3. **Converter para MP3:** Após carregar o arquivo de vídeo ou inserir o link do YouTube, clique no botão "Converter para MP3". O vídeo será convertido em um arquivo de áudio MP3.
    
    4. **Download de MP3:** Após a conversão, um botão "Download MP3" aparecerá. Clique nele para baixar o arquivo de áudio MP3 para o seu dispositivo.
    
    5. **Download de vídeo:** Se você inseriu um link do YouTube, também poderá baixar o vídeo original clicando no botão "Download vídeo".
    
    Se você tiver qualquer dúvida ou problema, entre em contato com o suporte.
    Email: mauro.mn@hotmail.com
    """)
