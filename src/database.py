import os
import sqlite3
from pathlib import Path

DATABASE_PATH = os.path.join(str(Path(__file__).parents[1]), "music.db")

if os.path.exists(DATABASE_PATH):
    os.remove(DATABASE_PATH)

with sqlite3.connect(DATABASE_PATH, check_same_thread=False) as conn:
    c = conn.cursor()
    c.executescript(
        """
            CREATE TABLE artist (
            artist_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            phone TEXT,
            website TEXT,
            is_group BOOLEAN CHECK (is_group IN (0, 1))
            );
            
            INSERT INTO artist (name, first_name, last_name, phone, website, is_group)
            VALUES ('Lil Uzi Vert', 'Symere', 'Woods', '505-744-6896', 'liluziofficial.com', false);
            INSERT INTO artist (name, first_name, last_name, phone, website, is_group)
            VALUES ('Playboi Carti', 'Jordan', 'Carter', '734-979-8405', 'playboicarti.com', false);
            INSERT INTO artist (name, first_name, last_name, phone, website, is_group)
            VALUES ('Drake', 'Aubrey', 'Graham', '615-541-4518', 'drakerelated.com', false);
            INSERT INTO artist (name, first_name, last_name, phone, website, is_group)
            VALUES ('Michael Jackson', 'Michael', 'Jackson', NULL, 'michaeljackson.com', false);
            INSERT INTO artist (name, first_name, last_name, phone, website, is_group)
            VALUES ('Coldplay', NULL, NULL, '904-305-2449', 'coldplay.com', true);
            INSERT INTO artist (name, first_name, last_name, phone, website, is_group)
            VALUES ('Yeat', 'Noah', 'Smith', '412-542-6931', 'twizzyrich.com', false);
            INSERT INTO artist (name, first_name, last_name, phone, website, is_group)
            VALUES ('Kodak Black', 'Bill', 'Kapri', '631-912-2820', 'officialkodakblack.com', false);
            INSERT INTO artist (name, first_name, last_name, phone, website, is_group)
            VALUES ('The Beatles', NULL, NULL, '402-480-1486', 'thebeatles.com', true);
            
            CREATE TABLE album (
            album_id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (artist_id) REFERENCES artist(artist_id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            
            INSERT INTO album (artist_id, name) VALUES (1, 'The Perfect LUV Tape');
            INSERT INTO album (artist_id, name) VALUES (1, 'Luv Is Rage');
            INSERT INTO album (artist_id, name) VALUES (1, 'Eternal Atake');
            INSERT INTO album (artist_id, name) VALUES (2, 'Die Lit');
            INSERT INTO album (artist_id, name) VALUES (3, 'Take Care');
            INSERT INTO album (artist_id, name) VALUES (4, 'Off the Wall');
            INSERT INTO album (artist_id, name) VALUES (5, 'Viva la Vida or Death and All His Friends');
            INSERT INTO album (artist_id, name) VALUES (6, 'Up 2 Më');
            INSERT INTO album (artist_id, name) VALUES (6, '2 Alivë');
            INSERT INTO album (artist_id, name) VALUES (7, 'Dying to Live');
            INSERT INTO album (artist_id, name) VALUES (8, 'Help!');
            
            CREATE TABLE song (
            song_id INTEGER PRIMARY KEY AUTOINCREMENT,
            album_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            duration REAL,
            UNIQUE(album_id, name) ON CONFLICT ABORT,
            FOREIGN KEY (album_id) REFERENCES album(album_id) ON DELETE CASCADE ON UPDATE CASCADE
            );
            
            INSERT INTO song (album_id, name, duration) VALUES (1, 'Erase Your Social', 3.19);
            INSERT INTO song (album_id, name, duration) VALUES (3, 'Venetia', 3.08);
            INSERT INTO song (album_id, name, duration) VALUES (4, 'Long Time', 3.31);
            INSERT INTO song (album_id, name, duration) VALUES (5, 'Marvins Room', 5.47);
            INSERT INTO song (album_id, name, duration) VALUES (6, 'Rock With You', 3.40);
            INSERT INTO song (album_id, name, duration) VALUES (7, 'Viva La Vida', 4.02);
            INSERT INTO song (album_id, name, duration) VALUES (8, 'Cmon', 1.42);
            INSERT INTO song (album_id, name, duration) VALUES (9, 'Poppin', 2.47);
            INSERT INTO song (album_id, name, duration) VALUES (10, 'From the Cradle', 3.11);
            INSERT INTO song (album_id, name, duration) VALUES (11, 'Hey Jude', 3.58);           
        """
    )
