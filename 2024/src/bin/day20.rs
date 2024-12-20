use aoc2024::grid::Grid;
use aoc2024::vector::Position2D;
use hashbrown::HashMap;
use indicatif::ParallelProgressIterator;
use pathfinding::prelude::bfs;
use rayon::iter::IndexedParallelIterator;
use rayon::iter::IntoParallelRefIterator;
use rayon::iter::ParallelIterator;
use std::sync::Mutex;

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let grid = Grid::from_str(&file);
    let start = grid.find_pos(b'S');
    let end = grid.find_pos(b'E');
    let path = find_shortest_path(&grid, start, end);
    let baseline = (path.len() - 1) as u64;
    println!("{baseline}");

    let pos_to_cost: HashMap<Position2D, u64> = path
        .iter()
        .enumerate()
        .map(|(index, pos)| (*pos, baseline - index as u64))
        .collect();

    let mut cheats: Mutex<HashMap<u64, u64>> = Mutex::new(HashMap::new());
    path.par_iter()
        .take(baseline as usize)
        .progress()
        .enumerate()
        .for_each(|(cost, pos)| {
            for &next in &path[cost + 1..] {
                if let Some(cheat_cost) = find_shortest_ignoring_walls(&grid, *pos, next, 20) {
                    assert!(cheat_cost <= 20);
                    let total_cost = cost as u64 + cheat_cost + pos_to_cost[&next];
                    if total_cost < baseline {
                        let saved = baseline - total_cost;
                        *cheats.lock().unwrap().entry(saved).or_default() += 1;
                    }
                }
            }
        });

    let mut values: Vec<(u64, u64)> = cheats
        .lock()
        .unwrap()
        .iter()
        .filter(|(cost, count)| **cost >= 100)
        .map(|(cost, count)| (*cost, *count))
        .collect();
    values.sort();
    for (cost, count) in &values {
        println!("{count} {cost}");
    }

    let total = values.into_iter().map(|(cost, count)| count).sum::<u64>();
    println!("{total}");

    Ok(())
}

fn part1(path: Vec<Position2D>, baseline: u64, grid: Grid, start: Position2D, end: Position2D) {
    for (cost, &pos) in path.iter().take(baseline as usize).enumerate() {
        for neighbor in grid.neighbour_positions_4(pos) {
            let c = grid.get_force(neighbor);
            if c != b'#' {
                continue;
            }
            for next in grid.neighbour_positions_4(neighbor) {
                if next != pos && path[cost + 1..].contains(&next) {
                    let next_cost = find_shortest(&grid, next, end) + 2;
                    let total_cost = next_cost + cost as u64;
                    if total_cost < baseline {
                        let saved = baseline - total_cost;
                        // if pos == Position2D::new(7, 7) {
                        //     println!("p={next}, c={cost}, nc={next_cost}, saved={saved}");
                        // }
                        // *cheats.entry(saved).or_default() += 1;
                    }
                }
            }
        }
    }
}

fn find_shortest(grid: &Grid, start: Position2D, end: Position2D) -> u64 {
    (find_shortest_path(grid, start, end).len() - 1) as u64
}

fn find_shortest_ignoring_walls(
    grid: &Grid,
    start: Position2D,
    end: Position2D,
    max: u64,
) -> Option<u64> {
    bfs(
        &start,
        |&pos| {
            if start.manhattan(pos) >= max {
                vec![]
            } else {
                grid.neighbour_positions_4(pos)
            }
        },
        |&pos| pos == end,
    )
    .map(|path| (path.len() - 1) as u64)
}

fn find_shortest_path(grid: &Grid, start: Position2D, end: Position2D) -> Vec<Position2D> {
    bfs(
        &start,
        |&pos| {
            grid.neighbour_positions_4(pos)
                .into_iter()
                .filter(|&pos| grid.get(pos) != Some(b'#'))
        },
        |&pos| pos == end,
    )
    .unwrap()
}

fn find_path(grid: &Grid, start: Position2D, end: Position2D, cheat_pos: Position2D) -> u64 {
    #[derive(Eq, PartialEq, Hash, Copy, Clone, Debug)]
    enum State {
        CheatNotUsed,
        CheatActive { remaining: usize },
        CheatUsed,
    }

    let path = bfs(
        &(start, State::CheatNotUsed),
        |&(pos, state)| {
            let neighbors = grid.neighbour_positions_4(pos).into_iter();

            let c = grid.get_force(pos);
            let next: Vec<(Position2D, State)> = match state {
                State::CheatNotUsed => {
                    if pos == cheat_pos {
                        neighbors
                            .map(|pos| (pos, State::CheatActive { remaining: 1 }))
                            .collect()
                    } else {
                        neighbors
                            .filter(|&pos| grid.get(pos) != Some(b'#'))
                            .map(|pos| (pos, State::CheatNotUsed))
                            .collect()
                    }
                }
                State::CheatActive { remaining } => {
                    if remaining == 0 {
                        if c == b'#' {
                            return vec![];
                        }
                        neighbors
                            .filter(|&pos| grid.get(pos) != Some(b'#'))
                            .map(|pos| (pos, State::CheatUsed))
                            .collect()
                    } else {
                        neighbors
                            .map(|pos| (pos, State::CheatActive { remaining: 0 }))
                            .collect()
                    }
                }
                State::CheatUsed => neighbors
                    .filter(|&pos| grid.get(pos) != Some(b'#'))
                    .map(|pos| (pos, State::CheatUsed))
                    .collect(),
            };
            next
        },
        |(pos, _)| *pos == end,
    )
    .unwrap();
    (path.len() - 1) as u64
}
// 1126443 too high
