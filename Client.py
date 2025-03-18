import asyncio
import sys
import Utils
from tkinter import filedialog
import os

from CommonClient import ClientCommandProcessor, CommonContext, gui_enabled, logger, server_loop, get_base_parser

class SS2CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

class SS2Context(CommonContext):
    command_processor = SS2CommandProcessor
    game = "System Shock 2"
    items_handling = 0b111  # full remote



    def __init__(self, server_address, password):
        super(SS2Context, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        self.seed = 0
        self.is_connected = False

        self.SS2DirPath = filedialog.askdirectory(title="Select System Shock 2 installation folder", mustexist = True)
        self.recieved_items_file = os.path.join(self.SS2DirPath + "/DMM/Archipelago/data/ReceivedItems.txt")
        self.sent_items_file = os.path.join(self.SS2DirPath + "/DMM/Archipelago/data/SentItems.txt")
        self.settings_file = os.path.join(self.SS2DirPath + "/DMM/Archipelago/data/Settings.txt")

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.auth = None
        await super().disconnect(allow_autoreconnect)

    async def server_auth(self, password_requested: bool = False):
        # This is called to autentificate with the server.
        if password_requested and not self.password:
            await super(SS2Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        self.is_connected = False
        await super(SS2Context, self).connection_closed()

    # Do not touch this
    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        open(self.recieved_items_file, "w").close()
        open(self.sent_items_file, "w").close()
        open(self.settings_file, "w").close()
        await super(SS2Context, self).shutdown()

    def on_package(self, cmd: str, args: dict):
        if cmd in {"RoomInfo"}:
            self.seed = args["seed_name"]

        if cmd in {"Connected"}:
            with open(self.recieved_items_file, "w") as f:
                f.write(str(self.seed) + ",")

            with open(self.sent_items_file, "w") as f:
                f.write(args["checked_locations"])

            with open(self.settings_file, "w") as f:
                f.write(str(self.seed) + ",")
                f.write(args["slot_info"]["options"])

            self.is_connected = True

        if cmd in {"ReceivedItems"}:
            with open(self.recieved_items_file, "a") as f:
                for item in args["items"]:
                    f.write(item["item"] + ",")
    
    def run_gui(self):
        from kvui import GameManager

        class SS2Manager(GameManager):
            base_title = "Archipelago System Shock 2 Client"

        self.ui = SS2Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

def print_error_and_close(msg):
    logger.error("Error: " + msg)
    Utils.messagebox("Error", msg, error=True)
    sys.exit(1)

async def loc_watcher(ctx):
    while True:
        if ctx.is_connected:
            locs = []
            with os.scandir(ctx.SS2DirPath) as entries:
                for entry in entries:
                    if "pylocid" in entry.name:
                        if entry.name == "pylocid2.txt":
                            asyncio.create_task(ctx.send_msgs([{"cmd": "StatusUpdate", "status": 30}]))#goal
                            continue
                        locs.append(int(entry.name.replace("pylocid","").replace(".txt", "")))
                        #os.remove(entry.path)
            if locs:
                asyncio.create_task(ctx.send_msgs([{"cmd": "LocationChecks", "locations": locs}]))
        await asyncio.sleep(2)

def launch():
    async def main(args):
        ctx = SS2Context(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        loc_watcher_task = asyncio.create_task(loc_watcher(ctx))
        await loc_watcher_task

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

    parser = get_base_parser()
    args = parser.parse_args()

    import colorama

    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()