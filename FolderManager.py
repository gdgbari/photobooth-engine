# FOLDERS EXPLANATION
#
#    main_folder
#       |___________> current       [ here the current shots: in future the user would choose from different shots]
#       |___________> originals     [ all the originals chosen shots                                              ]
#       |___________> output        [ all the outputs: cropped and cornered                                       ]
#

class FolderManager:

    def __init__(self, main_folder_path: str):

        self._main_folder_path = main_folder_path
        # now the paths of all the sub-folders
        self._current_folder_path = main_folder_path + '\\current'
        self._originals_folder_path = main_folder_path + '\\originals'
        self._output_folder_path = main_folder_path + '\\output'

        # then we check the folders consistency
        self._folder_consistency_assurance()

    def _folder_consistency_assurance(self):
        # if the sub-folders misses, will be created
        print('yeah ill do it later, it will work')