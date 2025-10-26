import yaml


'''
QueueManager class manages the photo and edit queues.
It provides methods to add photos and edits to the queues, check if the photo queue is ready, and get photos and edits from the queues.
'''

class QueueManager:

    def __init__(self):
        self._queue_path = 'temp_data.yaml'
        self._dict = {'photos':[],'edits':[]}

    def _update_yaml(self):
        '''
        Method which updates the yaml file with the current queues.
        '''

        with open(self._queue_path, 'r') as f:
            yaml_dict = yaml.safe_load(f)
        yaml_dict['photos'] = self._dict['photos']
        yaml_dict['edits'] = self._dict['edits']
        with open(self._queue_path, 'w') as f:
            yaml.dump(yaml_dict, f, default_flow_style=False, allow_unicode=True)

    def queue_is_ready(self):
        '''
        Method which checks if there are at least 2 photos in the photo queue.
        :return: True if there are at least 2 photos, False otherwise
        '''

        return len(self._dict['photos']) >= 2

    def add_photo(self, photo_path, times):
        '''
        Method which adds a photo to the photo queue according to the number of prints required.
        Then it updates the temp_data.yaml file.
        :param photo_path: photo path to add
        :param times: times number to add the photo
        '''

        for _ in range(times):
            self._dict['photos'].append(photo_path)
        self._update_yaml()

    def add_edit(self, edit_path, times):
        '''
        Method which adds an edit to the edit queue according to the number of prints required.
        Then it updates the temp_data.yaml file.
        :param edit_path: edit path to add
        :param times: times number to add the edit
        '''

        for _ in range(times):
            self._dict['edits'].append(edit_path)
        self._update_yaml()

    def get_two_photos(self)-> list[str]:
        '''
        Method which gets the first two photo from the photo queue and removes them from the queue.
        Then it updates the temp_data.yaml file.
        :return: two photo paths list
        '''

        photos = self._dict['photos'][:2]  # get first 2 photos from the queue
        # self._dict['photos'] = self._dict['photos'][:-2]  # delete last 2 photos from the queue
        del self._dict['photos'][:2]
        self._update_yaml()
        return photos

    def get_two_edit(self) -> list[str]:
        '''
        Method which gets the first two edit from the edit queue and removes them from the queue.
        Then it updates the temp_data.yaml file.
        :return: two edit paths list
        '''

        edits = self._dict['edits'][:2]
        # self._dict['edits'] = self._dict['edits'][:-2]
        del self._dict['edits'][:2]
        self._update_yaml()
        return edits

    def load_queue(self):
        '''
        Method which loads photo and edit queues from the temp_data.yaml file.
        '''

        with open(self._queue_path, 'r') as file:
            yaml_dict = yaml.load(file, Loader=yaml.FullLoader)
        if yaml_dict is not None:
            self._dict['photos'] = yaml_dict['photos']
            self._dict['edits'] = yaml_dict['edits']

    def dismiss(self):
        '''
        Method which clears the photo and edit queues and updates the temp_data.yaml file.
        '''

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