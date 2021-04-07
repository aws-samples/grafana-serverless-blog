import asyncio
import logging
import os
import random

from aiohttp import ClientConnectorError, ClientSession

API_URL = os.environ["API_URL"]

logger = logging.getLogger()
logger.setLevel(logging.INFO)


async def fetch(url, session):
    try:
        # Set 5% of invocations to error out due to a "bad actor"
        if random.randrange(0, 20) == 0:
            async with session.get(
                url,
                params={"error": "1"},
                headers={"User-Agent": "Malicious Agent 1.0"},
            ) as response:
                if response.status != 200:
                    logger.debug(f"HTTP error {response.status}")
                return await response.read()
        else:
            # benign request from random user agent
            async with session.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
                },
            ) as response:
                if response.status != 200:
                    logger.debug(f"HTTP error {response.status}")
                return await response.read()
    except ClientConnectorError as e:
        logger.error(f"Connection Error: " + str(e))


async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session)


async def run(r):
    tasks = []
    sem = asyncio.Semaphore(1000)  # max concurrent connections

    while True:
        async with ClientSession() as session:
            for _ in range(r):
                task = asyncio.ensure_future(bound_fetch(sem, API_URL, session))
                tasks.append(task)

            responses = asyncio.gather(*tasks)
            await responses


def lambda_handler(event, context):
    logger.info(f"Generating async traffic for {API_URL}...")
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(100_000))  # max requests
    loop.run_until_complete(future)
