import grpc

class GrpcClient:
    def __init__(self, target):
        self.target = target
        self.channel = None

    async def __aenter__(self):
        self.channel = await grpc.aio.insecure_channel(self.target)
        await self.channel.channel_ready()  
        return self.channel

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.channel.close() 