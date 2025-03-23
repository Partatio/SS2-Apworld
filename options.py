import typing
from Options import DefaultOnToggle, PerGameCommonOptions, Toggle, StartHints
from dataclasses import dataclass

class IncludeStatsSkillsPsi(DefaultOnToggle):                                                                
    """Include Technical Skills, Weapon Skills, Statistics, Psi Tier unlocks, and Psi ability unlocks."""
    display_name = "Include Tech Skills, Weapon Skills, Stats, and Psi" 

class IncludeOSUpgrades(DefaultOnToggle):
    """Include OSUpgrades."""
    display_name = "Include OSUpgrades"

class IncludeStartingWrench(Toggle):
    """Include the wrench found on the first body in medsci."""
    display_name = "Include starting wrench"

class ManyIsVictory(Toggle):
    """Make The Many the victory condition instead of Shodan."""
    display_name = "The Many is victory condition."

class SS2StartHints(StartHints):
    default = ["Science Access Card"]

@dataclass
class SS2options(PerGameCommonOptions):
    include_stats_skills_psi: IncludeStatsSkillsPsi
    include_os_upgrades: IncludeOSUpgrades
    include_starting_wrench: IncludeStartingWrench
    many_is_victory: ManyIsVictory
    start_hints: SS2StartHints