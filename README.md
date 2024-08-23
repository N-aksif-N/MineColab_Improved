<p align="center"><a href="https://github.com/N-aksif-N/MineColab"><img src="https://raw.githubusercontent.com/N-aksif-N/MineColab/master/MineColab_Improved.png" alt="Logo" height="80"/></a></p>
<h1 align="center">Mine Colab [Improved]</h1>
<p align="center">Run Minecraft Server on Google Colab</p>
<p align="right">
  <a target="_blank" href="https://discord.gg/F9nPJTn7Nu"><img src="https://discordapp.com/api/guilds/1214801871827501097/widget.png?style=shield" alt="Discord Minecolab Support"></a>
  <a target="_blank" href="https://github.com/N-aksif-N/Minecolab"><img src="https://img.shields.io/github/stars/N-aksif-N/Minecolab.svg?style=social&label=Star" alt="Star"></a>
  <a href="https://colab.research.google.com/github/N-aksif-N/MineColab_Improved/blob/free-config/MineColabImproved.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
  <a href="https://github.com/N-aksif-N/MineColab_Improved/releases/download/0.1.6/MinecolabImproved.ipynb" target="_parent"><img src="https://cdn-icons-png.flaticon.com/128/10741/10741247.png" alt="Download" width="20" height="20"></a> 
</p>

<details>
  <summary>Table of content</summary>
  
  - [ :hear_no_evil: What is Minecolab_Improved?](https://github.com/N-aksif-N/MineColab_Improved/tree/master/?tab=readme-ov-file#hear_no_evil--first-of-all-what-is-mine-colab-improved)
  - [ :moneybag: Can Minecolab server online 24/7?](https://github.com/N-aksif-N/MineColab_Improved/tree/master/?tab=readme-ov-file#moneybag--can-minecolab-server-online-247)
  - [ :page_with_curl: Instructions](https://github.com/N-aksif-N/MineColab_Improved/tree/master/?tab=readme-ov-file#page_with_curl-instructions)
  - [ :zap: How does Minecolab actually work?](https://github.com/N-aksif-N/MineColab_Improved/tree/master/?tab=readme-ov-file#zap--so-how-does-it-actually-work)
  - [ 🔮 License](https://github.com/N-aksif-N/MineColab_Improved/tree/master/?tab=readme-ov-file#-license)
  - [ 🐛 Found a bug?](https://github.com/N-aksif-N/MineColab_Improved/tree/master/?tab=readme-ov-file#-found-a-bug)
  - [ 👍 Notes](https://github.com/N-aksif-N/MineColab_Improved/tree/master/?tab=readme-ov-file#-notes)
</details>
                                                                                 
# :hear_no_evil:  First of all, what is Mine Colab [Improved]?

Mine Colab [Improved] is an alternative [Minecolab project](https://github.com/thecoder-001/MineColab) that helps to build a Minecraft server on your own Gdrive. It is easier to use and more flexible to edit. This project is suited for mainly [google colab](https://colab.research.google.com) (a free service based on [jupyter notebook](https://jupyter.org/) and [ubuntu](https://ubuntu.com) os), though this can be applied on other projects like [jupyter lab](https://jupyter.org/try-jupyter/lab/), [deepnote](https://deepnote.com/), etc. This project followed the [GNU License](https://github.com/N-aksif-N/Minecolab/blob/master/LICENSE). Before looking closer, please make sure to see [the original](https://github.com/thecoder-001/MineColab)

# :moneybag:  Can Minecolab server online 24/7?

Of course, it's possible but with a little hard work. Google Colab is a free service and it is not suited for 24/7 online so you can use [deepnote](https://deepnote.com/) instead. Or if you still want to use google collab you may need some tricks or friends to make the web online and accept the captcha manually.

# :page_with_curl: Instructions
- Open the notebook in Google Colab.
- RUN THE SET-UP CELL (important)
- Read through the notebook, most of the code is self-explanatory. Run the cells that are useful for your use case.

**Create Minecraft server**
1. Run the cell that creates the Minecraft server.
2. After that, you have five options. You can either use Ngrok, PlayIt, or Cloudflare's Argo. Ngrok, Localtonet is easy to set up and doesn't require anything to be installed by the clients but it can often be quite unreliable. Argo doesn't have such limitations but requires a bit more work. Playit, Zrok may get bugged at this point but it is more reliable and does not require any hard work.
   
- **[Ngrok](https://ngrok.com)**
  + Follow the prompts.
  + The IP will change whenever you restart the server.
- **[Cloudflare's argo](https://www.cloudflare.com/)** :
    - If the 'Your free tunnel has started!' notification appears => Done.
    - Access to your server:
    1. Download [Cloudflared client](https://github.com/cloudflare/cloudflared/releases/).
    2. Launch the binary with `<your Cloudflare file name> access tcp --hostname <tunnel_address> --url 127.0.0.1:25565` (note: tunnel_address is your address which has been set on your Cloudflare).
    4. Finally, connect to `127.0.0.1:25565` from the minecraft client which is located in that machine.

- **[Localtonet](https://localtonet.com/)**:
  
  1. Navigate to [TCP-UDG](https://localtonet.com/tunnel/tcpudp) page. Select TCP in Protocol Types.
  2. Get your authtoken from [Authtoken](https://localtonet.com/usertoken).
  3. Pick the server you'd like your tunnel to operate on.
  4. Input the IP and Port values the tunnel will listen to, in this case, for Minecraft, it's typically IP: 127.0.0.1 and Port: 25565.
  5. Finally, create and start your tunnel by pressing the Start button.

  - Read more on [how-to-use-localtonet-with-minecraft](https://localtonet.com/documents/using-localtonet-with-minecraft)
  
- **[Zrok](https://zrok.io/)**: 
  1. Download the zrok app through [link](https://docs.zrok.io/docs/getting-started/)
  2. Open the shell. Type `zrok invite` to sign up and get the authtoken
  3. Follow the prompts

- **[PlayIt](https://playit.gg/)**: follow the prompts.

# :zap:  So, how does it actually work?
MInecolab [Improved] is an alternative Minecolab project. Therefore, it has all the main features, which the Minecolab project does: 
 
 1. Update the system's apt-cache.
 2. Install Openjdk-8 (For Minecraft versions below 1.17) or Openjdk-17 (For Minecraft versions over or in 1.17) through apt-get.
 3. Mount Google Drive to access the Minecraft folder (Drive is used here to provide persistent storage).
 4. Setup Argo/ngrok/playit Tunnel (Opening a tunnel at port 25565) depending on the `tunnel_service` variable.
 5. Change the directory to the Minecraft server folder on Google Drive ("Minecraft-server" is the default, located in the root directory of your Google Drive.)
 6. List/Print the file list on the screen to indicate successful directory change.
 7. Startup the Minecraft server (with optimized JVM parameters from [Aikar's guide)](https://aikar.co/2018/07/02/tuning-the-jvm-g1gc-garbage-collector-flags-for-minecraft/) and from GC logging

Additionally, Minecolab [Improved] has more new features:

1. Bug Fixes: Mine Colab [Improved] addresses issues like Java errors, connection disruptions, and missing files, ensuring a smoother experience.
2. Performance Improvements: The project has been optimized for better performance, making it more efficient.
3. Mod and Plugin Support: You can now easily integrate mods, plugins, and mod packs from two primary sources: Modrinth and CurseForge.
4. Server Configuration:
    - Server Properties: Customize server properties such as game rules, difficulty, and world settings.
    - Server MOTD (Message of the Day): Describe the server, promote features, create announcements, attract attention.
5. Server Icon Configuration: Choose an icon to represent your server visually.
6. Logs Viewing: Access and review server logs to troubleshoot issues or monitor server activity.
7. Server Backup: Create backups of your server data in zip files, ensuring data safety.
8. Expanded Software Support:
    - Forge: Use the popular Forge modding platform.
    - Fabric: Opt for the lightweight Fabric mod loader.
    - Vanilla: Run a vanilla Minecraft server.
    - Snapshot: Experiment with the latest Minecraft snapshots.
    - Paper: Utilize the Paper server software.
    - Purpur: Explore the Purpur server implementation.
    - Arclight: Try out the Arclight server software.
    - Mohist: Use Mohist, which combines Forge and Fabric.
    - Banner: Deploy a Banner server.
    - Velocity: Set up a Velocity proxy server.
        
## 🔮 **License:**   
[![License](https://camo.githubusercontent.com/966484ce4d3faab2d9803e7354431ff8e4fce6a424e97689f05b2f50f4ee424b/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f497a7a656c416c697a2f4172636c696768743f7374796c653d666c61742d737175617265)](https://github.com/N-aksif-N)

## 🐛 Found a bug?

- Report the bug by creating a new issue and use this helpful [issue template](https://github.com/N-aksif-N/MineColab/blob/main/.github/ISSUE_TEMPLATE/bug_report.md).
Or join the Discord: [Minecolab Support](https://discord.gg/uCHcV3SAbs)
- Suggest a new feature using this [template](https://github.com/N-aksif-N/MineColab/blob/main/.github/ISSUE_TEMPLATE/feature_request.md).
- See all work that has been done, in processed, or what I want to do in the future from **[minecolab improve roadmap](https://github.com/users/N-aksif-N/projects/1)**

## 👍 Notes
- Please use the FUNCTION in the notebook unless you want any ERRORS/BUGS.
- If something does not work, try using a VPN like [windscribe](https://windscribe.com) before opening an issue.
- Switch between the three tunnel providers and see which works best.
- Make regular backups of your world.
- Google Colab is not designed to create Minecraft servers, but it can be done. Google Colab promises to work for 12 hours straight, however, it is possible that if no person is reviewing the page or using the console, basically if the page detects inactivity the process will end. The performance is approximately 12 GB of RAM, together with a processor with a power of 2.2 GHz and 2 threads, this is better than many paid hostings, but it doesn't have support and doesn't promise to be open always
- It is not advisable to fill it with as many as plugins, which is more limited to this server than its own processor, it is not very good, any hosting for 12 USD can offer a higher quality server, if you are thinking of creating something for many users, it's much better.

[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://github.com/N-aksif-N)
