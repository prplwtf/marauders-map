from fastapi import FastAPI

app = FastAPI()


class Probe:
    ip: str
    code: int
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/report")
async def report():


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

if __name__ == "__main__":
    main()
