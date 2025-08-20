import settings

class SS2Settings(settings.Group):
    class SS2folder(settings.UserFolderPath):
        """Path to your System Shock 2 installation root directory.  If manually changed make sure to use forward slashes.  Default folder names are "SS2" for classic and "System Shock 2 Remastered" for ae."""
        description = "System Shock 2 installation folder"
    
    ss2_path: SS2folder = SS2folder("C:/Program Files (x86)/Steam/steamapps/common/System Shock 2 Remastered")