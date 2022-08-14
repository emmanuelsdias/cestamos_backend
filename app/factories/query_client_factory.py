from fastapi import Depends
from app.dal.query_client \
    import ABCQueryClient, QueryClient
from app.factories.config import get_settings
from app.utils.settings import Settings


def get_query_client(
    config: Settings = Depends(get_settings)
) -> ABCQueryClient:
    client = QueryClient(config)
    try:
        yield client
    finally:
        pass