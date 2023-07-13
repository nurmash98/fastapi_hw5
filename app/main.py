from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from .repository import BooksRepository

app = FastAPI()

templates = Jinja2Templates(directory="templates")
repository = BooksRepository()


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/books")
def get_books(request: Request, page: int = 1, limit: int = 10):
    start_index = (page - 1) * limit
    end_index = page * limit
    books = repository.get_all()[start_index:end_index]
    amount_books = len(repository.get_all())
    return templates.TemplateResponse(
        "books/index.html",
        {"request": request, 
         "books": books, 
         "pages": (amount_books + limit - 1)//limit, 
         "page": page},
    )
# (сюда писать решение)
@app.get("/books/new")
def get_new_books(request: Request):
    return templates.TemplateResponse("books/new.html", {"request": request})

@app.post("/books")
def append_new_book(
    request: Request,
    title: str = Form(),
    author: str = Form(),
    year: str = Form(),
    total_pages: str = Form(),
    genre: str = Form()    
    ):

    if title == "" or author == "" or year == "" or total_pages == "" or genre == "":
        return Response("Empty Form", 422)
    new_book = {
        "title" : title,
        "author" : author,
        "year" : year, 
        "total_pages" : total_pages,
        "genre" : genre  
    }
    repository.save(new_book)
    return RedirectResponse("/books", status_code = 303)

@app.get("/books/{id}")
def get_book(request: Request, 
             id: int):
    book = repository.get_one(id)
    if book is None:
        return Response("Not Found", 404)
    return templates.TemplateResponse("books/book.html", 
                                      {"request" : request, 
                                       "book": book})

@app.get("/books/{id}/edit")
def get_edit(request: Request, id: int):
    book = repository.get_one(id)
    if book is None:
        return Response("Not Found", 404)
    return templates.TemplateResponse("books/edit.html",
                                        {"request": request, 
                                         "book": book})


@app.post("/books/{id}/edit")
def update_book(id: int, 
                title: str = Form(), 
                author: str = Form(), 
                year: str = Form(), 
                total_pages: str = Form(), 
                genre: str = Form()):
    
    updated_book = {"id": id,
                    "title": title, 
                    "author": author, 
                    "year": year, 
                    "total_pages": total_pages, 
                    "genre": genre}

    isHasBook = repository.update(id, updated_book)
    if not isHasBook:
        return Response("Not Found", 404)
    return RedirectResponse(f"/books/{id}", status_code = 303)


@app.delete("/books/{id}/delete")
def delete_book(id: int):
    isDeleted = repository.delete(id)
    if not isDeleted:
        return Response("NOT FOUND", 404)
    return RedirectResponse("/books", status_code = 303)
# (конец решения)
