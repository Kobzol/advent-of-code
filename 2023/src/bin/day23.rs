use aoc2023::grid::{Grid, Position2D};
use aoc2023::{Map, Set};
use itertools::Itertools;

fn can_reach(grid: &Grid, start: Position2D, end: Position2D, visited: &Set<Position2D>) -> bool {
    pathfinding::prelude::bfs(
        &start,
        |p| {
            grid.neighbour_positions_4(*p)
                .into_iter()
                .filter(|p| !visited.contains(p) && grid.get_force(*p) != b'#')
                .collect_vec()
        },
        |p| *p == end,
    )
    .is_some()
}

fn longest_path(
    grid: &Grid,
    start: Position2D,
    end: Position2D,
    steps: u64,
    visited: &mut Set<Position2D>,
    cache: &mut Map<Position2D, u64>,
) -> Option<u64> {
    if !can_reach(grid, start, end, &visited) {
        return None;
    }
    // if let Some(s) = cache.get(&start) {
    // We have reached this spot with more steps before already
    // if s < &steps {
    //     return None;
    // }
    // }

    if start == end {
        return Some(steps);
    }
    assert!(!visited.contains(&start));
    let c = grid.get_force(start);
    assert!(c != b'#');
    let mut next_positions = match c {
        // b'>' => vec![start.right()],
        // b'v' => vec![start.down()],
        b'.' => grid
            .neighbour_positions_4(start)
            .iter()
            .filter(|p| grid.get_force(**p) != b'#')
            .copied()
            .collect_vec(),
        _ => panic!(),
    };
    next_positions.retain(|pos| !visited.contains(pos));
    let mut dist = None;

    visited.insert(start);
    for pos in next_positions {
        let d = longest_path(&grid, pos, end, steps + 1, visited, cache);
        if let Some(d) = d {
            if let Some(dist_max) = dist {
                if d > dist_max {
                    dist = Some(d);
                }
            } else {
                dist = Some(d);
            }
        }
    }
    visited.remove(&start);

    // let max_steps = cache.entry(start).or_default();
    // *max_steps = (*max_steps).max(steps);
    dist
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let mut grid = Grid::from_str(&input);
    let start = Position2D::new(0, 1);
    let end = Position2D::new((grid.height() - 1) as isize, (grid.width() - 2) as isize);

    for (pos, c) in grid.items() {
        if c == b'>' || c == b'v' {
            grid.set(pos, b'.');
        }
    }

    let ret = longest_path(
        &grid,
        start,
        end,
        0,
        &mut Default::default(),
        &mut Default::default(),
    )
    .unwrap();
    println!("{ret}");

    Ok(())
}
