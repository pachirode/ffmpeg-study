from pathlib import Path

from utils.log import LoggerManager

logger = LoggerManager.get_logger()


class FilePathUtils:
    def __init__(self):
        self.base = Path("/")

    def get_back(self):
        if self.base == Path("/"):
            return self.base.__str__()
        self.base = self.base.parent
        return self.base.__str__()

    def get_child(self, child):
        self.base = self.base / child
        return self.base.__str__()


if __name__ == '__main__':
    file_path = FilePathUtils()
    print(file_path.base)
