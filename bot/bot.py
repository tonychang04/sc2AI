import sc2

from sc2 import BotAI, Race, UnitTypeId, AbilityId
from sc2 import units

from sc2.units import UnitSelection
from sc2.unit import Unit
from sc2.position import Point2
from sc2.units import Units
from sc2.player import Bot, Computer


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
        await self.build_gas()
        await self.build_cyber_core()
        await self.train_stalkers()
        await self.build_four_gates()
        await self.chrono()

        # Populate this function with whatever your bot should do!
        pass

    # build workers whenever base are idle and each base has less than 22 workers
    async def build_worker(self):
        probe_per_nexus = 22
        nexus = self.townhalls.ready.random
        if (
                self.can_afford(UnitTypeId.PROBE)
                and nexus.is_idle
                and self.workers.amount < self.townhalls.amount * probe_per_nexus

        ):
            nexus.train(UnitTypeId.PROBE)

    # build pylon facing the enemy and near nexus
    async def build_pylon(self):
        pylon_from_nexus_dis = 10
        remaining_supply = 3
        nexus = self.townhalls.ready.random
        pos = nexus.position.towards(self.enemy_start_locations[0], pylon_from_nexus_dis)

        if (
                self.supply_left < remaining_supply
                and self.already_pending(UnitTypeId.PYLON) == 0
                and self.can_afford(UnitTypeId.PYLON)
        ):
            await self.build(UnitTypeId.PYLON, near=pos)

    # build gateway next to a random pylon
    async def build_gateways(self):
        if (
                self.structures(UnitTypeId.PYLON).ready()
                and self.can_afford(UnitTypeId.GATEWAY)
                and not self.structures(UnitTypeId.GATEWAY)
        ):
            # if pylon is ready then build gate next to pylon
            pylon = self.structures(UnitTypeId.PYLON).ready.random
            await self.build(UnitTypeId.GATEWAY, near=pylon)

    # build gas
    async def build_gas(self):
        gas_to_nexus = 15
        if self.structures(UnitTypeId.GATEWAY):
            for nexus in self.townhalls.ready:
                vgs = self.vespene_geyser.closer_than(gas_to_nexus, nexus)
                for vg in vgs:
                    if not self.can_afford(UnitTypeId.ASSIMILATOR):
                        break
                    worker = self.select_build_worker(vg.position)
                    if (worker is None):
                        break
                    if not self.gas_buildings or not self.gas_buildings.closer_than(1, vg):
                        worker.build(UnitTypeId.ASSIMILATOR, vg)
                        worker.stop(queue=True)

    async def build_cyber_core(self):
        if (self.structures(UnitTypeId.GATEWAY).ready
                and self.can_afford(UnitTypeId.CYBERNETICSCORE)
                and not self.structures(UnitTypeId.CYBERNETICSCORE)
                and not self.already_pending(UnitTypeId.CYBERNETICSCORE)):
            pylon = self.structures(UnitTypeId.PYLON).ready.random
            await self.build(UnitTypeId.CYBERNETICSCORE, near=pylon)

    async def train_stalkers(self):
        for gateway in self.structures(UnitTypeId.GATEWAY):
            if (self.can_afford(UnitTypeId.STALKER) and gateway.is_idle):
                gateway.train(UnitTypeId.STALKER)

    async def build_four_gates(self):
        if (self.structures(UnitTypeId.PYLON).ready
                and self.can_afford(UnitTypeId.GATEWAY)
                and self.structures(UnitTypeId.GATEWAY).amount < 4):
            pylon = self.structures(UnitTypeId.PYLON).ready.random
            await self.build(UnitTypeId.GATEWAY, near=pylon)

    async def chrono(self):
        if (self.structures(UnitTypeId.PYLON)):
            nexus = self.structures(UnitTypeId.NEXUS).ready.random
            if (not self.structures(UnitTypeId.CYBERNETICSCORE).ready
                    and self.structures(UnitTypeId.PYLON).amount > 0
                    and nexus.energy >= 50):
                nexus(AbilityId.EFFECT_CHRONOBOOST, nexus)


    def on_end(self, result):
        print("Game ended.")
        # Do things here after the game ends
