import sqlite3
import uuid

# Connect to SQLite
connection = sqlite3.connect("storage.db")
cursor = connection.cursor()

def create_table():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS filemeta (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            signature TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    connection.commit()


def post_filemeta(name: str, file_type: str, signature: str):
    file_id = str(uuid.uuid4())
    cursor.execute(
        """
        INSERT INTO filemeta (id, name, type, signature)
        VALUES (?, ?, ?, ?)
        """,
        (file_id, name, file_type, signature)
    )
    connection.commit()
    return file_id


def get_all_filemeta():
    cursor.execute("SELECT * FROM filemeta")
    return cursor.fetchall()


def get_filemeta_by_id(file_id: str):
    cursor.execute("SELECT * FROM filemeta WHERE id = ?", (file_id,))
    return cursor.fetchone()


def delete_filemeta(file_id: str):
    cursor.execute("DELETE FROM filemeta WHERE id = ?", (file_id,))
    connection.commit()
    return cursor.rowcount


# Run this only when executed directly
if __name__ == "__main__":
    create_table()
