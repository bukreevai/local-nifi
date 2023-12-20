import gzip
from os import (
    path,
    remove,
    makedirs
)
import shutil


class Zipper:
    @staticmethod
    def unzip(
        source_path:str,
        target_path:str = None,
        keep_source: bool = True
    ):
        """
        Unpacks a gzip file with a modified target handling.

        :param source_path: Path to the source gzip file.
        :param target_path: Path to the target directory. If not specified, unpacks in the same directory as the source.
                      If specified, appends the original file name to the target path.
        :param keep_source: If True, keeps the source gzip file, otherwise deletes it.
        """
        # Extract the file name from the source path
        file_name = path.basename(path.splitext(source_path)[0])

        # Set the target file path
        if target_path:
            if not path.isdir(target_path):
                makedirs(target_path, exist_ok=True)
            target_path = path.join(target_path, file_name)
        else:
            target_path = path.join(path.dirname(source_path), file_name)

        # Unpacking the gzip file
        with gzip.open(source_path, 'rb') as f_in:
            with open(target_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Remove the source_path file if not keeping it
        if not keep_source:
            remove(source_path)

    @staticmethod
    def zip_file(
        source_path:str,
        target_path:str = None,
        keep_source: bool = True
    ):
        """
        Packs a file into a gzip archive with a modified target handling.

        :param source_path: Path to the source file to be compressed.
        :param target_path: Path to the target directory. If not specified, creates a gzip file in the same directory as the source.
                      If specified, appends the original file name with '.gz' extension to the target path.
        :param keep_source: If True, keeps the source file, otherwise deletes it after compression.
        """
        # Extract the file name from the source path and add the .gz extension
        file_name = path.basename(source_path) + '.gz'
        
        # Set the target file path
        if target_path:
            if not path.isdir(target_path):
                makedirs(target_path, exist_ok=True)
            target_path = path.join(target_path, file_name)
        else:
            target_path = path.join(path.dirname(source_path), file_name)
        
        # Compressing the file into a gzip file
        with open(source_path, 'rb') as f_in:
            with gzip.open(target_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Remove the source file if not keeping it
        if not keep_source:
                remove(source_path)  