import sqlite3

from tinytag import TinyTag
from playsound import playsound


def createPlaylists():
    try:
        c.execute("""CREATE TABLE Playlists
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT, Name UNIQUE, Description)""")
        c.execute("""CREATE TABLE PlaylistsSongs
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT, NameOfSong, PlaylistID INTEGER,
                        FOREIGN KEY(PlaylistID) REFERENCES Playlists(ID))""")
    except:
        pass


def createArtists():
    try:
        c.execute("""CREATE TABLE Artists
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT, Name, DateofBirth)""")
    except:
        pass


def createAlbums():
    try:
        c.execute("""CREATE TABLE Albums
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT, Name, BandName, NOofSongs)""")
        c.execute("""CREATE TABLE AlbumsSongs
                         (ID INTEGER PRIMARY KEY AUTOINCREMENT, NameOfSong, AlbumID INTEGER,
                                FOREIGN KEY(AlbumID) REFERENCES Album(ID))""")
    except:
        pass


def createSongs():
    try:
        c.execute("""CREATE TABLE Songs
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT, Name, Band, Artist, Album, DateofIt, Genre, Length, Path)""")
    except:
        pass


'''--------------------------------------------------------------------------------------------------------------------------------------------------------'''


def update():
    c.execute("""UPDATE playlist SET numbers = 0 WHERE albumNames = 'Mixed Songs' """)


def delete():
    c.execute("""DELETE from playlist WHERE albumNames = 'Anime Tracks' """)


def select(verbose=True):
    sql = "SELECT * FROM playlist"
    recs = c.execute(sql)
    if verbose:
        for row in recs:
            print(row)


# Marwa
def viewPlayLists():
    print('     -Playlists-    ')
    sql = "SELECT * FROM Playlists"
    recs = c.execute(sql)
    for row in recs:
        print('* ', row)


def viewAlbums():
    print('     -Albums-    ')
    sql = "SELECT * FROM Albums"
    recs = c.execute(sql)
    for row in recs:
        print('* ', row)


def viewArtists():
    print('     -Artists-    ')
    sql = "SELECT * FROM Artists"
    recs = c.execute(sql)
    for row in recs:
        print('* ', row)


def viewSongs():
    sql = "SELECT * FROM Songs"
    recs = c.execute(sql)
    print('      -Songs-      ')
    for row in recs:
        print('* ', row)


def viewPlaylistDescription(playlistName):
    recs = c.execute("""SELECT Description FROM Playlists WHERE Name=?""", (playlistName,))
    for row in recs:
        print('Playlist Name: ', playlistName, ' Des: ', row)


def Order(orderby):
    if orderby == 1:
        sql = "SELECT * FROM PlaylistS ORDER by Name"
        recs = c.execute(sql)
        for row in recs:
            print(row)
    elif orderby == 2:
        sql = "SELECT * FROM PlaylistS ORDER by Name DESC"
        recs = c.execute(sql)
        for row in recs:
            print(row)


'''-----------------------------------------------------------------------------------------------------------------------------------------------'''

# Mariam

NOOFSONGS = 0


def addNewPlaylist(name, description):
    c.execute("""INSERT INTO Playlists (Name, Description)
              values(?, ?)""", (name, description))
    print("inserted successfully")


def addArtist(name, date):
    c.execute("""INSERT INTO ARTISTS (Name, DateofBirth)
      values (?, ?)""", (name, date))
    print("inserted successfully")


def addAlbum(name, artist):
    c.execute("""INSERT INTO Albums (Name, BandName)
              values(?, ?)""", (name, artist))


def IDofPlaylist(playlistName):
    verbose = True
    recs = c.execute("""SELECT ID FROM Playlists WHERE Name=?""", (playlistName,))
    if verbose:
        for row in recs:
            print(row[0])
            return row[0]


def IDofAlbum(albumName):
    verbose = True
    recs = c.execute("""SELECT ID FROM Albums WHERE Name=?""", (albumName,))
    if verbose:
        for row in recs:
            print(row[0])
            return row[0]


def sum (idd, print_out=True):
    c.execute("""SELECT COUNT(*) FROM AlbumsSongs WHERE AlbumID = ?""", (idd,))
    print (idd)
    count = c.fetchall()
    count = format(count[0][0])
    if print_out:
        print ("k")
        print (count)
    return count


def addSong(path, playlistName):
    tag = TinyTag.get(path)
    name = tag.title
    artist = tag.artist
    album = tag.album
    date = tag.year
    genre = tag.genre
    length = int(tag.duration) / 60
    c.execute("""INSERT INTO Songs (Name, Artist, Album, DateofIt, Genre, Length, Path)
              VALUES(?, ?, ?, ?, ?, ?, ?)""", (name, artist, album, date, genre, length, path))
    a = IDofPlaylist(playlistName)
    c.execute("""INSERT INTO PlaylistsSongs (NameOfSong, PlaylistID)
              values(?, ?)""", (name, a))

    c.execute("SELECT EXISTS(SELECT 1 FROM Albums WHERE Name = ? LIMIT 1)", (album,))
    record = c.fetchone()
    if record[0] == 1:
        print(album)
        print("Name is in the table")
    else:
        print(album)
        print("Name not in table")
        addAlbum(album, artist)
    idd = IDofAlbum(album)
    c.execute("""INSERT INTO AlbumsSongs (NameOfSong, AlbumID)
                      values(?, ?)""", (name, idd))
    s = sum(idd, True)
    c.execute("""UPDATE Albums SET NOofSongs = ? WHERE ID = ?""", (s, idd))


def deletePlaylist(playlistname):
    c.execute('DELETE FROM Playlists WHERE Name=?', (playlistname,))


def deleteSong(songName):
    c.execute('DELETE FROM Songs WHERE Name=?', (songName,))


def deleteAlbum(albumName):
    c.execute('DELETE FROM Albums WHERE Name=?', (albumName,))


def deleteArtist(artistName):
    c.execute('DELETE FROM Artists WHERE Name=?', (artistName,))


def removesong(songName, playlistid):
    c.execute('DELETE FROM PlaylistsSongs WHERE NameOfSong=? AND PlaylistID=?', (songName, playlistid))


'''---------------------------------------------------------------------------------------------------------------------------------------------'''


# nagham


def playAlbum(album_name):
    connection = sqlite3.connect(db_path)
    c = connection.cursor()
    sql = "SELECT Songs.Path FROM Songs WHERE Songs.Album=(?)"
    c.execute(sql, (album_name,))
    for row in c:
        playsound(row[0], True)
    c.close()


def playBand(band_name):
    connection = sqlite3.connect(db_path)
    c = connection.cursor()
    sql = "SELECT Songs.Path FROM Songs WHERE Songs.Band=(?)"
    c.execute(sql, (band_name,))
    for row in c:
        playsound(row[0], True)
    c.close()


def playArtist(artist_name):
    connection = sqlite3.connect(db_path)
    c = connection.cursor()
    sql = "SELECT Songs.Path FROM Songs WHERE Songs.Artist=(?)"
    c.execute(sql, (artist_name,))
    for row in c:
        # print(row[0])
        playsound(row[0])
    c.close()


def playGenre(song_genre):
    connection = sqlite3.connect(db_path)
    c = connection.cursor()
    sql = "SELECT Songs.Path FROM Songs WHERE Songs.Genre=(?)"
    c.execute(sql, (song_genre,))
    for row in c:
        playsound(row[0], True)
    c.close()


'''---------------------------------------------------------------------------------------------------------------------------------'''

db_path = r'C:\Users\Belal\Desktop\concepts\database.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
createPlaylists()
createArtists()
createAlbums()
createSongs()


'''-------------------------------------------------------------------------------------------'''
print("----------MUSIC APP----------")

print("Enter 1 to view Playlists")
print("Enter 2 to view Albums")
print("Enter 3 to view Artists")
print("Enter 4 to view Song details")
print("Enter 5 to view Playlist Details")
print("Enter 6 to view Playlists Order")
print("Enter 7 to Play Album")
print("Enter 8 to Play Songs to band")
print("Enter 9 to Play Songs to artist")
print("Enter 10 to Play Songs to Genre")
print("Enter 11 to Add Playlist")
print("Enter 12 to Add Song")
print("Enter 13 to Add Artist")
print("Enter 14 to Add Album")
print("Enter 15 to Remove Song from Playlist")
print("Enter 16 to Remove Playlist")
print("Enter 17 to Remove Song")
print("Enter 18 to Remove Album")
print("Enter 19 to Remove Artist")
num = int(input("Enter the num."))
if num == 1:
    viewPlayLists()
elif num == 2:
    viewAlbums()
elif num == 3:
    viewArtists()
elif num == 4:
    viewSongs()
elif num == 5:
    name = raw_input("Enter the name of the playlist you want to view.")
    viewPlaylistDescription(name)
elif num == 6:
    print("1. Name Asc")
    print("2. Name Decs")
    orderby = raw_input("Enter the Order of the playlist you want to view.")
    Order(orderby)
elif num == 7:
    name = raw_input("Enter the name of the album you want to play.")
    playAlbum(name)
elif num == 8:
    name = raw_input("Enter the name of the band you want to play.")
    playBand(name)
elif num == 9:
    name = raw_input("Enter the name of the artist you want to play.")
    playArtist(name)
elif num == 10:
    name = raw_input("Enter the name of the Genre you want to play.")
    playGenre(name)
elif num == 11:
    name = raw_input("Enter the name of the playlist you want to add.")
    description = raw_input("Enter the description.")
    addNewPlaylist(name, description)
elif num == 12:
    path = raw_input("Enter the path of the Song you want to add.")
    playlistName = raw_input("Enter the name of the playlist you want to add in.")
    addSong(path, playlistName)
elif num == 13:
    artist = raw_input("Enter the Artist you want to add.")
    date = raw_input("Date of Birth.")
    addArtist(artist, date)
elif num == 14:
    album = raw_input("Enter the Album you want to add: ")
    artist = raw_input("Enter the Artist of the album.")
    addAlbum(album, artist)
elif num == 15:
    songName = raw_input("Enter the Song you want to delete.")
    PlaylistID = raw_input("Enter the playlist ID you want to delete.")
    removesong(songName, PlaylistID)
elif num == 16:
    deletedPlaylist = raw_input("Enter the PlayList you want to delete.")
    deletePlaylist(deletedPlaylist)
elif num == 17:
    deletedSong = raw_input("Enter the Song you want to delete.")
    deleteSong(deletedSong)
elif num == 18:
    deletedAlbum = raw_input("Enter the Album you want to delete.")
    deleteAlbum(deletedAlbum)
elif num == 19:
    deletedArtist = raw_input("Enter the Artist you want to delete.")
    deleteArtist(deletedArtist)
else:
    exit()

conn.commit()
c.close()
