import json
import os
import time
import requests
from dotenv import load_dotenv
import googlemaps


class GoogleMapsPhotoDownloader:
    def __init__(self, output_dir="Photos"):
        load_dotenv()
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not self.api_key:
            raise ValueError("請在 .env 檔案中設定 GOOGLE_MAPS_API_KEY")

        self.gmaps = googlemaps.Client(key=self.api_key)
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def get_place_id(self, query):
        try:
            result = self.gmaps.find_place(
                query, 'textquery', fields=['place_id'])
            if result['status'] == 'OK':
                return result['candidates'][0]['place_id']
            else:
                print(f"無法找到地點: {query}")
                return None
        except Exception as e:
            print(f"獲取地點ID時發生錯誤: {str(e)}")
            return None

    def get_place_photos(self, place_id):
        try:
            result = self.gmaps.place(place_id, fields=['photo'])
            if 'result' in result and 'photos' in result['result']:
                return result['result']['photos']
            else:
                print("無法獲取照片信息")
                return []
        except Exception as e:
            print(f"獲取照片信息時發生錯誤: {str(e)}")
            return []

    def download_photo(self, photo_reference, filename, max_width):
        try:
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
                return True
            else:
                print(f"下載照片失敗: {filename}, 狀態碼: {response.status_code}")
                return False
        except Exception as e:
            print(f"下載照片時發生錯誤: {str(e)}")
            return False

    def download_photos_for_place(self, query, max_width=800, max_photos=5):
        try:
            # 獲取地點ID
            place_id = self.get_place_id(query)
            if not place_id:
                return

            # 獲取照片列表
            photos = self.get_place_photos(place_id)
            if not photos:
                return

            # 限制照片數量
            if max_photos:
                photos = photos[:max_photos]

            # 下載照片
            success_count = 0
            for i, photo in enumerate(photos):
                filename = os.path.join(self.output_dir, f"{query}-{i+1}.jpg")
                if self.download_photo(photo['photo_reference'], filename, max_width):
                    success_count += 1
                time.sleep(1)  # 添加延遲以避免限制

            print(f"完成下載 {query} 的照片: 成功 {success_count}/{len(photos)}")

        except Exception as e:
            print(f"處理地點 {query} 時發生錯誤: {str(e)}")


if __name__ == "__main__":
    # 範例使用
    downloader = GoogleMapsPhotoDownloader("Image")

    # 從JSON檔案讀取地點列表
    try:
        with open('TW_List.json', encoding='utf-8') as f:
            data = json.load(f)['TW_Attractions']

        for place in data:
            print(f"\n開始處理地點: {place}")
            downloader.download_photos_for_place(
                place, max_width=800, max_photos=5)
            time.sleep(3)  # 在處理不同地點之間添加延遲

    except Exception as e:
        print(f"主程序發生錯誤: {str(e)}")
