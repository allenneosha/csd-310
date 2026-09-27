import mysql.connector

def display_all_tables():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bacchus_winery"
        )
        cursor = conn.cursor()

        cursor.execute("SHOW TABLES;")
        tables = [table[0] for table in cursor.fetchall()]

        print("=" * 60)
        print("         BACCHUS WINERY DATABASE DISPLAY SCRIPT")
        print("=" * 60)

        for table in tables:
            print(f"\n--- TABLE: {table.upper()} ---")
            cursor.execute(f"SELECT * FROM {table};")
            rows = cursor.fetchall()
            
            cursor.execute(f"DESCRIBE {table};")
            headers = [column[0] for column in cursor.fetchall()]
            
            print(" | ".join(headers))
            print("-" * 50)
            
            if rows:
                for row in rows:
                    print(" | ".join(str(item) for item in row))
            else:
                print("(No records found)")

        cursor.close()
        conn.close()
        print("\n" + "=" * 60)
        print("[+] All database tables retrieved successfully!")
        print("=" * 60)

    except mysql.connector.Error as err:
        print(f"Error connecting to local MariaDB: {err}")

if __name__ == "__main__":
    display_all_tables()
