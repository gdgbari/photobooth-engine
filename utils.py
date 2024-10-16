import os

def get_asset_path_from_name(asset_name : str) -> str:
    # WARNING: if this function is not in the main folder of the project,
    # it will not work properly
    current_working_dir = os.getcwd()
    output_path = os.path.join(current_working_dir,'Assets')
    output_path = os.path.join(output_path, asset_name)
    return output_path

def get_the_file_in_dir(folder_path :str) :

    files = os.listdir(folder_path)
    files_path = []
    for file_name in files:
        files_path.append(os.path.join(folder_path,file_name))

    return files_path[0], files[0]
