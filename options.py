import typing
from Options import DefaultOnToggle, PerGameCommonOptions, Toggle, StartInventory, DeathLink
from dataclasses import dataclass

class IncludeStatsSkillsPsi(DefaultOnToggle):                                                                
    """Include Technical Skills, Weapon Skills, Statistics, Psi Tier unlocks, and Psi ability unlocks."""
    display_name = "Include Tech Skills, Weapon Skills, Stats, and Psi" 

class IncludeOSUpgrades(DefaultOnToggle):
    """Include OSUpgrades."""
    display_name = "Include OSUpgrades"

class RemoveDuplicateLocations(DefaultOnToggle):
    """Drastically reduces the amount of locations by removing extra locations with the same name and locations close together.
    Does not affect chemicals if that option is on.  Removes all unneccesary audio logs, reduces amount of some weapons, and compresses consumables."""
    display_name = "Remove duplicate locations"

class RandomizeCodeArt(DefaultOnToggle):
    """Randomize which art has codes in recreation.  All 4 pieces of the code need to be seen to activate the transmitter.
    If this option is off the 4 locations are: 2 in Rec A, 1 near the safe behind the reception desk, 1 in a crew quarters room on the 2nd floor.
    1 in Rec B in the pool room.  1 in Rec C in the artechnology store.  If this option is on the 7 extra locations are:  2 in Rec A inside crew quarters rooms on the 2nd floor.
    1 in Rec B in the dining room where the lights turn off.  4 in Rec C in the artechnology store Rec C."""

class IncludeChemicals(Toggle):
    """Include chemicals and manifests."""
    display_name = "Include chemicals"
    
class IncludeStartingWrench(Toggle):
    """Include the wrench found on the first body in medsci."""
    display_name = "Include starting wrench"

class SS2DeathLink(DeathLink):
    """Whenever anyone with Death Link on dies, all other players in the multiworld with Death Link on die as well.  Not abusing saving is integral to this option functioning. 
    Both because it functionally needs the death animation to play out to work, but also because it can easily be invalidated by saving.  My recommendation is to only save after level transitions.
    I also recommend that even if this option is off to make SS2 more enjoyable."""
    display_name = "Death Link"

class ManyIsVictory(Toggle):
    """Make The Many the victory condition instead of Shodan."""
    display_name = "The Many is victory condition"

class RandomizeEnemies(DefaultOnToggle):
    """Randomizes enemies.  Turning off is untested and it is heavily recommended to stay on.
    If turned off the early game will be much more difficult, especially if the starting wrench is randomized, and the mid-late game will be too easy."""
    display_name = "Randomize Enemies"

class RandomizeReplicators(DefaultOnToggle):
    """Randomizes contents and prices of replicators.  Forces a Psi hypo to be in the MedSci Xerxes room replicator.  Intended to stay on."""
    display_name = "Randomize Replicators"

class SS2StartInventory(StartInventory):
    default = {"Science Access Card": 1}

@dataclass
class SS2options(PerGameCommonOptions):
    include_stats_skills_psi: IncludeStatsSkillsPsi
    include_os_upgrades: IncludeOSUpgrades
    remove_duplicate_locations: RemoveDuplicateLocations
    randomize_code_art: RandomizeCodeArt
    include_chemicals: IncludeChemicals
    include_starting_wrench: IncludeStartingWrench
    death_link: DeathLink
    many_is_victory: ManyIsVictory
    start_inventory: SS2StartInventory
    randomize_enemies: RandomizeEnemies
    randomize_replicators: RandomizeReplicators