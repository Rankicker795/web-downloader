import asyncio
from pathlib import Path
from urllib.parse import urlparse

import httpx
import parsel
from rich import print

url = "https://nssrgeo.ndc.nasa.gov/satellite/goes19/glm/l3/latest_geojson/"

with httpx.Client() as client:
    r = client.get(url)

response_text = r.text

selector = parsel.Selector(text=response_text)

files_to_download = selector.xpath("//a[contains(@href, 'gz')]/text()").getall()

download_list = [f"{url}{fl}" for fl in files_to_download]


async def download_file_async(client, fileurl):
    """Async downloads for a single file"""
    filename = urlparse(fileurl).path.split("/")[-1]
    local_path = Path(__file__).parent.resolve()
    fqfn = local_path / filename

    try:
        response = await client.get(fileurl, follow_redirects=True)
        response.raise_for_status()
        with open(fqfn, "wb") as f:
            f.write(response.content)
        return f"✅ Downloaded {fqfn}"
    except httpx.RequestError as e:
        return f"❌ Failed to download {fileurl}: {e}"


async def main(file_list):
    print("--- Starting Concurrent (Async) Download ---")
    async with httpx.AsyncClient() as client:
        tasks = [download_file_async(client, url) for url in file_list]
        results = await asyncio.gather(*tasks)

    for result in results:
        print(result)
    print("\n--- All downloads complete ---")


asyncio.run(main(download_list))
