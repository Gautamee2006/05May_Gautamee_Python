'''Suppose you want to build a 'Recently Played' feature like Spotify. Write a Python function 
using pymysql that deletes a playlist from the playlists table by its id, and handles the case 
where the id does not exist by printing an appropriate message.<br><br><em><strong>Constraint:
</strong> Use try-except to handle errors and close the connection properly in all cases.</em>'''

import pymysql

def delete_playlist(playlist_id):
    try:
        # Connect to MySQL
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="music_stream"
        )

        cursor = db.cursor()

        # Delete playlist by id
        query = "DELETE FROM playlists WHERE id = %s"
        cursor.execute(query, (playlist_id,))

        if cursor.rowcount > 0:
            db.commit()
            print("Playlist deleted successfully!")
        else:
            print("Playlist ID not found.")

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        db.close()
        print("Database connection closed.")

# Example
delete_playlist(2)