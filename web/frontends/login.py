import streamlit as st
from backends.settings import drive_path, SERVERCONFIG, ERROR, PROGRESS
from random import choices
from string import ascii_letters
from os.path import exists
from json import load, dump
from time import sleep

if st.session_state['login'] == True: st.switch_page(st.Page('frontends/choose_server.py'))
else:
  placeholder = st.container()
  user = load(open('/content/drive/MyDrive/streamlit-app/user.txt'))
  if user == {"choose": True, "user": {"authtoken": ""}}: text = 'Sign up'
  else: text = 'Log in'
  placeholder.title(text)
  choice = placeholder.text_input('Username: ', value='')
  password = placeholder.text_input('Password: ', value='')

  tmp, col2 = st.columns([9, 1], vertical_alignment='top')
  with col2:
    button = st.button(text, use_container_width=True)

  if button:
    if choice == '' or password == '':
      ERROR('Please enter user name and password')
    else:
      if user == {"choose": True, "user": {"authtoken": ""}}:
        authtoken = ''.join(choices(ascii_letters, k=20))
        st.write(f'Your owner authtoken: {authtoken}')
        user['user']['authtoken'] = authtoken
        dump(user, open('/content/drive/MyDrive/streamlit-app/user.txt', 'w'))
        sleep(5)
        st.session_state['permission']['owner'] = True
        user['user'][choice] = [password, st.session_state['permission']]
        dump(user, open('/content/drive/MyDrive/streamlit-app/user.txt', 'w'))
        sleep(5)
        st.session_state['login'] = True
        PROGRESS()
        st.switch_page(st.Page('frontends/choose_server.py'))
      elif choice in user['user']:
        if user['user'][choice][0] == password or user['user'][choice][0] == '':
          if user['user'][choice][1]['owner'] == True:
            authtoken = placeholder.text_input('Your authtoken: ')
            if authtoken == user['user']['authtoken']:
              st.session_state['permission']['owner'] = True
              st.session_state['login'] = True
              PROGRESS()
              st.switch_page(st.Page('frontends/choose_server.py'))
          else:
            st.session_state['login'] == True
            st.session_state['permission'] = user['user'][choice][1]
        else:
          ERROR('Invalid username or password')
      else:
        ERROR('Invalid username or password')
