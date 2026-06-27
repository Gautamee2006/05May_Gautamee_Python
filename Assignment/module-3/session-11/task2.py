'''Create a new MySQL database called music_stream and a table called playlists with columns: 
id (INT, primary key, auto-increment), name (VARCHAR), and song_count (INT). Write a Python 
script using pymysql to insert three sample playlists into this table.'''

import pymysql

try:
    # MySQL se connect
    connection = pymysql.connect(
        host="localhost",
        user="root",        
        password=""   
    )

    cursor = connection.cursor()

    # Database create
    cursor.execute("CREATE DATABASE music_stream")
    print("Database created successfully.")

    # Database select
    cursor.execute("USE music_stream")

    # Table create
    cursor.execute("""
        CREATE TABLE playlists (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            song_count INT
        )
    """)
    print("Table created successfully.")

    # Sample data
    sql = "INSERT INTO playlists (name, song_count) VALUES (%s, %s)"

    data = [
        ("Top Hits", 25),
        ("Workout Mix", 40),
        ("Chill Vibes", 18)
    ]

    # Data insert
    cursor.executemany(sql, data)

    # Save changes
    connection.commit()

    print("3 playlists inserted successfully.")

    cursor.close()
    connection.close()

except pymysql.MySQLError as e:
    print("Error:", e)