import os
import sqlite3

db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

if os.path.exists(db_path):
    print(f"Conectando a {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Clean tables
    cursor.execute("DELETE FROM feria_boletodigital;")
    cursor.execute("DELETE FROM feria_solicitudboleto;")
    cursor.execute("DELETE FROM feria_boletofisico;")
    cursor.execute("DELETE FROM feria_aporte;")
    
    # Reset auto-increment ID counters in SQLite
    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('feria_solicitudboleto', 'feria_boletodigital', 'feria_boletofisico', 'feria_aporte');")
    
    conn.commit()
    conn.close()
    print("✅ Base de datos limpiada y secuencias de ID reiniciadas a 1.")
else:
    print("❌ No se encontró db.sqlite3")
