# scrap.py

import os
import requests
import googlemaps
from dotenv import load_dotenv


class GooglePlacesPhotoDownloader:
    def __init__(self, output_dir="Photos"):
        load_dotenv()
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        self.gmaps = googlemaps.Client(key=self.api_key)
        self.output_dir = output_dir

    def get_place_id(self, query):
        result = self.gmaps.find_place(query, 'textquery', fields=['place_id'])
        if result['status'] == 'OK':
            return result['candidates'][0]['place_id']
        else:
            raise Exception("無法找到地點")

    def get_place_photos(self, place_id):
        result = self.gmaps.place(place_id, fields=['photo'])
        if 'result' in result and 'photos' in result['result']:
            return result['result']['photos']
        else:
            print("警告：無法獲取照片信息")
            return []

    def download_photo(self, photo_reference, filename, max_width):
        url = "https://maps.googleapis.com/maps/api/place/photo"
        params = {
            "maxwidth": max_width,
            "photoreference": photo_reference,
            "key": self.api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"已下載: {filename}")
        else:
            print(f"下載照片失敗: {filename}")

    def download_photos_for_place(self, query, max_width=400, max_photos=None):
        try:
            place_id = self.get_place_id(query)
            photos = self.get_place_photos(place_id)

            if not photos:
                print("沒有找到照片")
                return

            place_dir = os.path.join(self.output_dir, query)
            if not os.path.exists(place_dir):
                os.makedirs(place_dir)

            # 限制照片數量
            if max_photos:
                photos = photos[:max_photos]

            for i, photo in enumerate(photos):
                filename = os.path.join(place_dir, f"{i+1}.jpg")
                self.download_photo(
                    photo['photo_reference'], filename, max_width)
        except Exception as e:
            print(f"發生錯誤: {str(e)}")


if __name__ == "__main__":
    # 範例使用
    downloader = GooglePlacesPhotoDownloader("Photos")

    # 下載國立清華大學的照片，最大寬度800像素，最多5張
    downloader.download_photos_for_place("國立清華大學", max_width=800, max_photos=5)

    # 下載台北101的照片，最大寬度1600像素，不限數量則預設10張
    downloader.download_photos_for_place("台北101", max_width=1600)
