import re
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LoadClientConfigFile("owlDjango/googleDrive/client_secrets.json")
gauth.LoadCredentialsFile("owlDjango/googleDrive/credentials.json")
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()
gauth.SaveCredentialsFile("owlDjango/googleDrive/credentials.json")
drive = GoogleDrive(gauth)

def get_drive_client():
    return drive

def extract_folder_id_from_url(url):
    pattern = r"https://drive\.google\.com/drive/folders/([a-zA-Z0-9_-]+)"
    match = re.match(pattern, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid Google Drive URL.")

def list_image_files_in_folder(url):
    folder_id = extract_folder_id_from_url(url)
    query = f"'{folder_id}' in parents and trashed=false"
    file_list = drive.ListFile({'q': query}).GetList()
    image_files = [file for file in file_list if file['mimeType'].startswith('image/')]
    return image_files
