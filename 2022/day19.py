import dataclasses
from typing import Dict, Set
import tqdm

Resources = Dict[str, int]
Robots = Dict[str, int]


@dataclasses.dataclass
class Blueprint:
    id: int
    ore: Resources
    clay: Resources
    obsidian: Resources
    geode: Resources


def create_resources(ore=0, clay=0, obsidian=0, geode=0) -> Resources:
    return {
        "ore": ore,
        "clay": clay,
        "obsidian": obsidian,
        "geode": geode
    }


blueprints = []
with open("input.txt") as f:
    for line in f:
        line = line.strip()
        line = line[len("Blueprint "):]
        id = line[:line.index(":")]
        id = int(id)
        line = line[line.index("costs ") + len("costs "):]
        ore = line[:line.index(" ")]
        line = line[line.index("costs ") + len("costs "):]
        clay = line[:line.index(" ")]
        line = line[line.index("costs ") + len("costs "):]
        obsidian_ore = line[:line.index(" ")]
        line = line[line.index("and ") + len("and "):]
        obsidian_clay = line[:line.index(" ")]
        line = line[line.index("costs ") + len("costs "):]
        geode_ore = line[:line.index(" ")]
        line = line[line.index("and ") + len("and "):]
        geode_obsidian = line[:line.index(" ")]

        blueprints.append(Blueprint(
            id=id,
            ore=create_resources(ore=int(ore)),
            clay=create_resources(ore=int(clay)),
            obsidian=create_resources(ore=int(obsidian_ore), clay=int(obsidian_clay)),
            geode=create_resources(ore=int(geode_ore), obsidian=int(geode_obsidian))
        ))


def deduct_resources(source: Resources, requirements: Resources):
    for (resource, requirement) in requirements.items():
        source[resource] -= requirement


def has_enough_resources(source: Resources, requirements: Resources) -> bool:
    for (resource, requirement) in requirements.items():
        if source[resource] < requirement:
            return False
    return True


@dataclasses.dataclass
class State:
    robots: Resources
    resources: Resources

    @staticmethod
    def new() -> "State":
        return State(
            robots=create_resources(ore=1),
            resources=create_resources()
        )

    def copy(self) -> "State":
        return State(
            robots=dict(self.robots),
            resources=dict(self.resources)
        )

    def build(self, blueprint: Blueprint, robot: str):
        requirements = getattr(blueprint, robot)
        deduct_resources(self.resources, requirements)


@dataclasses.dataclass
class Result:
    quality_level: int = 0
    iters: int = 0


NUMBER_OF_STEPS = 32


def needs_resource(resource: str, state: State, needed: int, step: int):
    remaining_steps = NUMBER_OF_STEPS - step
    to_generate = remaining_steps * state.robots[resource]
    current_resource = state.resources[resource]
    total_res = to_generate + current_resource
    max_needed = needed * (remaining_steps - 1)
    return total_res < max_needed


def generate_build_plans(blueprint: Blueprint, state: State, step: int):
    needs_obsidian = state.robots["obsidian"] < blueprint.geode["obsidian"]
    needs_clay = state.robots["clay"] < blueprint.obsidian["clay"]
    needs_ore = state.robots["ore"] < max(blueprint.obsidian["ore"], blueprint.geode["ore"],
                                          blueprint.clay["ore"])

    built = []
    if has_enough_resources(state.resources, blueprint.geode):
        yield ["geode"]
        built.append("geode")
    if needs_obsidian and has_enough_resources(state.resources, blueprint.obsidian):
        yield ["obsidian"]
        built.append("obsidian")
    if needs_clay and has_enough_resources(state.resources, blueprint.clay):
        yield ["clay"]
        built.append("clay")
    if needs_ore and has_enough_resources(state.resources, blueprint.ore):
        yield ["ore"]
        built.append("ore")
    if "geode" not in built:  # and len(built) < 4:
        yield []


def resources_key(resources: Resources):
    return (
        resources["ore"],
        resources["clay"],
        resources["obsidian"],
        resources["geode"],
    )


def upper_bound_ql(state: State, step: int) -> int:
    remaining_steps = NUMBER_OF_STEPS - step
    current = state.resources["geode"]
    to_mine = remaining_steps * state.robots["geode"]
    to_mine += (remaining_steps * (remaining_steps - 1)) / 2
    return current + to_mine


def simulate_step(blueprint: Blueprint, state: State, step: int, result: Result, cache: Set):
    key = (resources_key(state.resources), resources_key(state.robots), step)
    if key in cache:
        return
    if result.quality_level > 0 and upper_bound_ql(state, step) <= result.quality_level:
        return

    if step >= NUMBER_OF_STEPS:
        quality_level = state.resources["geode"]
        if quality_level > result.quality_level:
            result.quality_level = quality_level
            print(quality_level)
        cache.add(key)
        return

    build_plans = generate_build_plans(blueprint, state, step)
    for build_plan in build_plans:
        new_state = state.copy()

        for robot in build_plan:
            new_state.build(blueprint, robot)
            new_state.robots[robot] += 1

        # Mine resources with old robots
        for (res, count) in state.robots.items():
            new_state.resources[res] += count

        simulate_step(blueprint, new_state, step + 1, result, cache)
    cache.add(key)


def simulate(blueprint: Blueprint) -> int:
    result = Result()
    cache = set()
    simulate_step(blueprint, State.new(), 0, result, cache)
    return result.quality_level


total = 1
for blueprint in tqdm.tqdm(blueprints[1:2]):
    quality_level = simulate(blueprint)
    print(f"ID: {blueprint.id}, QL: {quality_level}")
    total *= quality_level
print(total)

# 58, ???, 23

# 58 * 5 * 23, 6670, too low
# 58 * 7 * 23, 9338, too low
# 58 * 8 * 23, 10672, too low
# 58 * 9 * 23, 12006, too low
