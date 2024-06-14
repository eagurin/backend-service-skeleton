import asyncio

class TwoPhaseCommitCoordinator:
    def __init__(self):
        self.participants = []

    def add_participant(self, participant):
        self.participants.append(participant)

    async def prepare(self):
        prepare_tasks = [participant.prepare() for participant in self.participants]
        results = await asyncio.gather(*prepare_tasks, return_exceptions=True)
        return all(result is True for result in results)

    async def commit(self):
        commit_tasks = [participant.commit() for participant in self.participants]
        await asyncio.gather(*commit_tasks)

    async def rollback(self):
        rollback_tasks = [participant.rollback() for participant in self.participants]
        await asyncio.gather(*rollback_tasks)

    async def execute(self):
        try:
            if await self.prepare():
                await self.commit()
                return True
            else:
                await self.rollback()
                return False
        except Exception:
            await self.rollback()
            return False