from disp import dp, on_startup
from shed import scheduler
import warnings
import asyncio

warnings.filterwarnings("ignore")


async def main():
    await asyncio.gather(
        on_startup(dp),
        scheduler(),
    )

if __name__ == '__main__':
    asyncio.run(main())
