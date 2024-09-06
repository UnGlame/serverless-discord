import os

import requests

APP_ID = "1261684098397896756"
TEST_SERVER_ID = "1261685035594154014"
EYY_SERVER_ID = "262072069536088065"
BOT_TOKEN = os.environ["DST_BOT_TOKEN"]

# global commands are cached and only update every hour
url = f"https://discord.com/api/v10/applications/{APP_ID}/commands"

# while server commands update instantly
# they're much better for testing
# test_url = f"https://discord.com/api/v10/applications/{APP_ID}/guilds/{TEST_SERVER_ID}/commands"
# eyy_url = f"https://discord.com/api/v10/applications/{APP_ID}/guilds/{EYY_SERVER_ID}/commands"

# Commands
json = [
    {"name": "dststart", "description": "Start the DST server.", "options": []},
    {"name": "dststop", "description": "Stop the DST server.", "options": []},
    {"name": "dstsave", "description": "Save the DST server.", "options": []},
]

response = requests.put(
    url, headers={"Authorization": f"Bot {BOT_TOKEN}"}, json=json, timeout=10
)

# response = requests.put(
#     eyy_url, headers={"Authorization": f"Bot {BOT_TOKEN}"}, json=json, timeout=10
# )

print(response.json())
