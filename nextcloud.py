
from json import dumps
from nc_py_api import Nextcloud, NextcloudException
import os


def init_nextcloud(nc_base_url: str, nc_user: str, nc_pass: str) -> Nextcloud:
    return Nextcloud(nextcloud_url=nc_base_url, nc_auth_user=nc_user, nc_auth_pass=nc_pass)


def upload_and_delete_file(nc: Nextcloud, path: str) -> bool:
    """
    Upload file. Return true if successful and delete file.
    Return false and keep file if unsuccessful.
    """
    filename = path.split('/')[-1]
    # upload file
    try: 
        nc.files.upload_stream(path=f"CCTV/{filename}", fp=path)
        print(f"Successfully uploaded {filename}")
    except NextcloudException as e:
        # failed upload
        print(f"Failed to upload {filename}, because of NextCloudException: {e}")
        return False

    try: 
        os.remove(path=path)
        print(f"Deleted {path}")
    except FileNotFoundError as e:
        # just catch the error. If file is already gone don't worry about it.
        pass

    return True


if __name__ == "__main__":

    nc_base_url = os.environ.get("NC_BASE_URL", "localhost:5432")
    nc_user = os.environ.get("NC_USER", "")
    nc_pass = os.environ.get("NC_PASS", "")

    nc = init_nextcloud(nc_base_url=nc_base_url, nc_user=nc_user, nc_pass=nc_pass)

    upload_and_delete_file(nc, "img/photo_2024_2_24_21_48_46___5INK.jpg")