import typing
from Options import DefaultOnToggle, PerGameCommonOptions, Option, Toggle, DefaultOnToggle, Range, Choice, OptionSet
from dataclasses import dataclass

#class IncludeStatsSkillsPsi(DefaultOnToggle):                                                                
#    """Include Technical Skills, Weapon Skills, Statistics, Psi Tier unlocks, and Psi ability unlocks in the randomizer."""
#    display_name = "Include Tech Skills, Weapon Skills, Stats, and Psi" 
#conceptually very hard to add a way to turn this off, would have to replace all instances of stat requirmenets with the minimum number of cyber modules needed to obtain those stats.  But then you run into softlock issues where that is expecting
#the player to always put all their cyber modules into that thing.  But thats not even considering requiring the player to get two different stats.  So you need some sort of variable to track the current amount needed.
#but then again that expects the player to perfectly spend their cyber modules on stats needed for locations, which they wont.  So the only possible way to implement this involves removing all stat checks, which also means
#making it so progression items can't spawn in security crates.  And also the check for making sure the player has a weapon before leaving medsci1.  If you have an idea feel free to implement it but I dont see a way.

class IncludeOSUpgrades(DefaultOnToggle):
    """Include OSUpgrades in the randomizer."""
    display_name = "Include OSUpgrades"

class IncludeStartingWrench(Toggle):
    """Include the wrench found on the first body in medsci in the randomizer.  Softlocks, strange strategies, and frustation potentially possible."""
    display_name = "Include starting wrench"

class ManyIsVictory(Toggle):
    """Make The Many the victory condition instead of Shodan.  You can still go kill Shodan after."""
    display_name = "The Many is victory condition."


@dataclass
class SS2options(PerGameCommonOptions):
    #include_stats_skills_psi: IncludeStatsSkillsPsi
    include_os_upgrades: IncludeOSUpgrades
    include_starting_wrench: IncludeStartingWrench
    many_is_victory: ManyIsVictory