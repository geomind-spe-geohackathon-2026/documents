"""Import a memory seed additively: entries whose id is not in memory_entries are added."""
import asyncio
import json
import sys

from src.core.clients.postgres import models  # noqa: F401
from src.core.clients.postgres.client import create_postgres_client
from src.core.clients.postgres.repositories.memory import MemoryRepository


async def main(path: str) -> None:
    seed = json.load(open(path))
    section = seed["kind"]
    engine, factory = create_postgres_client()
    added, kept = [], []
    async with factory() as session:
        repository = MemoryRepository(session)
        for entry in seed["entries"]:
            if await repository.get(section, str(entry["id"]), None) is not None:
                kept.append(entry["id"])
                continue
            await repository.put(section, entry, None, ("seed", "documents/project/memory-seed"))
            added.append(entry["id"])
    print(json.dumps({"section": section, "added": added, "already_there": kept}))


asyncio.run(main(sys.argv[1]))
