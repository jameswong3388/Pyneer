import json


class file_handler:
    def __init__(self, file_path, mode, encoding='utf-8'):
        self.filename = file_path
        self.file = None
        self.error = ""
        self.encoding = encoding
        self.mode = mode

    """
    This will be called when the object is used as a context manager (with statement).
    """
    def __enter__(self):
        try:
            self.file = open(self.filename, mode=self.mode, encoding=self.encoding)
            return {"message": self.error, "file": self.file, "loaded_data": json.load(self.file)}

        except FileNotFoundError as e:
            self.error = str(e)
            return {"message": self.error}

        except json.decoder.JSONDecodeError as e:
            self.error = str(e)
            return {"message": self.error}

        except Exception as e:
            self.error = str(e)
            return {"message": self.error}

    """
    This will be called when (with statement) is finished.
    """
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file and not self.error:
            self.file.close()
