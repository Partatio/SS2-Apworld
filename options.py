import typing
from Options import DefaultOnToggle, PerGameCommonOptions, Toggle, StartInventory
from dataclasses import dataclass

class IncludeStatsSkillsPsi(DefaultOnToggle):                                                                
    """Include Technical Skills, Weapon Skills, Statistics, Psi Tier unlocks, and Psi ability unlocks."""
    display_name = "Include Tech Skills, Weapon Skills, Stats, and Psi" 

class IncludeOSUpgrades(DefaultOnToggle):
    """Include OSUpgrades."""
    display_name = "Include OSUpgrades"

class RemoveDuplicateLocations(DefaultOnToggle):
    """Drastically reduces the amount of locations by removing extra locations with the same name and locations close together.
    Does not affect chemicals if that option is on.  Removes all unneccesary audio logs, reduces amount of some weapons, and compresses items."""
    display_name = "Remove duplicate locations"

class IncludeChemicals(Toggle):
    """Include chemicals and manifests."""
    display_name = "Include chemicals"
    
class IncludeStartingWrench(Toggle):
    """Include the wrench found on the first body in medsci."""
    display_name = "Include starting wrench"

class ManyIsVictory(Toggle):
    """Make The Many the victory condition instead of Shodan."""
    display_name = "The Many is victory condition."

class SS2StartInventory(StartInventory):
    default = {"Science Access Card": 1}

@dataclass
class SS2options(PerGameCommonOptions):
    include_stats_skills_psi: IncludeStatsSkillsPsi
    include_os_upgrades: IncludeOSUpgrades
    remove_duplicate_locations: RemoveDuplicateLocations
    include_chemicals: IncludeChemicals
    include_starting_wrench: IncludeStartingWrench
    many_is_victory: ManyIsVictory
    start_inventory: SS2StartInventory