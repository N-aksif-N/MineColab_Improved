import streamlit as st
from json import load

pg = st.navigation([st.Page("frontends/login.py"), st.Page('frontends/choose_server.py'), st.Page('frontends/main_page.py'), st.Page('frontends/create_page_1.py'), st.Page('backends/settings.py')], position= 'hidden')
if "disabled" not in st.session_state:
  st.session_state["disabled"] = [False, False]
if 'login' not in st.session_state:
  st.session_state['login'] = False
if 'server_in_use' not in st.session_state:
  serverconfig = load(open('/content/drive/MyDrive/minecraft/server_list.txt'))
  if serverconfig['server_in_use'] != '':
    st.session_state['server_in_use'] = serverconfig['server_in_use']
if 'Starting' not in st.session_state:
  st.session_state['Starting'] = False
if 'start_button' not in st.session_state:
  st.session_state['start_button'] = '▶ Start'
if 'ip' not in st.session_state:
  st.session_state['ip'] = '___ Run Your Server ___'
if 'permission' not in st.session_state:
  st.session_state['permission'] = {'console': False, 'software': False, 'log viewing': False, 'world': False, 'server settings': False, 'owner': False}
st.set_page_config(page_title='Minecolab', page_icon="https://raw.githubusercontent.com/N-aksif-N/MineColab/master/minecolab.png", layout='wide')
pg.run()
