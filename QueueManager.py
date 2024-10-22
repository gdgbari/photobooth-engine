from types import NoneType

import yaml

class QueueManager:

    def __init__(self):
        self._queue_path = 'queue.yaml'
        self._dict = {'photos':[],'edits':[]}

    def queue_is_ready(self):
        return len(self._dict['photos']) >= 2

    def add_photo(self, photo_path):
        self._dict['photos'].append(photo_path)
        with open(self._queue_path, 'w') as file:
            yaml.dump(self._dict, file, default_flow_style=False, allow_unicode=True)

    def add_edit(self, edit_path):
        self._dict['edits'].append(edit_path)
        with open(self._queue_path, 'w') as file:
            yaml.dump(self._dict, file, default_flow_style=False, allow_unicode=True)

    def get_two_photos(self)-> list[str]:
        photos = self._dict['photos'][-2:]  # get last 2 photos from the queue
        self._dict['photos'] = self._dict['photos'][:-2]  # delete last 2 photos from the queue
        with open(self._queue_path, 'w') as file:
            yaml.dump(self._dict, file, default_flow_style=False, allow_unicode=True)
        return photos

    def get_two_edit(self) -> list[str]:
        edits = self._dict['edits'][-2:]
        self._dict['edits'] = self._dict['edits'][:-2]
        with open(self._queue_path, 'w') as file:
            yaml.dump(self._dict, file, default_flow_style=False, allow_unicode=True)
        return edits

    def load_queue(self):
        with open(self._queue_path, 'r') as file:
            yaml_dict = yaml.load(file, Loader=yaml.FullLoader)
        if yaml_dict is not None:
            self._dict['photos'] = yaml_dict['photos']
            self._dict['edits'] = yaml_dict['edits']

    def dismiss(self):
        dict = {'photos': [], 'edits': []}
        with open(self._queue_path, 'w') as file:
            yaml.dump(dict, file, default_flow_style=False, allow_unicode=True)


#DEBUG
# manager = QueueManager()
# manager.load_queue()
# manager.add_photo('ciao')
# manager.add_photo('ciaone')
# if manager.queue_is_ready():
#     print(manager.get_two_photos())
# manager.dismiss()