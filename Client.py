import asyncio
from tkinter import filedialog
import os
import sys
import psutil
from time import time

import Utils
from NetUtils import ClientStatus
from CommonClient import ClientCommandProcessor, CommonContext, gui_enabled, logger, server_loop, get_base_parser

death_link_enabled = False
death_link_toggle = False
class SS2CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_deathlink(self):
        "Toggles Death Link, if Death Link was not enabled as an option this does nothing."
        global death_link_enabled
        global death_link_toggle
        if death_link_enabled:
            if death_link_toggle:
                death_link_toggle = False
                logger.info("Death Link turned off")
            else:
                death_link_toggle = True
                logger.info("Death Link turned on")
        else:
            logger.info("Can't toggle Death Link, option was not enabled")

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
        self.is_ae = False
        self.sent_items = set()
        self.ss2_proc = None
        self.last_deathlink_time = 0.0

        options = Utils.get_options()
        self.ss2_dir_path = os.path.join(options["ss2_options"]["ss2_path"])
        if not os.path.exists(self.ss2_dir_path):
            print_error_and_close("Couldn't find your SS2 installation.")
        if os.path.exists(os.path.join(self.ss2_dir_path, "hathor_Shipping_Playfab_Steam_x64.exe")):
            self.is_ae = True
        if self.is_ae:
            if not os.path.exists(os.path.join(self.ss2_dir_path, "mods", "Archipelago.kpf")):
                print_error_and_close("Couldn't find mod, install the SS2 mod before running the client.")
        else:
            if not os.path.exists(os.path.join(self.ss2_dir_path, "DMM", "Archipelago")):
                print_error_and_close("Couldn't find mod, install the SS2 mod before running the client.")
        self.communication_path = os.path.join(self.ss2_dir_path, "APcommunications")
        if not os.path.exists(self.communication_path):
            os.makedirs(self.communication_path)
        if self.is_ae:
            self.loc_id_files_path = os.path.join(self.communication_path, "LocIdFiles")
            if not os.path.exists(self.loc_id_files_path):
                os.makedirs(self.loc_id_files_path)
                for x in range(1, 2001):
                    self.file_name = "LocId" + str(x) + ".txt"
                    self.file_path = os.path.join(self.loc_id_files_path, self.file_name)
                    open(self.file_path, "x").close()
        self.recieved_items_file = os.path.join(self.communication_path, "ReceivedItems.txt")
        self.sent_items_file = os.path.join(self.communication_path, "SentItems.txt")
        self.settings_file = os.path.join(self.communication_path, "Settings.txt")

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
                f.write("0,")
                if len(args["checked_locations"]) > 0:
                    f.write(str(args["checked_locations"]).strip("[]").replace(" ", "") + ",")

            self.sent_items = set(args["checked_locations"])

            options = (args["slot_data"]["options"])
            with open(self.settings_file, "w") as f:
                f.write(str(self.seed) + ",")
                f.write(options)

            global death_link_enabled
            global death_link_toggle
            if "DeathLink" in options:
                death_link_enabled = True
                death_link_toggle = True
            else:
                death_link_enabled = False
                death_link_toggle = False

            self.is_connected = True

        if cmd in {"ReceivedItems"}:
            with open(self.recieved_items_file, "a") as f:
                for item in args["items"]:
                    f.write(str(item[0]) + ",")
    
    def on_deathlink(self, data: dict[str, object]):
        global death_link_toggle
        if death_link_toggle:
            with open(self.recieved_items_file, "a") as f:
                f.write("500,")

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Archipelago System Shock 2 Client"
        return ui


def print_error_and_close(msg):
    logger.error("Error: " + msg)
    Utils.messagebox("Error", msg, error=True)
    sys.exit(1)

def find_procs_by_name(name):
    for p in psutil.process_iter(['name']):
        if p.info['name'] == name:
            return p
    return None

def find_open_loc_files(process):
    ids = []
    open_files = process.open_files()
    for file in open_files:
        filename = os.path.basename(file.path)
        if filename.startswith("LocId"):
            locid = int(filename.strip("LocId.txt"))
            ids.append(locid)
    return ids

async def loc_watcher(ctx):
    while not ctx.exit_event.is_set():
        if ctx.is_connected:
            global death_link_enabled
            global death_link_toggle
            if death_link_enabled:
                if death_link_toggle and "DeathLink" not in ctx.tags:
                    await ctx.update_death_link(death_link_toggle)
                if not death_link_toggle and "DeathLink" in ctx.tags:
                    await ctx.update_death_link(death_link_toggle)
            locs = []
            if ctx.is_ae:
                try:
                    if ctx.ss2_proc is None:
                        ctx.ss2_proc = find_procs_by_name("hathor_Shipping_Playfab_Steam_x64.exe")
                        if ctx.ss2_proc is not None:
                            logger.info("Found SS2 AE process")
                    if ctx.ss2_proc is not None:
                        loc_ids = find_open_loc_files(ctx.ss2_proc)
                        if loc_ids:
                            for loc_id in loc_ids:
                                logger.info(loc_id)
                                if loc_id not in ctx.sent_items:
                                    locs.append(loc_id)
                                    if loc_id < 1800:
                                        ctx.sent_items.add(loc_id)
                                        with open(ctx.sent_items_file, "a") as f:
                                            f.write(str(loc_id) + ",")
                except psutil.NoSuchProcess:
                    logger.info("SS2 AE process closed")
                    ctx.ss2_proc = None
                except psutil.AccessDenied:
                    logger.info("SS2 AE process access denied, restart the client as admin")
            else:
                with open(ctx.sent_items_file, "r") as f:
                    sent_items_str = f.read()
                    sent_items_set = set(map(int, sent_items_str.strip(",").split(",")))
                    new_locs = sent_items_set - ctx.sent_items
                    if new_locs:
                        locs.extend(new_locs)
                        ctx.sent_items.union(new_locs)
            if locs:
                if 2 in locs:
                    asyncio.create_task(ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]))
                    locs.remove(2)
                if 2000 in locs:
                    locs.remove(2000)
                    if death_link_toggle and (time() - ctx.last_deathlink_time) > 4.0:
                        await ctx.send_death(death_text = "Goggles failed you.")
                        ctx.last_deathlink_time = time()
                    if not ctx.is_ae:
                        with open(ctx.sent_items_file, "r+") as f:
                            contents = f.readline()
                            contents = contents.replace("2000,", "")
                            f.seek(0)
                            f.truncate(0)
                            f.write(contents)
                if 1999 in locs: #deathlink acknowledged so remove deathlink item and the acknowledge
                    locs.remove(1999)
                    if not ctx.is_ae:
                        with open(ctx.sent_items_file, "r+") as f:
                            contents = f.readline()
                            contents = contents.replace("1999,", "")
                            f.seek(0)
                            f.truncate(0)
                            f.write(contents)
                    with open(ctx.recieved_items_file, "r+") as f:
                        contents = f.readline()
                        contents = contents.replace("500,", "")
                        f.seek(0)
                        f.truncate(0)
                        f.write(contents)

                asyncio.create_task(ctx.send_msgs([{"cmd": "LocationChecks", "locations": locs}]))
        await asyncio.sleep(0.3)

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