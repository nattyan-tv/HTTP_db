import HTTP_db

database = HTTP_db.HTTP_db("0.0.0.0", 45352, "file.db")
database.run()
print("If database finished, you can see this message!")
