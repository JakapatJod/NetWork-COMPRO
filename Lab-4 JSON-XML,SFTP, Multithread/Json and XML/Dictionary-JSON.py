import json

books = {'A':'Book1','B':'Book2','C':'Book3'}
type(books)

books['A']
books['B']
books['C']

json.dumps(books)
books_json = json.dumps(books)
print(books_json)
json.loads(books_json)