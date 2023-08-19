import os
import json
import asyncio
import aiohttp
from tqdm import tqdm

json_file = "links.json"
output_directory = "downloaded_files"
concurrent_downloads = 5

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

async def download_file(session, file_name, link):
    save_path = os.path.join(output_directory, file_name + ".mp4")

    async with session.get(link) as response:
        file_size = int(response.headers.get("content-length", 0))

        progress_bar = tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=1024, desc=file_name, ncols=100, colour='green')

        with open(save_path, "wb") as output_file:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                progress_bar.update(len(chunk))
                output_file.write(chunk)

        progress_bar.close()

async def main():
    with open(json_file, "r") as f:
        json_data = json.load(f)

    async with aiohttp.ClientSession() as session:
        tasks = []

        for file_name, link in json_data.items():
            task = download_file(session, file_name, link)
            tasks.append(task)

            if len(tasks) == concurrent_downloads:
                await asyncio.gather(*tasks)
                tasks = []

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("Download completed. Files are saved in the directory:", output_directory)

    print("Pobieranie zakończone. Pliki dostępne w katalogu:", output_directory)
