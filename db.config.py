import psycopg2 as pg

conn = pg.connect(
    'dbname=example password=12345'
)

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS todos;")
cursor.execute("""
  CREATE TABLE todos (
    id serial PRIMARY KEY,
    description VARCHAR NOT NULL
  );
""")

while True:
    task = input("Send the task you want to insert or Q to quit.\n")
    if task == "Q":
        break
    cursor.execute("INSERT INTO todos (description) values ('{0}')".format(task))

cursor.execute("SELECT * FROM todos;")

print("You have the following takss:")
for data in cursor.fetchall():
    print("|", end=" ")
    for chunk in data:
        print(str(chunk) + " |", end=" ")
    print("\n-------------------------\n")

conn.commit()

cursor.close()
conn.close()
