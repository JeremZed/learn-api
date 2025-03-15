import asyncio
from client import Client

async def main():
    async with Client(options={
        'host': '127.0.0.1',
        'port': '8000',
        'protocol': 'http',
        'headers': {"Content-Type": "application/json"},
    }) as client:
        response = await client.login("j.thulliez@gmail.com", "password")
        print(response)


asyncio.run(main())