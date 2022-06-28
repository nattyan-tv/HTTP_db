import HTTP_db
import asyncio

client = HTTP_db.Client("http://localhost:8080")

async def get_all_data_and_print():
    data = await client.get_all()
    print(data)

if __name__ == "__main__":
    asyncio.run(get_all_data_and_print())
