from typing import ClassVar, Dict, Any
from .options import SS2options
from .items import SS2items, SS2item
from .locations import SS2locations, SS2location
from .settings import SS2Settings
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule, forbid_item
from BaseClasses import Region, Location, Entrance, Item, ItemClassification, CollectionState
from worlds.LauncherComponents import components, Component, Type, launch as launch_component

from Utils import visualize_regions

def launch_client(*args):
    from .Client import launch
    launch_component(launch, "SS2Client", args)

components.append(Component("System Shock 2 Client", func=launch_client, component_type=Type.CLIENT))

class SS2World(World):
    """System Shock 2 item, enemy, skill, stat, and psi randomizer."""
    game = "System Shock 2"  # name of the game/world
    options_dataclass = SS2options  # options the player can set
    options: SS2options
    settings: SS2Settings
    topology_present = True  # show path to required location checks in spoiler

    item_name_to_id = {name: data["id"] for name, data in SS2items.items()}
    location_name_to_id = {name: data["id"] for name, data in SS2locations.items()}
    item_name_groups = {"Pistols": {"Pistol", "Damaged Pistol"},
                        "Shotguns": {"Shotgun", "Damaged Shotgun"},
                        "Laser Pistols": {"Laser Pistol", "Damaged Laser Pistol"},
                        }


    def create_location(self, locname: str, locregion) -> SS2location:
        locdata = SS2locations[locname]
        return SS2location(self.player, locname, locdata["id"], locregion)

    def has_functional_weapon(self, state: CollectionState):
        p = self.player
        cybmodamount = self.cyb_mod_count(state)
        functional_weapon = (((state.has_group("Pistols", p) or (state.has("Broken Pistol", p) and self.upgrade_or_cybmod(state, "Repair Upgrade", 1, 17, cybmodamount))) and self.upgrade_or_cybmod(state, "Conventional weapon Upgrade", 1, 21, cybmodamount) and state.has("Standard Clip", p, 4)) or
                             
                            ((state.has_group("Shotguns", p) or (state.has("Broken Shotgun", p) and self.upgrade_or_cybmod(state, "Repair Upgrade", 3, 39, cybmodamount))) and self.upgrade_or_cybmod(state, "Conventional weapon Upgrade", 3, 45, cybmodamount) and state.has("6 Rifled Slugs", p, 4)) or

                            ((state.has_group("Laser Pistols", p) or (state.has("Broken Laser Pistol", p) and self.upgrade_or_cybmod(state, "Repair Upgrade", 1, 17, cybmodamount))) and self.upgrade_or_cybmod(state, "Energy weapon Upgrade", 1, 21, cybmodamount)) or

                            ((state.has("Grenade Launcher", p) or (state.has("Broken Grenade Launcher", p) and self.upgrade_or_cybmod(state, "Repair Upgrade", 2, 25, cybmodamount))) and self.upgrade_or_cybmod(state, "Heavy weapon Upgrade", 1, 21, cybmodamount) and state.has("3 Fragmentation Grenades", p, 5)) or
    
                            (state.has("Psi Amp", p) and self.upgrade_or_cybmod(state, "Psi Upgrade", 2, 41, cybmodamount) and
                            ((self.upgrade_or_cybmod(state, "Projected Cryokinesis Psi Ability", 1, 41, cybmodamount) and self.upgrade_or_cybmod(state, "First Tier Neural Capacity Psi Ability", 1, 41, cybmodamount)) or 
                            (state.has("Localized Pyrokinesis Psi Ability", p) and state.has("Second Tier Neural Capacity Psi Ability", p)) or
                            (state.has("Projected Pyrokinesis Psi Ability", p) and state.has("Third Tier Neural Capacity Psi Ability", p)) or
                            (state.has("Cerebro-Energetic Extension Psi Ability", p) and state.has("Fourth Tier Neural Capacity Psi Ability", p)))))
        return functional_weapon

    def create_regions(self) -> None:
        curoptions = "" #there is prob a way better way than this
        if self.options.include_stats_skills_psi:
            curoptions += "StatsSkillsPsi,"

        if self.options.include_os_upgrades:
            curoptions += "OSUpgrades,"

        if self.options.remove_duplicate_locations:
            curoptions += "RemoveDuplicates,"
        else:
            curoptions += "KeepDuplicates,"
        
        if self.options.include_chemicals:
            curoptions += "Chemicals,"

        if self.options.include_starting_wrench:
            curoptions += "StartingWrench,"

        if self.options.many_is_victory:
            curoptions += "ManyIsVictory"


        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        medsci1_region = Region("medsci1", self.player, self.multiworld)
        self.multiworld.regions.append(medsci1_region)
        medsci1sci_region = Region("medsci1sci", self.player, self.multiworld)
        self.multiworld.regions.append(medsci1sci_region)
        medsci1rd_region = Region("medsci1rd", self.player, self.multiworld)
        self.multiworld.regions.append(medsci1rd_region)
        medsci2med_region = Region("medsci2med", self.player, self.multiworld)
        self.multiworld.regions.append(medsci2med_region)
        medsci2crew_region = Region("medsci2crew", self.player, self.multiworld)
        self.multiworld.regions.append(medsci2crew_region)
        eng1_region = Region("eng1", self.player, self.multiworld)
        self.multiworld.regions.append(eng1_region)
        eng2_region = Region("eng2", self.player, self.multiworld)
        self.multiworld.regions.append(eng2_region)
        hydro2_region = Region("hydro2", self.player, self.multiworld)
        self.multiworld.regions.append(hydro2_region)
        hydro1_region = Region("hydro1", self.player, self.multiworld)
        self.multiworld.regions.append(hydro1_region)
        hydro3_region = Region("hydro3", self.player, self.multiworld)
        self.multiworld.regions.append(hydro3_region)
        ops1_region = Region("ops1", self.player, self.multiworld)
        self.multiworld.regions.append(ops1_region)
        ops2_region = Region("ops2", self.player, self.multiworld)
        self.multiworld.regions.append(ops2_region)
        ops3_region = Region("ops3", self.player, self.multiworld)
        self.multiworld.regions.append(ops3_region)
        ops4_region = Region("ops4", self.player, self.multiworld)
        self.multiworld.regions.append(ops4_region)
        rec1_region = Region("rec1", self.player, self.multiworld)
        self.multiworld.regions.append(rec1_region)
        rec2_region = Region("rec2", self.player, self.multiworld)
        self.multiworld.regions.append(rec2_region)
        rec3_region = Region("rec3", self.player, self.multiworld)
        self.multiworld.regions.append(rec3_region)
        command1_region = Region("command1", self.player, self.multiworld)
        self.multiworld.regions.append(command1_region)
        command2_region = Region("command2", self.player, self.multiworld)
        self.multiworld.regions.append(command2_region)
        rick1_region = Region("rick1", self.player, self.multiworld)
        self.multiworld.regions.append(rick1_region)
        rick2_region = Region("rick2", self.player, self.multiworld)
        self.multiworld.regions.append(rick2_region)
        rick3_region = Region("rick3", self.player, self.multiworld)
        self.multiworld.regions.append(rick3_region)
        many_region = Region("many", self.player, self.multiworld)
        self.multiworld.regions.append(many_region)
        shodan_region = Region("shodan", self.player, self.multiworld)
        self.multiworld.regions.append(shodan_region)

        for location, data in SS2locations.items():
            if data["option"] not in curoptions:
                continue

            locregion = self.multiworld.get_region(data["region"], self.player)
            loc = self.create_location(location, locregion)
            locregion.locations.append(loc)
            for reqitem, amount in data["reqitems"].items():
                match reqitem:
                    case "Psi Wall":
                        add_rule(loc, lambda state: state.has("Psi Amp", self.player) and self.upgrade_or_cybmod(state, "Metacreative Barrier Psi Ability", 1, 169, curcba := self.cyb_mod_count(state)) and self.upgrade_or_cybmod(state, "Fifth Tier Neural Capacity Psi Ability", 1, 169, curcba))
                    case "Cyber Modules":
                        add_rule(loc, lambda state, a = amount: a <= self.cyb_mod_count(state))
                    case "Hacking Upgrade":
                        if self.options.include_stats_skills_psi:
                            add_rule(loc, lambda state, ri = reqitem, a = amount[0]: (state.has(ri, self.player, a) and state.has("Cybernetic Affinity Upgrade", self.player, (a // 2))) or 
                                    (state.has("Psi Upgrade", self.player, (a*2)-2) and state.has("Psi Amp", self.player) and state.has("Remote Circuitry Manipulation Psi Ability", self.player) and state.has("Fourth Tier Neural Capacity Psi Ability", self.player)))
                        else:
                            add_rule(loc, lambda state, ri = reqitem, a = amount[0], cba = amount[1]: self.upgrade_or_cybmod(state, ri, a, cba, self.cyb_mod_count(state)))
                    case "Research Upgrade":
                        if self.options.include_stats_skills_psi:
                            add_rule(loc, lambda state, ri = reqitem, a = amount[0]: state.has(ri, self.player, a) or (state.has(ri, self.player, a-1) and state.has("LabAssistant(TM) Implant", self.player)))
                        else:
                            add_rule(loc, lambda state, ri = reqitem, a = amount[0], cba = amount[1]: self.upgrade_or_cybmod(state, ri, a, cba, self.cyb_mod_count(state)))
                    case "Repair Upgrade":
                        add_rule(loc, lambda state, ri = reqitem, a = amount[0], cba = amount[1]: self.upgrade_or_cybmod(state, ri, a, cba, self.cyb_mod_count(state)))
                    case "Deck 5 Crew Access Card":
                        if self.options.include_stats_skills_psi:
                            add_rule(loc, lambda state, ri = reqitem, a = amount: state.has(ri, self.player, a) or (state.has("Psi Amp", self.player) and state.has("Metacreative Barrier Psi Ability", self.player) and state.has("Fifth Tier Neural Capacity Psi Ability", self.player)))
                        else:
                            add_rule(loc, lambda state, ri = reqitem, a = amount: state.has(ri, self.player, a) or 169 <= self.cyb_mod_count(state))
                    case "Antimony" | "Vanadium":
                        if self.options.include_chemicals:
                            add_rule(loc, lambda state, ri = reqitem, a = amount: state.has(ri, self.player, a))
                    case _:
                        add_rule(loc, lambda state, ri = reqitem, a = amount: state.has(ri, self.player, a))

        if self.options.include_stats_skills_psi:
            for i in range(1, 148):
                cybmodshop = "Cyber module shop " + str(i)
                forbid_item(self.multiworld.get_location(cybmodshop, self.player), "13 Cyber Modules", self.player)
                forbid_item(self.multiworld.get_location(cybmodshop, self.player), "14 Cyber Modules", self.player)
                forbid_item(self.multiworld.get_location(cybmodshop, self.player), "15 Cyber Modules", self.player)
                forbid_item(self.multiworld.get_location(cybmodshop, self.player), "16 Cyber Modules", self.player)
                forbid_item(self.multiworld.get_location(cybmodshop, self.player), "20 Cyber Modules", self.player)
                forbid_item(self.multiworld.get_location(cybmodshop, self.player), "25 Cyber Modules", self.player)
                forbid_item(self.multiworld.get_location(cybmodshop, self.player), "30 Cyber Modules", self.player)
                forbid_item(self.multiworld.get_location(cybmodshop, self.player), "Naturally Able OSUpgrade", self.player)

        menu_region.add_exits({"medsci1"})
        medsci1_region.add_exits({"medsci1sci"}, {"medsci1sci": lambda state: state.has("Science Access Card", self.player)})
        medsci1sci_region.add_exits({"medsci1rd", "medsci2med", "medsci2crew", "eng1"}, {"medsci1rd": lambda state: state.has("R & D Access Card", self.player),
                                                                                        "medsci2med": lambda state: state.has("Dead Power Cell", self.player, 2) and self.has_functional_weapon(state), 
                                                                                        "medsci2crew": lambda state: state.has("Deck 2 crew Access Card", self.player) and self.has_functional_weapon(state), 
                                                                                        "eng1": lambda state: state.has("Maintenance conduit Access AL", self.player) and self.has_functional_weapon(state)})
        medsci2crew_region.add_exits({"medsci2med"}, {"medsci2med": lambda state: state.has("Deck 2 crew Access Card", self.player)})
        eng1_region.add_exits({"eng2", "hydro2"}, {"hydro2": lambda state: state.has("45m/dEx circuit board", self.player) and state.has("Fluidics Control Access AL", self.player)})
        if self.options.include_chemicals:
            hydro2_region.add_exits({"ops2"}, {"ops2": lambda state: state.has("Toxin-A", self.player, 4) and state.has("Vanadium", self.player) and state.has("Antimony", self.player, 2)
                                                                     and (self.upgrade_or_cybmod(state, "Research Upgrade", 1, 17, self.cyb_mod_count(state)) or state.has("LabAssistant(TM) Implant", self.player)) 
                                                                     and state.has("Hydroponics A Access Card", self.player) and state.has("Hydroponics D Access Card", self.player)})
        else:
            hydro2_region.add_exits({"ops2"}, {"ops2": lambda state: state.has("Toxin-A", self.player, 4) and (self.upgrade_or_cybmod(state, "Research Upgrade", 1, 17, self.cyb_mod_count(state)) or state.has("LabAssistant(TM) Implant", self.player))
                                                                     and state.has("Hydroponics A Access Card", self.player) and state.has("Hydroponics D Access Card", self.player)})
        hydro2_region.add_exits({"hydro1", "hydro3"}, {"hydro1": lambda state: state.has("Hydroponics A Access Card", self.player), 
                                                               "hydro3": lambda state: state.has("Hydroponics D Access Card", self.player)})
        ops2_region.add_exits({"rec1", "ops1", "ops3", "ops4"})
        rec1_region.add_exits({"command1", "rec2", "rec3"}, {"command1": lambda state: state.has("Quantum Simulation Chip", self.player) and state.has("Linear Simulation Chip", self.player) and state.has("Interpolated Simulation Chip", self.player) and state.has("Security Access Card", self.player)
                                                             and (state.has("Deck 5 Crew Access Card", self.player) or (state.has("Psi Amp", self.player) and self.upgrade_or_cybmod(state, "Metacreative Barrier Psi Ability", 1, 169, self.cyb_mod_count(state)) and self.upgrade_or_cybmod(state, "Fifth Tier Neural Capacity Psi Ability", 1, 169, self.cyb_mod_count(state)))) and state.has("Dead Power Cell", self.player, 2) and state.has("Athletics Access Card", self.player)})
        command1_region.add_exits({"command2", "rick1"}, {"rick1": lambda state: state.has("Ops Override Access Card", self.player) and state.has("Shuttle Bay Access Card", self.player)
                                                          and state.has("Sympathetic Resonator", self.player) and state.has("Bridge Access Card", self.player)})
        rick1_region.add_exits({"rick2"}, {"rick2": lambda state: state.has("Rickenbacker Access Card", self.player)})
        rick2_region.add_exits({"rick3"})
        rick3_region.add_exits({"many"})
        many_region.add_exits({"shodan"})

        if self.options.many_is_victory:
            VictoryLoc = SS2location(self.player, "Victory", None, many_region)
            many_region.locations.append(VictoryLoc)
        else:
            VictoryLoc = SS2location(self.player, "Victory", None, shodan_region)
            shodan_region.locations.append(VictoryLoc)
        VictoryLoc.place_locked_item(SS2item("Victory", ItemClassification.progression, None, self.player))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        #visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

        
            
    def create_item(self, name: str) -> SS2item:
        itemdata = SS2items[name]
        match itemdata["classification"]:
            case "progression":
                itemclass = ItemClassification.progression
            case "useful":
                itemclass = ItemClassification.useful
            case "filler":
                itemclass = ItemClassification.filler
            case "trap":
                itemclass = ItemClassification.trap
            case _:
                itemclass = ItemClassification.filler
        return SS2item(name, itemclass, itemdata["id"], self.player)

    def create_items(self) -> None:
        SS2itempool = []
        curoptions = ""
        if self.options.include_stats_skills_psi:
            curoptions += "StatsSkillsPsi,"

        if self.options.include_os_upgrades:
            curoptions += "OSUpgrades,"

        if self.options.remove_duplicate_locations:
            curoptions += "RemoveDuplicates,"
        else:
            curoptions += "KeepDuplicates,"

        if self.options.include_chemicals:
            curoptions += "Chemicals,"

        if self.options.include_starting_wrench:
            curoptions += "StartingWrench,"

        SS2itemlist = SS2items

        if self.options.remove_duplicate_locations: #303 already removed
            SS2itemlist["Wrench"]["count"] -= 12 #leaves 2 wrench and 1 starting wrench
            SS2itemlist["Pistol"]["count"] -= 4 #leaves 1
            SS2itemlist["Damaged Pistol"]["count"] -= 17 #leaves 1
            SS2itemlist["Broken Pistol"]["count"] -= 9 #leaves 1
            SS2itemlist["Shotgun"]["count"] -= 1 #leaves 1
            SS2itemlist["Damaged Shotgun"]["count"] -= 7 #leaves 1
            SS2itemlist["Broken Shotgun"]["count"] -= 5 #leaves 1
            SS2itemlist["Laser Pistol"]["count"] -= 3 #leaves 1
            SS2itemlist["Damaged Laser Pistol"]["count"] -= 1 #leaves 1
            #SS2itemlist["Broken Laser Pistol"]["count"] -= 0 #leaves 1
            #SS2itemlist["Grenade Launcher"]["count"] -= 0 #leaves 2
            SS2itemlist["Broken Grenade Launcher"]["count"] -= 2 #leaves 1
            SS2itemlist["Psi Amp"]["count"] -= 4 #leaves 3
            SS2itemlist["Assault Rifle"]["count"] -= 1 #leaves 1
            SS2itemlist["Damaged Assault Rifle"]["count"] -= 1 #leaves 1
            SS2itemlist["Broken Assault Rifle"]["count"] -= 1 #leaves 1
            #SS2itemlist["Broken Stasis Field Generator"]["count"] -= 0 #leaves 2
            #SS2itemlist["Damaged Stasis Field Generator"]["count"] -= 0 #leaves 1
            SS2itemlist["Laser Rapier"]["count"] -= 2 #leaves 3
            SS2itemlist["EMP Rifle"]["count"] -= 3 #leaves 1
            SS2itemlist["Damaged EMP Rifle"]["count"] -= 1 #leaves 1
            SS2itemlist["Broken EMP Rifle"]["count"] -= 1 #leaves 1
            SS2itemlist["Crystal Shard"]["count"] -= 14 #leaves 3
            SS2itemlist["Damaged Fusion Cannon"]["count"] -= 1 #leaves 2
            #SS2itemlist["Broken Fusion Cannon"]["count"] -= 0 #leaves 1
            #SS2itemlist["Annelid Launcher"]["count"] -= 0 leaves 3
            
            SS2itemlist["Small Standard Clip"]["count"] -= 58 #leaves 0
            SS2itemlist["Standard Clip"]["count"] += 29 #leaves 65
            SS2itemlist["Small AP Clip"]["count"] -= 12 #leaves 1
            SS2itemlist["AP Clip"]["count"] += 6 #leaves 11
            SS2itemlist["Box of 6 Anti-personnel Bullets"]["count"] -= 8 #leaves 0
            SS2itemlist["Box of 12 Anti-Personnel Bullets"]["count"] += 4 #leaves 12
            SS2itemlist["10 Prisms"]["count"] -= 10 #leaves 1
            SS2itemlist["20 Prisms"]["count"] += 5 #leaves 15

            SS2itemlist["Suit of Light Combat Armor"]["count"] -= 4 #leaves 1
            SS2itemlist["Suit of Standard-Issue Combat Armor"]["count"] -= 3 #leaves 1
            SS2itemlist["Suit of Powered Armor"]["count"] -= 1 #leaves 1
            SS2itemlist["Suit of Worm Skin Armor"]["count"] -= 4 #leaves 1
            SS2itemlist["Suit of Heavy Combat Armor"]["count"] -= 4 #leaves 1

            SS2itemlist["BrawnBoost Implant"]["count"] -= 2 #leaves 2
            SS2itemlist["PsiBoost Implant"]["count"] -= 2 #leaves 2
            SS2itemlist["SwiftBoost Implant"]["count"] -= 3 #leaves 2
            #SS2itemlist["LabAssistant Implant"]["count"] -= 0 #leaves 2
            SS2itemlist["EndurBoost Implant"]["count"] -= 1 #leaves 2
            SS2itemlist["WormMind Implant"]["count"] -= 2 #leaves 2
            #SS2itemlist["ExperTech Implant"]["count"] -= 0 #leaves 2
            #SS2itemlist["WormBlood Implant"]["count"] -= 0 #leaves 2
            SS2itemlist["WormHeart Implant"]["count"] -= 2 #leaves 2

            #maintain the same or very close total amount of nanites (core 5208, current 5211)
            SS2itemlist["5 Nanites"]["count"] -= 16 #leaves 1
            SS2itemlist["10 Nanites"]["count"] -= 34 #leaves 1
            SS2itemlist["15 Nanites"]["count"] -= 12 #leaves 1
            SS2itemlist["20 Nanites"]["count"] -= 31 #leaves 2
            SS2itemlist["30 Nanites"]["count"] -= 10 #leaves 4
            SS2itemlist["35 Nanites"]["count"] -= 0 #leaves 6
            SS2itemlist["40 Nanites"]["count"] += 6 #leaves 16
            SS2itemlist["50 Nanites"]["count"] -= 9 #leaves 10
            SS2itemlist["55 Nanites"]["count"] += 6 #leaves 11
            SS2itemlist["65 Nanites"]["count"] += 4 #leaves 11
            SS2itemlist["73 Nanites"]["count"] += 10 #leaves 12
            SS2itemlist["79 Nanites"]["count"] += 2 #leaves 8
            SS2itemlist["85 Nanites"]["count"] += 3 #leaves 4
            SS2itemlist["503 Nanites"]["count"] -= 0 #leaves 1

            #maintain the same or very close total amount of cyber modules (core 944, current 944)
            #make sure there is some amount of cyber module items 10 or less or it will cause generation issues
            SS2itemlist["2 Cyber Modules"]["count"] -= 22 #leaves 0
            SS2itemlist["3 Cyber Modules"]["count"] -= 24 #leaves 2
            SS2itemlist["4 Cyber Modules"]["count"] -= 9 #leaves 3
            SS2itemlist["5 Cyber Modules"]["count"] -= 7 #leaves 2
            SS2itemlist["6 Cyber Modules"]["count"] -= 0 #leaves 10
            SS2itemlist["7 Cyber Modules"]["count"] -= 0 #leaves 2
            SS2itemlist["8 Cyber Modules"]["count"] -= 0 #leaves 5
            SS2itemlist["10 Cyber Modules"]["count"] -= 0 #leaves 19
            SS2itemlist["13 Cyber Modules"]["count"] += 2 #leaves 4
            SS2itemlist["14 Cyber Modules"]["count"] += 2 #leaves 4
            SS2itemlist["15 Cyber Modules"]["count"] += 4 #leaves 10
            SS2itemlist["16 Cyber Modules"]["count"] += 3 #leaves 4
            SS2itemlist["20 Cyber Modules"]["count"] -= 0 #leaves 9
            SS2itemlist["25 Cyber Modules"]["count"] += 1 #leaves 2
            SS2itemlist["30 Cyber Modules"]["count"] += 0 #leaves 2

        if "Science Access Card" in self.options.start_inventory:
            SS2itemlist["Science Access Card"]["count"] -= 1
            SS2itemlist["15 Nanites"]["count"] += 1

        for item, data in SS2itemlist.items():
            if data["option"] not in curoptions:
                continue
            amount = data["count"]
            while amount > 0:
                newitem = self.create_item(item)
                SS2itempool.append(newitem)
                amount -= 1
    
        self.multiworld.itempool += SS2itempool
        
    def fill_slot_data(self) -> Dict[str, Any]:
        curoptions = ""

        if self.options.include_stats_skills_psi:
            curoptions += "StatsSkillsPsi,"
        else:
            curoptions+= "Respec,"

        if self.options.include_os_upgrades:
            curoptions += "OSUpgrades,"

        if self.options.remove_duplicate_locations:
            curoptions += "RemoveDuplicates,"
        else:
            curoptions += "KeepDuplicates,"

        if self.options.include_chemicals:
            curoptions += "Chemicals,"

        if self.options.include_starting_wrench:
            curoptions += "StartingWrench,"

        if self.options.many_is_victory:
            curoptions += "ManyIsVictory"

        return {"options": curoptions}
    
    def cyb_mod_count(self, state) -> int:
        curcybmodamount = 0
        curcybmodamount += state.count("2 Cyber Modules", self.player) * 2
        curcybmodamount += state.count("3 Cyber Modules", self.player) * 3
        curcybmodamount += state.count("4 Cyber Modules", self.player) * 4
        curcybmodamount += state.count("5 Cyber Modules", self.player) * 5
        curcybmodamount += state.count("6 Cyber Modules", self.player) * 6
        curcybmodamount += state.count("7 Cyber Modules", self.player) * 7
        curcybmodamount += state.count("8 Cyber Modules", self.player) * 8
        curcybmodamount += state.count("10 Cyber Modules", self.player) * 10
        curcybmodamount += state.count("13 Cyber Modules", self.player) * 13
        curcybmodamount += state.count("14 Cyber Modules", self.player) * 14
        curcybmodamount += state.count("15 Cyber Modules", self.player) * 15
        curcybmodamount += state.count("16 Cyber Modules", self.player) * 16
        curcybmodamount += state.count("20 Cyber Modules", self.player) * 20
        curcybmodamount += state.count("25 Cyber Modules", self.player) * 25
        curcybmodamount += state.count("30 Cyber Modules", self.player) * 30
        if state.has("Naturally Able OSUpgrade", self.player):
            curcybmodamount += 20
        return curcybmodamount
    
    def upgrade_or_cybmod(self, state, item, amount, cybmodamount, curcybmodamount) -> bool:
        if self.options.include_stats_skills_psi:
            return state.has(item, self.player, amount)
        else:
            return cybmodamount <= curcybmodamount
            