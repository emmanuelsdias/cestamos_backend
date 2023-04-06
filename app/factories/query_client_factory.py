from fastapi import Depends
from dal.query_client \
    import ABCQueryClient, QueryClient
from factories.config import get_settings
from utils.settings import Settings


def get_query_client(
    config: Settings = Depends(get_settings)
) -> ABCQueryClient:
    client = QueryClient(config)
    try:
        yield client
    finally:
        pass