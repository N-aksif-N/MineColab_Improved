import streamlit as st
from json import load

path = ''
serverconfig = load(open(f'{path}/content/drive/My Drive/minecraft/serverconfig.txt'))
pg = st.navigation([st.Page("frontends/login.py"), st.Page('frontends/choose_server.py'), st.Page('frontends/main_page.py'), st.Page('frontends/create_page_1.py')], position= 'hidden')
if 'Starting' not in st.session_state:
  st.session_state['Starting'] = {}
  for server in serverconfig['server_list']:
    st.session_state['Starting'][server] = ['Start', False]
if 'ip' not in st.session_state:
  st.session_state['ip'] = '___ Run Your Server ___'
st.set_page_config(page_title='Minecolab', page_icon="https://raw.githubusercontent.com/N-aksif-N/MineColab/master/minecolab.png", layout='wide')
pg.run()
