import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = "apikey"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=query,
        type="video",
        part="id,snippet",
        maxResults=100
    ).execute()

    videos = []
    # Add each result to the list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result)

    # Fetch video statistics for each video
    video_data = []
    for video in videos:
        video_id = video["id"]["videoId"]
        video_response = youtube.videos().list(
            id=video_id,
            part="snippet,statistics"
        ).execute()

        # Extract the relevant information from the API response
        title = video_response["items"][0]["snippet"]["title"]
        channel = video_response["items"][0]["snippet"]["channelTitle"]
        views = video_response["items"][0]["statistics"]["viewCount"]
        likes = video_response["items"][0]["statistics"]["likeCount"]
        comments = video_response["items"][0]["statistics"]["commentCount"]

        video_data.append((title, channel, views, likes, comments))

    return video_data

if __name__ == "__main__":
    query = input("Enter your search query: ")
    video_data = youtube_search(query)

    # Save the data to a CSV file
    with open("youtube_data.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Title", "Channel", "Views", "Likes",  "Comments"])
        writer.writerows(video_data)
