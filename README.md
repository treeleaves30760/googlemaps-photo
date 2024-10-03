# Google Map Photo Scrapper

This is a Scrapper for Google map photo

## Install

Request a Google Map API token from google
Copy the .env.example and rename as .env
Replace the Word in .env

```ENV
GOOGLE_MAPS_API_KEY=yours google API token
```

Then install the requirements.txt

```bash
pip install googlemaps --use-pep517
pip install -r requirements.txt 
```

## Usage

```python
from scrap import GooglePlacesPhotoDownloader

downloader = GooglePlacesPhotoDownloader("Photos")

# 下載國立清華大學的照片，最大寬度800像素，最多5張
downloader.download_photos_for_place("國立清華大學", max_width=800, max_photos=5)

# 下載台北101的照片，最大寬度1600像素，不限數量則預設10張
downloader.download_photos_for_place("台北101", max_width=1600)
```
