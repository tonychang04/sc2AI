from sc2 import BotAI, Race, UnitTypeId


class CompetitiveBot(BotAI):
    NAME: str = "CompetitiveBot"
    """This bot's name"""
    RACE: Race = Race.Protoss
    """This bot's Starcraft 2 race.
    Options are:
        Race.Terran
        Race.Zerg
        Race.Protoss
        Race.Random
    """

    async def on_start(self):
        print("Game started")
        # Do things here before the game starts

    async def on_step(self, iteration):
        await self.distribute_workers()
        await self.build_worker()
        # Populate this function with whatever your bot should do!

        pass
    async def build_worker(self):
        nexus = self.townhalls.ready.random
        if (
            self.can_afford(UnitTypeId.PROBE)
            and nexus.is_idle
            and self.workers.amount < self.townhalls.amount * 22
        ):
            nexus.train(UnitTypeId.PROBE)

    def on_end(self, result):
        print("Game ended.")
        # Do things here after the game ends
