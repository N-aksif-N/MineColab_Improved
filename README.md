<p align="center"><a href="https://github.com/thecoder-001/MineColab"><img src="https://github.com/thecoder-001/MineColab/blob/master/Logo.png" alt="Logo" height="80"/></a></p>
<h1 align="center">MineColab</h1>
<p align="center">Run Minecraft Server on Google Colab</p>
<p align="right">
  <a target="_blank" href="https://github.com/N-aksif-N/Minecolab"><img src="https://img.shields.io/github/stars/N-aksif-N/Minecolab.svg?style=social&label=Star" alt="Star"></a>
  <a href="https://colab.research.google.com/drive/1XaKGzktNHVr3o2rf4SuwlkuwDmQapYal?usp=sharing" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
</p>

                                                                                 
# :hear_no_evil:  First of all, what is Mine Colab [Improved]?

Mine Colab [Improved] is an alternative [Minecolab project](https://github.com/thecoder-001/MineColab) that helps to build a Minecraft server on your own Gdrive. It is easier to use and more flexible to edit. This project is suited for mainly [google colab](https://colab.research.google.com) (a free service based on [jupyter notebook](https://jupyter.org/) and [ubuntu](https://ubuntu.com) os), though this can be applied on other projects like [jupyter lab](https://jupyter.org/try-jupyter/lab/), [deepnote](https://deepnote.com/), etc. This project followed the MIT. Before looking closer, please make sure to see [the original](https://github.com/thecoder-001/MineColab)

# :moneybag:  Can Minecolab server online 24/7?

Of course, it's possible but with a little hard work. Google Colab is a free service and it is not suited for 24/7 online so you can use [deepnote](https://deepnote.com/) instead. Or if you still want to use google collab you may need some tricks or friends to make the web online and accept the captcha manually.

# :page_with_curl: Instructions
- Open the notebook in Google Colab.
- RUN THE SET-UP CELL (important)
- Read through the notebook, most of the code is self-explanatory. Run the cells that are useful for your use case.

**Create Minecraft server**
1. Run the cell that creates the Minecraft server.
2. After that, you have three options. You can either use Ngrok, PlayIt, or Cloudflare's Argo. Ngrok is easy to set up and doesn't require anything to be installed by the clients but it can often be quite unreliable. Argo doesn't have such limitations but requires a bit more work. Playit may get bugged at this point but it gives users a static domain and does not require any hard work.
- **[Ngrok](https://ngrok.com)**
  + Follow the prompts.
  + The IP will change whenever you restart the server.
- **[Cloudflare's argo](https://www.cloudflare.com/)** :
    - If the 'Your free tunnel has started!' notification appears => Done.
    - Access to your server: 
    1. Download [Cloudflared client](https://github.com/cloudflare/cloudflared/releases/).
    2. Launch the binary with `<your Cloudflare file name> access tcp --hostname <tunnel_address> --url 127.0.0.1:25565` (note: tunnel_address is your address which has been set on your Cloudflare)
    4. Finally, connect to `127.0.0.1:25565` from the Minecraft client which is located in that machine.
- **[PlayIt](https://playit.gg/)**: follow the prompts.

# :zap:  So, how does it actually work?
Because MInecolab [Improved] is an alternative Minecolab project. Therefore, it has all the main features, which the Minecolab project does: 
 
 1. Update the system's apt-cache.
 2. Install Openjdk-16 (Java) through apt-get.
 3. Mount Google Drive to access the Minecraft folder (Drive is used here to provide persistent storage).
 4. Setup Argo/ngrok/playit Tunnel (Opening a tunnel at port 25565) depending on the `tunnel_service` variable.
 5. Change the directory to the Minecraft server folder on Google Drive ("Minecraft-server" is the default, located in the root directory of my Google Drive.)
 6. List/Print the file list on the screen to indicate successful directory change.
 7. Startup the Minecraft server (with optimized JVM parameters from [Aikar's guide)](https://aikar.co/2018/07/02/tuning-the-jvm-g1gc-garbage-collector-flags-for-minecraft/) and from GC logging

Additionally, Minecolab [Improved] has more new features:

 1. Bug fixed (java error)
 2. Get mod, plugin, mod pack, shaders pack, and data pack from 2 main webs: [modrinth](https://modrinth.com/) and [curseforge](https://www.curseforge.com/minecraft)
 3. Server properties, server MOTD, and server icon configuration.
 4. Logs View.
 5. Server Backup.
 6. Expanded software (forge, fabric, vanilla, snapshot, paper, purpur)
- See all work that has been done, in processed, or what I want to do in the future from **[minecolab improve roadmap](https://github.com/users/N-aksif-N/projects/1)**

## 🐛 Found a bug?

- Report the bug by creating a new issue and use this helpful [issue template](https://github.com/N-aksif-N/MineColab/blob/main/.github/ISSUE_TEMPLATE/bug_report.md).
Or join the Discord: [Minecolab Support](https://discord.gg/uCHcV3SAbs)
- Suggest a new feature using this [template](https://github.com/N-aksif-N/MineColab/blob/main/.github/ISSUE_TEMPLATE/feature_request.md).

## 👍 Notes
- If something does not work, try using a VPN like [windscribe](https://windscribe.com) before opening an issue.
- Switch between the three different tunnel providers and see which works best for you.
- Make regular backups of your world.
- Google Colab is not designed to create Minecraft servers, but it can be done. Google Colab promises to work for 12 hours straight, however, it is possible that if no person is reviewing the page or using the console, basically if the page detects inactivity the process will end. The performance is approximately 12 GB of RAM, together with a processor with a power of 2.2 GHz and 2 threads, this is better than many paid hostings, but it doesn't have support and doesn't promise to be open always
- It is not advisable to fill it with as many as plugins, which is more limited to this server than its own processor, it is not very good, any hosting for 12 USD can offer a higher quality server, if you are thinking of creating something for many users, it's much better.
