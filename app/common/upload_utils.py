import os


class UploadUtils:
    @staticmethod
    def is_valid_file(file, authorized_extensions, max_file_size):
        file.seek(0, os.SEEK_END)
        size = file.tell()
        extension = file.filename.rsplit(".", 1)[1].lower()
        return (
            size < max_file_size
            and file.filename != ""
            and "." in file.filename
            and extension in authorized_extensions
        )
