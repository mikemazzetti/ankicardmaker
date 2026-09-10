---
deck: "Resume Prep::FastAPI"
topic: "FastAPI"
tags: [ankicardmaker, resume-prep, fastapi]
note_type: Mixed (Basic / Basic (and reversed card) / Cloze)
created: 2026-09-09
---

# FastAPI — Resume Prep

Source of truth for the `Resume Prep::FastAPI` deck (18 notes). Edit here and re-push to update.

## Basic cards

1. **Q:** How do you code a FastAPI path parameter with a type hint?
   **A:** <pre><code>from fastapi import FastAPI
app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}</code></pre>

2. **Q:** In FastAPI, how does a function parameter become a query parameter vs a path parameter?
   **A:** If the parameter name matches a <code>{name}</code> placeholder in the route path, it's a path parameter; any other function parameter with a simple type (not a Pydantic model) is automatically treated as a query parameter.

3. **Q:** How do you code an optional query parameter with a default value in FastAPI?
   **A:** <pre><code>@app.get("/items")
def list_items(q: str | None = None, limit: int = 10):
    return {"q": q, "limit": limit}</code></pre>

4. **Q:** What is a Pydantic model used for in FastAPI request bodies?
   **A:** A class subclassing <code>BaseModel</code> that declares field names and types for the JSON request body; FastAPI parses, type-converts, and validates incoming JSON against it automatically, returning a 422 error on mismatch.

5. **Q:** How do you code a FastAPI POST endpoint that accepts a JSON body validated by a Pydantic model?
   **A:** <pre><code>from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
def create_item(item: Item):
    return item</code></pre>

6. **Q:** What does FastAPI's dependency injection system (<code>Depends</code>) let you do?
   **A:** It lets you declare reusable pieces of logic (e.g. get a DB session, verify auth) as functions, and have FastAPI automatically call them and inject their return value into any route that needs it.

7. **Q:** How do you code a FastAPI dependency that provides a DB session and use it in a route?
   **A:** <pre><code>def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()</code></pre>

8. **Q:** Why does a FastAPI dependency using <code>yield</code> support setup/teardown logic?
   **A:** Code before the <code>yield</code> runs before the request is handled (setup, e.g. opening a DB session); code after the <code>yield</code> runs after the response is sent (teardown, e.g. closing the session), even if an exception occurred.

9. **Q:** How do you code an async FastAPI endpoint that awaits an external HTTP call?
   **A:** <pre><code>import httpx

@app.get("/proxy")
async def proxy():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.example.com")
    return resp.json()</code></pre>

10. **Q:** When should a FastAPI route be declared <code>async def</code> vs plain <code>def</code>?
   **A:** Use <code>async def</code> when the handler awaits non-blocking async I/O (e.g. an async DB driver or HTTP client); use plain <code>def</code> for blocking/sync code — FastAPI automatically runs sync <code>def</code> routes in a thread pool so they don't block the event loop.

11. **Q:** How does FastAPI generate interactive OpenAPI docs (Swagger UI, ReDoc) automatically?
   **A:** It builds an OpenAPI schema from your route declarations, type hints, and Pydantic models at startup, then serves interactive docs (Swagger UI at <code>/docs</code>, ReDoc at <code>/redoc</code>) from that schema with no extra configuration needed.

12. **Q:** What is a FastAPI <code>response_model</code> used for?
   **A:** It declares the Pydantic model FastAPI should validate and filter the returned data against before serializing the response, ensuring extra or internal fields (like a hashed password) aren't accidentally exposed.

13. **Q:** How do you code a FastAPI route that returns a specific status code and raises a 404 when not found?
   **A:** <pre><code>from fastapi import HTTPException, status

@app.get("/items/{item_id}", status_code=status.HTTP_200_OK)
def get_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]</code></pre>

14. **Q:** What does adding a <code>@validator</code> (Pydantic v1) or <code>field_validator</code> (Pydantic v2) to a model field let you do?
   **A:** Define custom validation logic beyond basic type checking, e.g. rejecting a negative price or normalizing a string, that runs automatically when FastAPI parses the request body into that model.

15. **Q:** What's the difference between a FastAPI path parameter declared as <code>item_id: int</code> versus <code>item_id: str</code>?
   **A:** With <code>int</code>, FastAPI automatically converts and validates the URL segment as an integer, returning a 422 if it isn't numeric; with <code>str</code> any raw segment is accepted as-is with no conversion.

16. **Q:** How do you organize a larger FastAPI app's routes into separate files/modules?
   **A:** Use <code>APIRouter</code> in each module to define a group of related routes, then include it in the main app with <code>app.include_router(router, prefix="/users")</code>.

17. **Q:** How do you code registering an APIRouter with a prefix and tag in FastAPI?
   **A:** <pre><code># users.py
router = APIRouter()

@router.get("/")
def list_users():
    return []

# main.py
app.include_router(users.router, prefix="/users", tags=["users"])</code></pre>

## Cloze cards

- In FastAPI, a Pydantic field validation failure on the request body returns HTTP status {{c1::422}} (Unprocessable Entity) with a JSON body describing which fields failed.
