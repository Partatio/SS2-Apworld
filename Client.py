import asyncio
from tkinter import filedialog
import os
import sys

import Utils
from NetUtils import ClientStatus
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

        options = Utils.get_options()
        self.ss2_dir_path = os.path.join(options["ss2_options"]["ss2_path"])
        if not os.path.exists(self.ss2_dir_path):
            print_error_and_close("Couldn't find your SS2 installation.")
        if not os.path.exists(os.path.join(self.ss2_dir_path, "DMM", "Archipelago", "data")):
            print_error_and_close("Couldn't find mod, install the SS2 mod before running the client.")
        self.recieved_items_file = os.path.join(self.ss2_dir_path, "DMM", "Archipelago", "data", "ReceivedItems.txt")
        self.sent_items_file = os.path.join(self.ss2_dir_path, "DMM", "Archipelago", "data", "SentItems.txt")
        self.settings_file = os.path.join(self.ss2_dir_path, "DMM", "Archipelago", "data", "Settings.txt")

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
            self.seed = str(args["seed_name"])[:6]

        if cmd in {"Connected"}:
            with open(self.recieved_items_file, "w") as f:
                f.write(str(self.seed) + ",")

            with open(self.sent_items_file, "w") as f:
                f.write("0, ")
                f.write(str(args["checked_locations"]).strip("[]") + ", ")

            with open(self.settings_file, "w") as f:
                f.write(str(self.seed) + ",")
                f.write(str(args["slot_data"]["options"]))

            self.is_connected = True

        if cmd in {"ReceivedItems"}:
            with open(self.recieved_items_file, "a") as f:
                for item in args["items"]:
                    f.write(str(item[0]) + ",")
    
    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Archipelago System Shock 2 Client"
        return ui


def print_error_and_close(msg):
    logger.error("Error: " + msg)
    Utils.messagebox("Error", msg, error=True)
    sys.exit(1)

async def loc_watcher(ctx):
    while not ctx.exit_event.is_set():
        if ctx.is_connected:
            locs = []
            with os.scandir(ctx.ss2_dir_path) as entries:
                for entry in entries:
                    if "pylocid" in entry.name:
                        first_seven = ""
                        with open(entry, "r") as locfile:
                            first_seven = locfile.read(7)
                        if first_seven == "play_cd":
                            if entry.name == "pylocid2.txt":
                                asyncio.create_task(ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]))
                            else:
                                locid = int(entry.name.strip("pylocid.txt"))
                                locs.append(locid)
                                with open(ctx.sent_items_file, "a") as f:
                                    f.write(str(locid) + ", ")
                            os.remove(entry.path)
            if locs:
                asyncio.create_task(ctx.send_msgs([{"cmd": "LocationChecks", "locations": locs}]))
        await asyncio.sleep(0.5)

def launch(*args):
    async def main(args):
        ctx = SS2Context(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        loc_watcher_task = asyncio.create_task(loc_watcher(ctx))

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        ctx.server_address = None

        await loc_watcher_task

        await ctx.shutdown()

    parser = get_base_parser()
    args = parser.parse_args(args)

    import colorama

    colorama.just_fix_windows_console()
    asyncio.run(main(args))
    colorama.deinit()