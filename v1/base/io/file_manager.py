import os
import json
import logging
from pathlib import Path
import shutil

logger = logging.getLogger(__file__)


class FileManager(object):
    def __init__(self, file_directory=os.getcwd()):
        pass

    @classmethod
    def read_all_files(cls, directory, valid_extensions=[".csv"], reverse=False):
        files = []
        if not os.path.exists(directory):
            return []
        for f in os.listdir(directory):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_extensions:
                continue
            files += [f]
        return sorted(files, reverse=reverse)

    @classmethod
    def delete_file(cls, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    @classmethod
    def remove_directory(cls, directory):
        if os.path.exists(directory):
            shutil.rmtree(directory)

    @classmethod
    def get_file_name(cls, file_path):
        base_file_name = Path(file_path).name
        return base_file_name

    @classmethod
    def read_json(cls, file_path):
        logger.info("Reading file: %s" % file_path)
        file_data = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if content:
                    file_data = json.loads(content)
                    logger.info("File read done with contents: %s" % str(file_data))
                else:
                    logger.warning("No file data")
        except Exception as exp:
            logger.warning("Exception: %s" % str(exp))
        return file_data

    @classmethod
    def write_json(cls, file_path, data):
        with open(file_path, "w", encoding='utf-8', newline='\n') as tf:
            json.dump(data, tf)


if __name__ == "__main__":
    pass

