import os

try:
    from folder_paths import get_output_directory as _get_output_directory
except Exception:
    def _get_output_directory():
        return os.path.join(os.getcwd(), "output")


def get_output_directory():
    return _get_output_directory()
