import json


class file_handler:
    def __init__(self, file_path, mode, encoding='utf-8'):
        self.action = False
        self.encoding = encoding
        self.file = None
        self.filename = file_path
        self.mode = mode

    """
    This will be called when the object is used as a context manager (with statement).
    """

    def __enter__(self):
        try:
            self.file = open(self.filename, mode=self.mode, encoding=self.encoding)
            self.action = True
            return {"action": True, "file": self.file, "loaded_data": json.load(self.file)}

        except FileNotFoundError:
            return {"action": self.action}

        except json.decoder.JSONDecodeError:
            return {"action": self.action}

        except Exception:
            return {"action": self.action}

    """
    This will be called when (with statement) is finished.
    """

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file and not self.action:
            self.file.close()
