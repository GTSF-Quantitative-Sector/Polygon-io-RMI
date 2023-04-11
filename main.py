import rmi
import asyncio

async def main():
    client = rmi.Client("_4BtZn3PRCLu6fsdu7dgddb4ucmB1sfp")
    print(await client.get_rmi("AAPL", "2022-01-01"))
    print(await client.get_rsi("AAPL", "2013-01-01"))

if __name__ == "__main__":
    asyncio.run(main())
