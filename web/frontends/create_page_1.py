
import streamlit as st
from time import sleep
from backends.settings import Install_server, LOG, ERROR, PROGRESS, SERVERCONFIG
from json import load

server_name = st.text_input('Server name: ')
tunnel_service = st.selectbox('Tunnel service: ',  ('ngrok', 'argo', 'zrok', 'playit', 'localtonet'))
col1, col2, col3 = st.columns(3, vertical_alignment="bottom")
with col1:
  create = st.button('Create', use_container_width= True)
if create == True and server_name != '':
  st.warning('Please do not change the server_name during creating new server.')
  serverconfig = load(open(SERVERCONFIG))
  serverconfig['server_list'] += [server_name]
  serverconfig['server_in_use'] = server_name
  if serverconfig['ngrok_proxy'] == {"authtoken": "", "region": ""} and tunnel_service == 'ngrok':
    LOG('Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken')
    serverconfig['ngrok_proxy']['authtoken'] = st.text_input('Your authtoken: ')
    LOG('Available Regions:', ' ap - Asia/Pacific (Singapore)', ' au - Australia (Sydney)', ' eu - Europa (Frankfurt - Germany)', ' in - India (Mumbai)', ' jp - Japan (Tokyo)', ' sa - America (São Paulo - Brazil)', ' us - United States (Ohio)')
    serverconfig['ngrok_proxy']['region'] = st.text_input('Region: ')
  elif tunnel_service == 'zrok' and serverconfig['zrok_proxy'] == {'authtoken': ''}:
    serverconfig['zrok_proxy']['authtoken'] = st.text_input('Your zrok token: ')
  elif tunnel_service == 'localtonet' and serverconfig['localtonet_proxy'] == {'authtoken': ''}:
    LOG('Get your authtoken from https://localtonet.com/usertoken')
    serverconfig['localtonet_proxy']['authtoken'] = st.text_input('Your localtonet token: ')
  Install_server(server_name = server_name, server_type  = "vanilla" , version = 'vanilla - latest_version', tunnel_service = tunnel_service)
  PROGRESS()
  if 'server_in_use' not in st.session_state:
    st.session_state['server_in_use'] = server
  st.session_state['server_in_use'] = server
  sleep(1)
  st.switch_page(st.Page('frontends/main_page.py'))
with col2:
  if st.button('Exit to login page', use_container_width= True):
    st.switch_page(st.Page('frontends/choose_server.py'))
with col3:
  if st.button('Exit to main page', use_container_width= True):
    st.switch_page(st.Page('frontends/main_page.py'))
