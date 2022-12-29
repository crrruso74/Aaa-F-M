echo "Cloning Repo, Please Wait..."
git clone -b master https://github.com/Zk-Bots/Link-Search-koyeb.git /Link-Search-koyeb
cd /Link-Search-koyeb
echo "Installing Requirements..."
pip3 install -U -r requirements.txt
echo "Starting Bot, Please Wait..."
python3 bot.py
