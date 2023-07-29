import json # ต้องระบุ path cd Lab-4

with open("books.json","rt") as file:
    books = json.load(file)

print(books)

print(type(books))