
class SyllabiPDFTextExtractor:
    

    def __init__(self, folder_path):
        self.folder_path = folder_path


    def set_folder_path(self, folder_path):
        self.folder_path = folder_path
    
    
    def get_folder_path(self):
        return self.folder_path
