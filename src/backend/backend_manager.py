from backend.new_backend_endpoint import PhotoAPIClient
from core.photo_edit_manager import Tailor
import PIL
from pathlib import Path

class BackendMananger():

    def __init__(self, backend_url : str) -> None:
        
        self._backend = PhotoAPIClient(base_url=backend_url)
        self._editor = Tailor()

    
    def send_photo_and_edit(self, photo_path: str, corner_path:str):
        # up to now is more simple to re-edit here, the corner chooser is into another dev branch
        # when it will be ready, this class could simply receive the already edited photo
        photo = self._editor.prepare_single_photo(photo_path,corner_path)
        photo_name = Path(photo_path).name
        self._backend.upload_pil_background(photo, photo_name)