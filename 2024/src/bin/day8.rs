use aoc2024::grid::Grid;
use aoc2024::vector::Position2D;
use hashbrown::{HashMap, HashSet};
use itertools::Itertools;

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let grid = Grid::from_str(&file);
    let mut antennas: HashMap<u8, Vec<Position2D>> = HashMap::new();
    for (item, c) in grid.items() {
        if c != b'.' {
            antennas.entry(c).or_default().push(item);
        }
    }
    let mut antinodes: HashSet<Position2D> = HashSet::new();
    for (antenna, positions) in antennas {
        for (&a, &b) in positions.iter().tuple_combinations() {
            let diff = a - b;
            let mut point = a;
            while grid.contains_pos(point) {
                antinodes.insert(point);
                point = point + diff;
            }

            let diff = b - a;
            let mut point = b;
            while grid.contains_pos(point) {
                antinodes.insert(point);
                point = point + diff;
            }
        }
    }
    let antinodes = antinodes
        .into_iter()
        .filter(|&pos| grid.contains_pos(pos))
        .count();
    println!("{}", antinodes);

    Ok(())
}
