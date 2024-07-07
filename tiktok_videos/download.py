import os
import gdown
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'tiktok_videos/techjam.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)


def fetch_video_ids_from_folder(folder_id):
    query = f"'{folder_id}' in parents and mimeType='video/mp4'"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    video_ids = [item['id'] for item in items]
    return video_ids


def download_videos(tag, output_dir):
    folders = {
        "#AI - #MachineLearning - #TechInnovation": "1JYv-bd4bWg2LucmnS0631wqJCABAwA0g",
        "#Foodie - #RecipeOfTheDay - #CookingHacks": "1oGdZ8xWMq3bH74MhFL8PmDKOv5IK2p0I",
        "#MakeupTutorial - #BeautyHacks - #SkincareRoutine": "1bn2d-6tjDi9cb03uRwFG019B4CKjnyT7",
        "#OOTD - #FashionInspo - #StyleTips": "1axVn0xBJ41grkByuCdEOGNFJ-YjVIJST",
        "#TravelVlog - #HiddenGems - #TravelTips": "1Y1zbBzSWB_sbQp7P7Y4yAnX3UzWQtLfl"
    }

    folder_id = None
    for folder_name, fid in folders.items():
        if f"#{tag}" in folder_name.split(" - "):
            folder_id = fid
            break

    if not folder_id:
        return []

    video_ids = fetch_video_ids_from_folder(folder_id)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video_files = []
    for i, video_id in enumerate(video_ids):
        if i <= 2:
            video_url = f"https://drive.google.com/uc?id={video_id}"
            output_path = os.path.join(output_dir, f'video_{i + 1}.mp4')
            gdown.download(video_url, output_path, quiet=False)
            video_files.append(output_path)
        else:
            break

    return video_files
