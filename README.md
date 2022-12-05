A simple yet trustworthy security system for your Discord server
# What does it do?
This simple bot will ask any user who joins your server to verify and solve an easy math problem to gain full access to your server. This will prevent bots and raiders from gaining access to your server.
# How to set it up
Setting up this bot is very easy, just follow these steps:
1. Clone the repository to your computer
2. Install `requirements.txt` using `pip install -r requirements.txt` in the shell
3. Edit the `.env` file and replace `YourToken` with your bot's token
4. Edit the `config.json` file to your liking
5. Run the command `/verify` in the channel you wish for users to come to verify
6. Enjoy!
# FAQ
**Why does `sessions.json` have a random session ongoing?**  
That's what we call a "dummy session" and without it Python will not load the file properly. So don't delete that session.

**Can I edit this code?**  
Yes, you can! This code is not trademarked, so you may edit this code to your liking as long as you follow the `LICENCE` file!

**I found a bug, how do I report it?**  
Just let me know by opening an issue and I'll try to tackle it as soon as I can!
