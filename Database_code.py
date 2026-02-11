import sqlite3
from models import ObservationDTO


class DatabaseManager:

    def __init__(self, db_name="astrodata.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self._create_table()

    def _create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS astrodata(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            object TEXT NOT NULL,
            date TEXT NOT NULL,
            equipment TEXT,
            note TEXT,
            UNIQUE (object, date, equipment, note))''')
        self.conn.commit()

    def add_observation(self, obs_data):
        try:
            self.conn.execute(
                "INSERT INTO astrodata (object, date, equipment, note) VALUES (?, ?, ?, ?)",
                obs_data
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_observations(self):
        cursor = self.conn.execute("SELECT * FROM astrodata")
        return [
            ObservationDTO(id=row[0], object=row[1], date=row[2], equipment=row[3], note=row[4]) 
            for row in cursor.fetchall()
        ]

    def delete_observation(self, obs_id):
        self.conn.execute("DELETE FROM astrodata WHERE id = ?", (obs_id,))
        self.conn.commit()
        
    def search_observations(self, term):
        cursor = self.conn.execute(
            "SELECT * FROM astrodata WHERE object LIKE ? OR date LIKE ?", 
            (f'%{term}%', f'%{term}%')
        )
        return [
            ObservationDTO(id=row[0], object=row[1], date=row[2], equipment=row[3], note=row[4]) 
                for row in cursor.fetchall()
        ]
    
    def __del__(self):
        self.conn.close()