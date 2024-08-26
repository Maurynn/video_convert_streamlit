import streamlit as st
from moviepy.editor import *
import tempfile
import os
from yt_dlp import YoutubeDL
from time import sleep
from yt_dlp.utils import DownloadError

# Configuração da página

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
    #MainMenu {
        visibility: hidden;
    }#
    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Home", "Ajuda"])

with tab1:
    st.image("Imagens/pytube-down.png")
    st.divider()
    youtube_link = st.text_input('Insira um link do YouTube e aperte Enter:', placeholder="Cole o link aqui.", help="Clique em compartilhar no vídeo do YouTube e copie o link que será colado aqui... Também funciona com vídeos do Facebook.")
    video_file = st.file_uploader("Carregue um arquivo de vídeo:", type=['mp4', 'mov', 'avi', 'flv', 'wmv'],help="Selecione o vídeo que deseja converter para áudio.")

    def download_youtube_video(url):
        try:
            ydl_opts = {'outtmpl': 'downloaded_videos/%(title)s.%(ext)s'}
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                video_url = ydl.prepare_filename(info_dict)
                return video_url
        except DownloadError:
            st.error("⚠️ Ocorreu um erro ao tentar baixar o vídeo. Por favor, para evitar possíveis erros, clique em compartilhar na página do YouTube e copie o link gerado... Se o erro persistir, tente outro link.")
            return None

    if video_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False) 
        tfile.write(video_file.read())
        
        video_clip = VideoFileClip(tfile.name)

        if st.button('Converter para MP3'):
            with st.spinner('Convertendo Vídeo...'):
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
                with st.spinner('Convertendo Vídeo do YouTube...'):
                    audio_clip = video_clip.audio
                    audio_file = f"{video_file_path}.mp3"
                    audio_clip.write_audiofile(audio_file)
                    audio_data = open(audio_file, 'rb').read()
                    st.audio(audio_data, format='audio/mp3')
                    st.info('Áudio pronto para download, clique no botão abaixo:')
                    st.download_button(label="Download YouTube MP3", data=audio_data, file_name="youtube_output.mp3", mime="audio/mpeg")

            if st.button('Download Vídeo do YouTube'):
                with st.spinner('Preparando vídeo do YouTube para download...'):
                    sleep(3)
            
                    video_data = open(video_file_path, 'rb').read()

                    st.info('Video pronto para download, clique no botão abaixo:')
                    st.download_button(label="Clique aqui para baixar o vídeo", data=video_data, file_name="youtube_video.mp4", mime="video/mp4")

    st.divider()
    st.markdown("Developed by: Mauro Alves®")
    
    st.markdown("""
        <a href="https://github.com/Maurynn" target="_blank" style="margin-right: 15px; text-decoration: none">
        <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="Github logo" width="25" height="25">
        </a>
        <a href="https://linkedin.com/in/maurosp" target="_blank" style="margin-right: 15px; text-decoration: none">
        <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" alt="LinkedIn logo" width="25" height="25">
        </a>
        <a href="https://instagram.com/maurinn?igshid=ZDc4ODBmNjlmNQ==" target="_blank" style="margin-right: 15px; text-decoration: none">
        <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram logo" width="25" height="25">
        </a>
        <a href="https://wa.me/5511952483074" target="_blank" style="margin-right: 15px; text-decoration: none">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp logo" width="25" height="25">
        </a>
    """, unsafe_allow_html=True)


    #"[View the source code](https://github.com/Maurynn/video_convert_streamlit/blob/main/app.py)"

with tab2:
    st.header("Instruções de uso:")
    st.write("""
    1. **Envie um arquivo de vídeo:** Clique no botão "Enviar um arquivo de vídeo" e escolha um arquivo de vídeo do seu dispositivo em um dos formatos suportados (.mp4, .mov, .avi, .flv, . wmv).
    
     2. **Inserir um link do YouTube:** Se preferir, você pode simplesmente inserir o link do vídeo do YouTube no campo de entrada "Inserir um link do YouTube".
    
     3. **Converter para MP3:** Após enviar o arquivo de vídeo ou inserir o link do YouTube, clique no botão "Converter para MP3".  O vídeo será convertido em um arquivo de áudio MP3.
    
     4. **Download de MP3:** Após a conversão, um botão "Baixar MP3" aparecerá.  Clique nele para baixar o arquivo de áudio MP3 para o seu dispositivo.
    
     5. **Download de vídeo:** Se você inseriu um link do YouTube, também poderá baixar o vídeo original clicando no botão "Baixar vídeo".
    
     Se você tiver alguma dúvida ou problema, entre em contato com o suporte.
     E-mail: mauro.mn@hotmail.com
    """)
