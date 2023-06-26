import streamlit as st
from moviepy.editor import *
import tempfile
import os
from yt_dlp import YoutubeDL
from time import sleep
from yt_dlp.utils import DownloadError

st.set_page_config(layout='wide')

st.markdown("<h1 style='text-align: center; color: orange;'>📽️ Video Converter 🎶</h1>", unsafe_allow_html=True)

if st.sidebar.checkbox('Mostrar instruções de uso'):
    st.sidebar.write("""
    1. **Carregar um arquivo de vídeo:** Clique no botão "Carregar um arquivo de vídeo" e escolha um arquivo de vídeo do seu dispositivo em um dos formatos suportados (.mp4, .mov, .avi, .flv, .wmv).
    
    2. **Inserir um link do YouTube:** Se você preferir, pode simplesmente inserir o link do vídeo do YouTube no campo de entrada "Insira um link do YouTube".
    
    3. **Converter para MP3:** Após carregar o arquivo de vídeo ou inserir o link do YouTube, clique no botão "Converter para MP3". O vídeo será convertido em um arquivo de áudio MP3.
    
    4. **Download de MP3:** Após a conversão, um botão "Download MP3" aparecerá. Clique nele para baixar o arquivo de áudio MP3 para o seu dispositivo.
    
    5. **Download de vídeo:** Se você inseriu um link do YouTube, também poderá baixar o vídeo original clicando no botão "Download vídeo".
    
    Se você tiver qualquer dúvida ou problema, entre em contato com o suporte.
    """)

video_file = st.file_uploader("Carregue um arquivo de vídeo", type=['mp4', 'mov', 'avi', 'flv', 'wmv'])

youtube_link = st.text_input('Ou, insira um link do YouTube e aperte Enter.')

def download_youtube_video(url, is_playlist=False):
    try:
        ydl_opts = {'outtmpl': 'downloaded_videos/%(title)s.%(ext)s'}
        if is_playlist:
            ydl_opts['noplaylist'] = False
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            if is_playlist:
                return [entry['webpage_url'] for entry in info_dict['entries']]
            else:
                video_url = ydl.prepare_filename(info_dict)
                return video_url
    exceptDesculpe pelo erro de formatação. Aqui está o final do código:

```python
    except DownloadError:
        st.error("Erro ao baixar o vídeo do YouTube. Por favor, verifique o link e tente novamente.")
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
    is_playlist = st.checkbox("É uma playlist?")
    video_file_paths = download_youtube_video(youtube_link, is_playlist)
    if video_file_paths is not None:
        for video_file_path in video_file_paths:
            video_clip = VideoFileClip(video_file_path)
            st.video(video_file_path)

            if st.button(f'Converter YouTube para MP3 - {video_file_path}'):
                with st.spinner('Convertendo vídeo do YouTube...'):
                    audio_clip = video_clip.audio
                    audio_file = f"{video_file_path}.mp3"
                    audio_clip.write_audiofile(audio_file)
                    audio_data = open(audio_file, 'rb').read()
                    st.audio(audio_data, format='audio/mp3')
                    st.download_button(label="Download YouTube MP3", data=audio_data, file_name="youtube_output.mp3", mime="audio/mpeg")

            if st.button(f'Download YouTube Video - {video_file_path}'):
                with st.spinner('Preparando vídeo do YouTube para download...'):
                    sleep(3)
                    video_data = open(video_file_path, 'rb').read()
                    
                    st.info('Vídeo pronto para download, Clique no botão abaixo:')
                    st.download_button(label="Clique aqui para baixar o vídeo ", data=video_data, file_name="youtube_video.mp4", mime="video/mp4")
