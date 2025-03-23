# from types import NoneType
import yaml


class QueueManager:

    def __init__(self):
        self._queue_path = 'temp_data.yaml'
        self._dict = {'photos':[],'edits':[]}

    def _update_yaml(self):
        with open(self._queue_path, 'r') as f:
            yaml_dict = yaml.safe_load(f)
        yaml_dict['photos'] = self._dict['photos']
        yaml_dict['edits'] = self._dict['edits']
        with open(self._queue_path, 'w') as f:
            yaml.dump(yaml_dict, f, default_flow_style=False, allow_unicode=True)

    def queue_is_ready(self):
        return len(self._dict['photos']) >= 2

    def add_photo(self, photo_path, times):
        for _ in range(times):
            self._dict['photos'].append(photo_path)
        self._update_yaml()

    def add_edit(self, edit_path, times):
        for _ in range(times):
            self._dict['edits'].append(edit_path)
        self._update_yaml()

    def get_two_photos(self)-> list[str]:
        photos = self._dict['photos'][:2]  # get first 2 photos from the queue
        # self._dict['photos'] = self._dict['photos'][:-2]  # delete last 2 photos from the queue
        del self._dict['photos'][:2]
        self._update_yaml()
        return photos

    def get_two_edit(self) -> list[str]:
        edits = self._dict['edits'][:2]
        # self._dict['edits'] = self._dict['edits'][:-2]
        del self._dict['edits'][:2]
        self._update_yaml()
        return edits

    def load_queue(self):
        with open(self._queue_path, 'r') as file:
            yaml_dict = yaml.load(file, Loader=yaml.FullLoader)
        if yaml_dict is not None:
            self._dict['photos'] = yaml_dict['photos']
            self._dict['edits'] = yaml_dict['edits']

    def dismiss(self):
        self._dict = {'photos': [], 'edits': []}
        self._update_yaml()


#DEBUG
# manager = QueueManager()
# manager.load_queue()
# manager.add_photo('ciao')
# manager.add_photo('ciaone')
# if manager.queue_is_ready():
#     print(manager.get_two_photos())
# manager.dismiss()
