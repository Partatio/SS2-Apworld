import settings

class SS2Settings(settings.Group):
    class SS2folder(settings.UserFolderPath):
        """Folder path of your System Shock 2 installation"""
        description = "System Shock 2 installation folder"
    
    ss2_path: SS2folder = SS2folder("C:/Program Files (x86)/Steam/steamapps/common/SS2")