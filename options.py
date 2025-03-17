import typing
from Options import DefaultOnToggle, PerGameCommonOptions, Option, Toggle, DefaultOnToggle, Range, Choice, OptionSet
from dataclasses import dataclass

class IncludeStatsSkillsPsi(DefaultOnToggle):                                                                
    """Include Technical Skills, Weapon Skills, Statistics, Psi Tier unlocks, and Psi ability unlocks in the randomizer."""
    display_name = "Include Tech Skills, Weapon Skills, Stats, and Psi" 

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
    include_stats_skills_psi: IncludeStatsSkillsPsi
    include_os_upgrades: IncludeOSUpgrades
    include_starting_wrench: IncludeStartingWrench
    many_is_victory: ManyIsVictory