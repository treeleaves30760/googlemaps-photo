from scrap import GooglePlacesPhotoDownloader

downloader = GooglePlacesPhotoDownloader('Photos')

downloader.download_photos_for_place('台北101', max_photos=50)
downloader.download_photos_for_place('故宮', max_photos=50)
downloader.download_photos_for_place('國立清華大學', max_photos=50)
