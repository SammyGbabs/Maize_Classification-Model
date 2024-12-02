uvicorn_config = {
    "limit_concurrency": 1,
    "timeout_keep_alive": 0,
    "limit_max_requests": 0,
    "http": {
        "h11_max_incomplete_size": 0,  # No limit
    },
}