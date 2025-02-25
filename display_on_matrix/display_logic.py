import asyncio

import asyncio

async def display_task(self, event, gen_gifs):
    print("Running event: " + str(event))

    if event["mode"].strip().lower()=="static":
        self.animation_task = asyncio.create_task(self.static_text(event.get("args",{}),ticker=False))

    elif event["mode"].strip().lower()=="text":
        self.animation_task = asyncio.create_task(self.flow_text(event.get("args",{}),ticker=False))

    elif event["mode"].strip().lower()=="ticker":
        self.animation_task = asyncio.create_task(self.flow_text(event.get("args",{}),ticker=True))

    elif event["mode"].strip().lower()=="image":
        self.animation_task = asyncio.create_task(self.display_image(event.get("args",{})))

    elif event["mode"].strip().lower()=="gif":
        if gen_gifs:
            if "chaos" in event["systems"].strip().lower():
                self.animation_task = asyncio.create_task(self.display_gif(event.get("args",{})))
            else:
                self.animation_task = asyncio.create_task(self.display_generated_gif(event.get("args",{}), event))
        else:
            self.animation_task = asyncio.create_task(self.display_gif(event.get("args",{})))


    if self.animation_task != None:
        if self.flag_infinity:
            self.animation_task.cancel()
            self.flag_infinity = False
        else:
            result = await self.animation_task
    #if selfs.animation_task != None and self.flag_infinity:

    self.queue.task_done()
        
    self.event_args=None
