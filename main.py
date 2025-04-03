"""Main python file"""

if __name__ == "__main__":
    import uvicorn
    from src.conf.config import config

    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=config.debug)
