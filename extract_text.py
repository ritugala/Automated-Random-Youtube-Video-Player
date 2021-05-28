import bs4 as bs
import requests
import re
import json
import random
import pytube
import argparse
from pathlib import Path
import os
import datetime


def get_soup(link):
	headers = {
	        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
	        'Content-Type': 'text/html',
	}
	source = requests.get(link, headers=headers).text
	soup = bs.BeautifulSoup(source, 'lxml')
	# TODO: Only first 100 videos are found, others are not found coz they are loaded on scrolling
	return soup


def get_videos_list(soup):
	initDataVariable = soup.find(text=re.compile('ytInitialData'))
	initDataJSONString = initDataVariable[initDataVariable.index('{'):-1]  # -1 because string ends with ;
	initDataJSON = json.loads(initDataJSONString)

	videos = initDataJSON['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']
	videoIds = []
	for video in videos:
		if 'playlistVideoRenderer' in video:
			videoIds.append(video['playlistVideoRenderer']['videoId'])
	return videoIds


def download_video(today_video, output_path):
	link = "https://www.youtube.com/watch?v="+today_video
	yt = pytube.YouTube(link)
	stream = yt.streams.filter(file_extension='mp4').get_by_resolution('720p')
	filename=stream.default_filename.replace(" ", "-").replace("??", "-")
	file_path = output_path+"\\"+filename
	my_file = Path(file_path)
	if my_file.is_file():
		# Modify last_modified_date as rn.
		os.utime(file_path, (datetime.datetime.now().timestamp(), datetime.datetime.now().timestamp()))
	else:
		stream.download(output_path=output_path, filename=filename)


def main():
	parser = argparse.ArgumentParser(description="Provide additional output-file parameters and youtube link")
	parser.add_argument('-l', '--link', help='Youtube playlist link', required=False, default="https://www.youtube.com/playlist?list=PLE5lGVrS3V9dYEeiY79ix7gEkb1ucCSKD")
	parser.add_argument('-o', '--output-path', help='Output Directory for storing the video', required=False, default="C:\\Users\\Ritu\\Downloads\\HIIT-Downloads")
	args = parser.parse_args()

	soup = get_soup(args.link)
	videoList = get_videos_list(soup)
	todayVideo = random.choice(videoList)
	download_video(todayVideo, args.output_path)


if __name__ == "__main__":
	main()


