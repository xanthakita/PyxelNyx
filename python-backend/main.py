import sys
import argparse
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(title="PyxelNyx Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "PyxelNyx backend is running"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()

    print(f"Starting PyxelNyx Backend on port {args.port}", flush=True)
    sys.stdout.flush()

    uvicorn.run(app, host="127.0.0.1", port=args.port, log_level="info")
