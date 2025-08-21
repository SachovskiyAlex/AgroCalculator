import mysql.connector
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1111",  
    "database": "agro_calc"
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def додати_поле(name, area):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fields (name, area) VALUES (%s, %s)", (name, area))
    conn.commit()
    cursor.close()
    conn.close()


def додати_препарат(name, rate_min, rate_max):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chemicals (name, rate_min, rate_max) VALUES (%s, %s, %s)", (name, rate_min, rate_max))
    conn.commit()
    cursor.close()
    conn.close()



def отримати_поля():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, area FROM fields")
    результат = cursor.fetchall()
    cursor.close()
    conn.close()
    return результат


def отримати_препарати():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, rate_min, rate_max FROM chemicals")
    результат = cursor.fetchall()
    cursor.close()
    conn.close()
    return результат

def отримати_форсунки():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            parameters.id,
            nozles.nozlesName,
            parameters.pressure,
            parameters.speed,
            parameters.flow_rate
        FROM parameters
        JOIN nozles ON parameters.nozlesID = nozles.nozlesID
    """)
    результат = cursor.fetchall()
    cursor.close()
    conn.close()
    return результат

def підключитись():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111",
        database="agro_calc"
    )


def видалити_поле(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fields WHERE name = %s", (name,))
    conn.commit()
    cursor.close()
    conn.close()

def видалити_препарат(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chemicals WHERE name = %s", (name,))
    conn.commit()
    cursor.close()
    conn.close()


def зберегти_в_історію(field_name, area, pesticide_name, rate, nozzle_type, pressure,
                       speed, water_flow, total_pesticide, total_water):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO history (
            field_name, area, pesticide_name, rate, nozzle_type,
            pressure, speed, water_flow, total_pesticide, total_water
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (field_name, area, pesticide_name, rate, nozzle_type, pressure,
          speed, water_flow, total_pesticide, total_water))
    conn.commit()
    cursor.close()
    conn.close()


def отримати_історію():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, field_name, area, pesticide_name, rate, nozzle_type, pressure, speed, water_flow, total_pesticide, total_water, created_at FROM history")
    результат = cursor.fetchall()
    cursor.close()
    conn.close()
    return результат

def видалити_з_історії(record_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history WHERE id = %s", (record_id,))
    conn.commit()
    cursor.close()
    conn.close()
