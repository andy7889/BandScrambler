from bs4 import BeautifulSoup
import requests
import os

def get_soup(url):
    response = requests.get(url)
    if response.status_code == 404:
        raise ValueError("Invalid artist/not listed")
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

class LyricsGetter:
    def __init__(self, artist):
        self.artist = artist
        url = LyricsGetter.format_url(artist)
        self.soup = get_soup(url)
        name = LyricsGetter.format_name(artist)
        self.path = os.path.join("artists", name)
        self.save()
    def get_song_urls(self):
        links = self.soup.find_all("a")
        urls=[]
        for a in links:
            try:
                urls.append(a["href"])
            except:
                pass
        artist = LyricsGetter.format_name(self.artist)
        urls = filter(lambda url: artist in url, urls)
        return list(urls)
    def get_song_lyrics(self, soup):
        verses = None
        try:
            verses = soup.find_all("p", class_="verse")
        except:
            return None
        if verses == None:
            return None
        result = ""
        for verse in verses:
            result += verse.text + "\n"
        return result
    def get_all_songs(self):
        urls = self.get_song_urls()
        songs = {}
        for url in urls:
            soup = get_soup(url)
            lyrics = self.get_song_lyrics(soup)
            if len(lyrics) < 1:
                continue
            songs[soup.title.text] = self.get_song_lyrics(soup)
        return dict(songs)
    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        else:
            return
        print("Getting all song lyrics from artist %s..." % self.artist)
        self.songs = self.get_all_songs()
        for song in self.songs:
            filename = song + ".txt"
            full_path = os.path.join(self.path, filename)
            if os.path.isfile(full_path):
                continue
            with open(full_path, "w") as f:
                f.write(self.songs[song])
        print("Done.")
    def get_all_lyrics(self):
        songs = {}
        for file in os.listdir(self.path):
            full = os.path.join(self.path, file)
            with open(full, "r") as f:
                songs[file] = str(f.read())
        return songs
    @staticmethod
    def format_name(artist):
        return artist.lower().replace(" ", "-")
    @staticmethod
    def format_url(artist):
        base_url="https://www.metrolyrics.com/%s-lyrics.html"
        return base_url % LyricsGetter.format_name(artist)
    @staticmethod
    def request(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.html
