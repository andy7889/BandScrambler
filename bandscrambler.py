from lyricsgetter import LyricsGetter
import random
import sys

class BandScrambler:
    def __init__(self, artist):
        self.artist = artist
        self.lg = LyricsGetter(artist)
        self.songs = self.lg.get_all_lyrics()
        self.body = ""
        for song in self.songs:
            self.body += self.songs[song] + "\n"
        self.body = self.body.replace("\n", " \n")
        self.words = self.body.split(" ")
    def get_body(self):
        return " ".join(self.words)
    def scramble(self):
        for i in range(len(self.words)):
            word = self.words[i]
            matched = False
            while not matched:
                index = random.randint(0, len(self.words) - 1)
                other = self.words[index]
                if len(other) <= 3 or other == word:
                    continue
                self.words[index] = word
                self.words[i] = other
                matched = True
    def save(self):
        self.path = "%s BandScramble.txt" % self.artist
        with open(self.path, "w") as f:
            f.write(self.get_body())

if __name__ == "__main__":
    if len(sys.argv) == 1:
        keep_trying = True
        bs = None
        while keep_trying:
            keep_trying = False
            artist = input("What artist do you want to bandscramble? ")
            try:
                bs = BandScrambler(artist)
            except ValueError:
                keep_trying = True
                print("Invalid artist. Please try again.")
        bs.scramble()
        bs.save()
        print("Your bandscramble has been saved!")
        print("The file is %s" % bs.path)
    else:
        artist = " ".join(map(str, sys.argv[1:]))
        bs = BandScrambler(artist)
        bs.scramble()
        bs.save()