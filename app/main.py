from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import string, random

from database import init_db, insert_url, get_url_by_code
from cache import get_from_cache, set_to_cache

app = FastAPI()
init_db()

class URLRequest(BaseModel):
    original_url: str

from fastapi.responses import HTMLResponse

from fastapi import Request, Form
from fastapi.responses import HTMLResponse
import string, random

@app.get("/", response_class=HTMLResponse)
def form_page():
    return """
    <html>
        <head>
            <title>Сокращатель ссылок</title>
        </head>
        <body style="font-family:sans-serif; text-align:center; margin-top:5em">
            <h1>Введите ссылку</h1>
            <form action="/shorten-html/" method="post">
                <input type="text" name="original_url" size="50" placeholder="https://example.com" required>
                <br><br>
                <input type="submit" value="Сократить">
            </form>
        </body>
    </html>
    """

@app.post("/shorten-html/", response_class=HTMLResponse)
def handle_form(original_url: str = Form(...)):
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    insert_url(code, original_url)
    short = f"http://localhost:8000/{code}"
    return f"""
    <html>
        <head><title>Сокращено ✅</title></head>
        <body style="font-family:sans-serif; text-align:center; margin-top:5em">
            <h1>Готово!</h1>
            <p>Сокращённая ссылка: <a href="{short}">{short}</a></p>
            <p><a href="/">Назад</a></p>
        </body>
    </html>
    """

@app.post("/shorten/")
def create_short_url(data: URLRequest):
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    insert_url(code, data.original_url)
    return {"short_url": f"http://localhost:8000/{code}"}

from fastapi.responses import RedirectResponse

@app.get("/{code}")
def redirect(code: str):
    cached = get_from_cache(code)
    if cached:
        return RedirectResponse(url=cached)

    url = get_url_by_code(code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    set_to_cache(code, url)
    return RedirectResponse(url=url)

