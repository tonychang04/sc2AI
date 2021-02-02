import sc2

from sc2 import BotAI, Race, UnitTypeId, AbilityId
from sc2 import sc2.units

from sc2.units import UnitSelection
from sc2.unit import Unit
from sc2.position import Point2
from sc2.units import Units
from sc2.player import Bot,Computer



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
    def __init__(self):
        sc2.BotAI.__init__(self)

    async def on_start(self):
        print("Game started")
        # Do things here before the game starts

    async def on_step(self, iteration):
        await self.distribute_workers()
        await self.build_worker()
        await self.build_pylon()
        await self.build_gateways()
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

    # build gateway next to a random pylon
    async def build_gateways(self):
        if (
            self.structures(UnitTypeId.PYLON).ready()
            and self.can_afford(UnitTypeId.GATEWAY)
            and not self.structures(UnitTypeId.GATEWAY)
        ):
            pylon = self.structures(UnitTypeId.PYLON).ready.random
            await self.build(UnitTypeId.GATEWAY,near = pylon)


    # build gas
    async def build_gas(self):
        if self.structures(UnitTypeId.GATEWAY):
            for nexus in self.townhalls.ready:
                vgs =

        pass

    def on_end(self, result):
        print("Game ended.")
        # Do things here after the game ends
