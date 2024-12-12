use aoc2024::grid::Grid;
use aoc2024::vector::{Direction2D, Position2D};
use itertools::Itertools;
use std::collections::HashSet;

#[derive(Clone, Debug)]
struct Scanner {
    pos: Position2D,
    direction: Direction2D,
}

impl Scanner {
    fn next_pos(&self) -> Position2D {
        self.pos + self.direction
    }
    fn at_next_pos(&self) -> Self {
        Self {
            pos: self.next_pos(),
            direction: self.direction,
        }
    }
    fn turned_right(&self) -> Self {
        Self {
            pos: self.pos,
            direction: self.direction.turn_right(),
        }
    }
    fn turned_left(&self) -> Self {
        Self {
            pos: self.pos,
            direction: self.direction.turn_left(),
        }
    }

    fn adjacent(&self, region: &HashSet<Position2D>) -> Option<Position2D> {
        let perpendicular = self.direction.turn_right();
        let target_pos = self.pos + perpendicular;
        if region.contains(&target_pos) {
            Some(target_pos)
        } else {
            None
        }
    }
}

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let grid = Grid::from_str(&file);

    let mut visited = HashSet::new();
    let mut regions = vec![];

    for (pos, c) in grid.items() {
        let mut region = vec![];
        fill(&grid, c, pos, &mut region, &mut visited);
        if !region.is_empty() {
            regions.push(region.into_iter().collect::<HashSet<Position2D>>());
        }
    }
    let res = regions
        .into_iter()
        .map(|r| {
            let count = r.len() as u64;
            let sides = get_sides(&grid, &r);
            println!(
                "{}: {count}c x {sides}s = {}",
                grid.get_force(*r.iter().next().unwrap()) as char,
                count * sides
            );
            count * sides
        })
        .sum::<u64>();
    println!("{res}");

    Ok(())
}

fn get_sides(grid: &Grid, region: &HashSet<Position2D>) -> u64 {
    let target = grid.get_force(*region.iter().next().unwrap());
    // if target != b'C' {
    //     return 0;
    // };
    let mut visited: HashSet<(Position2D, Position2D)> = HashSet::new();

    let mut positions = region.iter().collect::<Vec<_>>();
    positions.sort_by_key(|p| (p.row, p.col));

    let scanner = Scanner {
        pos: positions[0].up(),
        direction: Direction2D::Right,
    };
    // println!("{} {scanner:?}", target as char);
    let mut sides = get_sides_inner(&region, scanner, &mut visited);
    // println!("{}: external sides {sides}", target as char);

    for (pos, c) in grid.items() {
        if !region.contains(&pos) {
            for dir in Direction2D::all() {
                let scanner = Scanner {
                    pos,
                    direction: Direction2D::Right,
                };
                if let Some(adjacent) = scanner.adjacent(&region) {
                    // println!(
                    //     "{}, {scanner:?} {}",
                    //     target as char,
                    //     visited.contains(&(adjacent, scanner.pos))
                    // );
                    let internal = get_sides_inner(&region, scanner.clone(), &mut visited);
                    if internal > 0 {
                        // println!(
                        //     "{}: internal sides {internal}, starting at {scanner:?}",
                        //     target as char
                        // );
                        sides += internal;
                    }
                }
            }
        }
    }

    // println!("{}: total sides {sides}", target as char);
    sides
}

fn get_sides_inner(
    region: &HashSet<Position2D>,
    mut scanner: Scanner,
    visited: &mut HashSet<(Position2D, Position2D)>,
) -> u64 {
    let mut sides = 0;

    'main: loop {
        let adjacent = scanner.adjacent(region).unwrap();
        let key = (adjacent, scanner.pos);
        if !visited.insert(key) {
            break;
        }
        // println!("{scanner:?}");

        // Hit into the region, try to turn around
        if region.contains(&scanner.at_next_pos().pos) {
            sides += 1;
            scanner = scanner.turned_left();
            continue;
        }

        // Went out of the board
        if scanner.at_next_pos().adjacent(region).is_none() {
            if let Some(adjacent) = scanner.adjacent(region) {
                visited.insert((adjacent, scanner.pos));
            }
            scanner = scanner.at_next_pos().turned_right().at_next_pos();
            sides += 1;
        } else {
            scanner = scanner.at_next_pos();
        }
    }

    sides
}

fn fill(
    grid: &Grid,
    target: u8,
    pos: Position2D,
    region: &mut Vec<Position2D>,
    visited: &mut HashSet<Position2D>,
) {
    if visited.contains(&pos) {
        return;
    }
    if grid.get(pos) != Some(target) {
        return;
    }
    region.push(pos);
    visited.insert(pos);
    for neighbor in grid.neighbour_positions_4(pos) {
        fill(grid, target, neighbor, region, visited);
    }
}

fn get_perimeter(grid: &Grid, region: &[Position2D]) -> u64 {
    let directions = [(1, 0), (0, -1), (-1, 0), (0, 1)];
    let target = grid.get_force(region[0]);
    let mut perimeter = 0;

    for &position in region {
        for &dir in &directions {
            if grid.get(position + Position2D::new(dir.0, dir.1)) != Some(target) {
                perimeter += 1;
            }
        }
    }

    perimeter
}

// 912348 too low
// 913663 too low
// 922247 too high
