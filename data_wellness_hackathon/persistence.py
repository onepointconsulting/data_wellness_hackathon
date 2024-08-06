import sys
import asyncio
from typing import Callable, Any, List, Tuple

from psycopg import AsyncConnection, AsyncCursor

from data_wellness_hackathon.config import cfg
from data_wellness_hackathon.log_init import logger

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def create_connection() -> AsyncConnection:
    return await AsyncConnection.connect(conninfo=cfg.neon_connection)


async def create_cursor(func: Callable, commit=False) -> Any:
    # await asynch_pool.check()
    try:
        conn = await create_connection()
        # async with asynch_pool.connection() as conn:
        async with conn.cursor() as cur:
            return await func(cur)
    except:
        logger.exception("Could not create cursor.")
        return None
    finally:
        if "conn" in locals() and conn is not None:
            if commit:
                await conn.commit()
            await conn.close()


async def handle_select_func(query: str, query_params: dict):
    async def func(cur: AsyncCursor):
        await cur.execute(
            query,
            query_params,
        )
        return list(await cur.fetchall())

    return func


async def select_from(query: str, parameter_map: dict) -> list:
    handle_select = await handle_select_func(query, parameter_map)
    return await create_cursor(handle_select)


async def list_tables() -> List[Tuple[str, str]]:
    res = await select_from(
        """
SELECT table_schema, table_name FROM information_schema.tables WHERE  table_type = 'BASE TABLE' ORDER BY table_name
""",
        {},
    )
    if res is None:
        return []
    else:
        return [(r[0], r[1]) for r in res]
    


async def list_properties(schema: str, table: str) -> List[Any]:
    res = await select_from(
        """
SELECT *
  FROM information_schema.columns
 WHERE table_schema = %(schema)s
   AND table_name   = %(table)s
""",
        {"schema": schema, "table": table},
    )
    if res is None:
        return []
    else:
        return res


async def insert_embeddings(
    title: str, text: str, embedding: List[int],
) -> int:
    async def process_save_embedding(cur: AsyncCursor):
        await cur.execute(
            """
INSERT INTO public.document_embeddings(ID, embedding)
VALUES((SELECT COUNT(*) + 1 from public.document_embeddings), %(embedding)s)
RETURNING ID
            """,
            {
                "embedding": embedding,
            },
        )
        created_row = await cur.fetchone()
        created_id = created_row[0]
        
        await cur.execute(
            """
INSERT INTO public.documents(ID, title, content)
VALUES(%(id)s, %(title)s, %(content)s)
RETURNING ID
            """,
            {
                "id": created_id,
                "title": title,
                "content": text
            },
        )
        created_row = await cur.fetchone()
        created_id = created_row[0]
        return created_id

    return await create_cursor(process_save_embedding, True)

if __name__ == "__main__":
    tables = asyncio.run(list_tables())
    for t in tables:
        print(t)

    print(" --------------------------- ")

    def list_fields(table: str):
        print(table)
        print("_" * len(table))
        fields = asyncio.run(list_properties("public", table))
        for f in fields:
            print(f)

    list_fields("document_embeddings")
    list_fields("documents")
