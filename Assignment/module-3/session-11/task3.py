'''Write a Python script using pymysql to fetch and display all playlists from the music_stream
 database where song_count is greater than 10, showing the playlist name and song_count only.'''

import pymysql

try:
    # Connect to MySQL
    connection = pymysql.connect(
        host="localhost",
        user="root",           
        password="",  
        database="music_stream"
    )

    cursor = connection.cursor()

    # Fetch playlists with song_count > 10
    query = "SELECT name, song_count FROM playlists WHERE song_count > 10"
    cursor.execute(query)

    records = cursor.fetchall()

    print("Playlist Name\t\tSong Count")
    print("-" * 35)

    for row in records:
        print(f"{row[0]}\t\t{row[1]}")

    cursor.close()
    connection.close()

except pymysql.MySQLError as e:
    print("Error:", e)