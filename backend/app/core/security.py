import asyncio

import bcrypt


def _hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _verify(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


# bcrypt при cost 12 — это сотни миллисекунд чистого CPU. В корутине он
# останавливает весь event loop, поэтому обе операции уходят в тред.
async def hash_password(password: str) -> str:
    return await asyncio.to_thread(_hash, password)


async def verify_password(password: str, hashed: str) -> bool:
    return await asyncio.to_thread(_verify, password, hashed)
