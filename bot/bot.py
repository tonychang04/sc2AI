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
        await self.build_pylon()
        # Populate this function with whatever your bot should do!
        pass

    # build workers whenever base are idle and each base has less than 22 workers
    async def build_worker(self):
        nexus = self.townhalls.ready.random
        if (
            self.can_afford(UnitTypeId.PROBE)
            and nexus.is_idle
            and self.workers.amount < self.townhalls.amount * 22
        ):
            nexus.train(UnitTypeId.PROBE)

    # build pylon facing the enemy and near nexus
    async def build_pylon(self):
        nexus = self.townhalls.ready.random
        pos = nexus.position.towards(self.enemy_start_locations[0], 10)
        if (
            self.supply_left < 3
            and self.already_pending(UnitTypeId.PYLON) == 0
            and self.can_afford(UnitTypeId.PYLON)
        ):
            await self.build(UnitTypeId.PYLON, near = pos)

    async def build_gateways(self):
        if (
           self.structures()
        ):
            pass

    def on_end(self, result):
        print("Game ended.")
        # Do things here after the game ends
