import asyncio
import config

async def auto_delete(txt=None, m=None):
    try:
        if config.AUTO_DELETE is not False:

            if txt and m or not None:
            # Waiting for the time to pass.
                await asyncio.sleep(300)
                if m is not None:
                    await m.delete(300)
                if txt is not None:
                    await txt.delete(300)

    except Exception as e:
        print(e)
