import math

SS2itemsfilepath = "SS2 items output.txt"
SS2instructionsfilepath = "SS2 instructions output.txt"
APitemsfilepath = "Archipelago items output.txt"
APlocsfilepath = "Archipelago locations output.txt"
SaveDatapath = "RegItemIDLocIDSave.txt"

def newitem(SS2name, APname, id, classification, properties):
    with open(SS2itemsfilepath, "a") as f:
        f.write("\"" + str(id) + "\": [\"" + SS2name + "\", " + properties + "],\n")

    with open(APitemsfilepath, "a") as f:
        f.write("\"" + APname + "\": {\"id\": " + str(id) + ",\n    \"classification\": \"" 
                + classification + "\",\n    \"count\": 1,\n    \"option\": \"\"},\n")

def newloc(name, loc, id, destroyeditem, region, reqitems):
    with open(SS2instructionsfilepath, "a") as f:
        if loc[0] == "[":
            f.write("[\"placeaploc\", " + "\"\", " + loc + ", " + str(id) + ", " + destroyeditem + "], #" + str(id) + ":" + name + "\n")
        else:
            f.write("[\"placeaploc\", " + "\"\", vector" + loc + ", " + str(id) + ", " + destroyeditem + "], #" + str(id) + ":" + name +"\n")

    with open(APlocsfilepath, "a") as f:
        f.write("\"" + name + "\": {\"id\": " + str(id) + ",\n    \"region\": \"" 
                + region + "\",\n    \"option\": \"\",\n    \"reqitems\": " + reqitems 
                + "},\n")

def cybmodshop(terminalids, loc):
    with open(SS2instructionsfilepath, "a") as f:
        f.write("[\"replacecybmodshop\", " + "\"\", " + terminalids + ", vector" + loc + "],\n")

def destroyobj(objid):
    with open(SS2instructionsfilepath, "a") as f:
        f.write("[\"destroy\", " + "\"\", " + objid + "],\n")

def randomizerepl(replid):
    with open(SS2instructionsfilepath, "a") as f:
        f.write("[\"randomizerepl\", " + "\"\", " + replid + "],\n")

def randomizeenemy(enemyid, tier, loc):
    with open(SS2instructionsfilepath, "a") as f:
        f.write("[\"randomizeenemy\", " + "\"\", " + enemyid + ", \"" + tier + "\", vector" + loc + "],\n")

def randomizeenemygen(enemygenid, tier):
    with open(SS2instructionsfilepath, "a") as f:
        f.write("[\"directmonstergenrando\", " + "\"\", " + enemygenid + ", \"" + tier + "\"],\n")

def temp():
    with open(APlocsfilepath, "a") as f:
        amount = 0
        for i in range(1481, 1628):
            numb = i - 1480
            amount += 6
            f.write("\"Cyber module shop " + str(numb) + "\": {\"id\": " + str(i) + ",\n    \"region\": \"Menu\",\n    \"option\": \"StatsSkillsPsi\",\n    \"reqitems\": {\"Cyber Modules\": " + str(amount) + "}},\n")

curregion = ""
nextitemid = 1
nextlocid = 1
with open(SaveDatapath, "r") as f:
    data = f.readline().split(",")
    curregion = data[0]
    nextitemid = int(data[1])
    nextlocid = int(data[2])

while True:
    command = input("Available commands: itemid, locid, region, item, loc, shop, destroy, randorepl, randoenemy, randoenemygen, close\n")
    match command:
        case "Temp":
            temp()

        case "itemid":
            nextitemid = int(input("New itemid?\n"))

        case "locid":
            nextlocid = int(input("New locid?\n"))

        case "region":
            curregion = input("New region?\n")

        case "item":
            SS2itemname = input("Name for item in shocked?\n")
            APitemname = input("Name for item in AP?\n")

            noclassification = True
            APclassification = "progression"
            while noclassification:
                APclassificationnumber = input("Classification in Archipelago?  1 for progression, 2 for useful, 3 for filler, or 4 for trap\n")
                match int(APclassificationnumber):
                    case 1:
                        APclassification = "progression"
                        noclassification = False
                    case 2:
                        APclassification = "useful"
                        noclassification = False
                    case 3:
                        APclassification = "filler"
                        noclassification = False
                    case 4:
                        APclassification = "trap"
                        noclassification = False
                    case _:
                        print("invalid entry, enter 1, 2, 3, or 4")

            itemproperties = input("What are this items properties? enter a list if so, or nothing if none\nfor each property create a list, example: [[\"StackCount\", 239], [\"Scale\", vector(3.00, 0.50, 1.00)], [\"LightColor\", \"hue\", 8.3]]\nif its a character upgrade instead see PlayerScripts and VariousDataTables\n")
            if len(itemproperties) == 0:
                itemproperties = "[]"
            newitem(SS2itemname, APitemname, nextitemid, APclassification, itemproperties)
            nextitemid += 1

        case "loc":
            locname = input("Name of location for AP?\n")
            location = input("Location for SS2?  if vector enter (x, y, z), if set of containers enter [containerid, containerid, ...]\n")
            destroyedobjid = input("SS2 ObjID of replaced object to be destroyed? enter nothing if none.\n")
            if len(destroyedobjid) == 0:
                destroyedobjid = "0"
            requireditems = input("What items are required to reach this location? enter a table of \"name\": amount if so, otherwise enter nothing if none\n")
            if len(requireditems) == 0:
                requireditems = "{}"
            newloc(locname, location, nextlocid, destroyedobjid, curregion, requireditems)
            nextlocid += 1

        case "shop":
            terminalidlist = input("list of 4 terminal objids to replace?\n")
            shoplocation = input("Vector of location shop should be placed? enter in format (x, y, z)\n")
            cybmodshop(terminalidlist, shoplocation)

        case "destroy":
            destroyedobjid = input("Id of the item to destroy?\n")
            destroyobj(destroyedobjid)

        case "randorepl":
            replicatorid = input("Id of the repl to randomize?\n")
            randomizerepl(replicatorid)

        case "randoenemy":
            enemyobjid = input("SS2 objid of enemy to replace? enter nothing if none\n")
            if len(enemyobjid) == 0:
                enemyobjid = "0"
            enemytier = input("Tier of enemy? enter the number for tier of enemy,\nadding the word Ranged right after with no spaces if ranged only\n")
            enemylocation = input("Location of placement of new enemy? enter in format (x, y, z)\n")
            randomizeenemy(enemyobjid, enemytier, enemylocation)

        case "randoenemygen":
            enemygenobjid = input("SS2 objid of enemygen or direnemygen?\n")
            enemytier = input("Tier of enemy? enter the number for tier of enemy,\nadding the word Ranged right after with no spaces if ranged only\n")
            randomizeenemygen(enemygenobjid, enemytier)

        case "close":
            with open(SaveDatapath, "w") as f:
                f.write(curregion + "," + str(nextitemid) + "," + str(nextlocid))
            exit()

        case _:
            print("invalid command")