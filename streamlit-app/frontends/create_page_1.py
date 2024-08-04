import streamlit as st
from time import sleep
from backends.settings import Install_server, PROGRESS, SET_SERVERCONFIG, USER, drive_path
from json import load, dump
from os import listdir

user = load(open(USER)); uid = dict(st.context.headers); user_name = ''
del uid['Sec-Websocket-Key']
uid = str(uid)
for user_ in user['user']:
  if user_ != 'authtoken':
    if uid in user['user'][user_]['user_id']: 
      if user['user'][user_]['server_in_use'] != '': st.switch_page(st.Page('frontends/main_page.py'))
      user_name = user_; break
if user_name == '': st.switch_page(st.Page('frontends/login.py'))
  
drive_dir = listdir(drive_path); drive_dir.remove('serverconfig.txt');  drive_dir.remove('logs');
divider(label='Creating server:', align='center', color='red')
server_name = st.text_input('Server name: ')
tunnel_service = st.selectbox('Tunnel service: ',  ('ngrok', 'argo', 'zrok', 'playit', 'localtonet'), index=None)
st.subheader('\nExtra options: \n')
divider(label='Extra options:', align='center', color='red')
col1, col2, col3 = st.columns(3, vertical_alignment="bottom")
with col1:
  if st.button('Create', use_container_width= True):
    if server_name != '' and tunnel_service != None:
      if server_name not in drive_dir:
        SET_SERVERCONFIG(tunnel_service, server_name)
        Install_server(server_name = server_name, server_type  = "vanilla" , version = 'vanilla - latest_version', tunnel_service = tunnel_service)
        user['user'][user_name]['server_in_use'] = server_name
        st.session_state['ip'][server] = '___ Run Your Server ___'
        st.session_state['Starting'][server_name] = ['Start', False]
        PROGRESS()
        st.switch_page(st.Page('frontends/main_page.py'))
      else: ERROR('You have created that server. Please give a different minecraft server name.')
with col2:
  if st.button('Exit to login page', use_container_width= True):
    st.switch_page(st.Page('frontends/choose_server.py'))
with col3:
  if st.button('Exit to main page', use_container_width= True):
    if drive_dir == []:
      if user['user'][user_name]['server_in_use'] == '':
        user['user'][user_name]['server_in_use'] = drive_dir[0]
        dump(user, open(USER, 'w'))
        sleep(1)
      st.switch_page(st.Page('frontends/main_page.py'))
st.warning('Please do not change the server_name during creating new server.')
