'''Modify your script to update the name of a playlist in the playlists table (for example, 
change 'Chill Vibes' to 'Chill Hits') and print a message confirming the update.<br><br><em>
<strong>Hint:</strong> Use the UPDATE SQL statement and commit the changes.</em>'''

import pymysql

# Connect to MySQL
db = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="music_stream"
)

cursor = db.cursor()

# Update playlist name
query = "UPDATE playlists SET name = 'Chill Hits' WHERE name = 'Chill Vibes'"

cursor.execute(query)

# Save changes
db.commit()

print("Playlist name updated successfully!")

# Close connection
cursor.close()
db.close()