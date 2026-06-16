from datetime import datetime


REPUTATION_CACHE = {}


def cache_reputation(

    domain: str,
    reputation: str

):

    REPUTATION_CACHE[domain] = {

        "reputation":
            reputation,

        "timestamp":
            datetime.utcnow().isoformat()
    }

    return True


def get_cached_reputation(

    domain: str

):

    return REPUTATION_CACHE.get(

        domain,

        None
    )


def clear_cache():

    REPUTATION_CACHE.clear()

    return {

        "success": True,

        "message":
            "Cache cleared"
    }


def cache_size():

    return {

        "entries":
            len(REPUTATION_CACHE)
    }