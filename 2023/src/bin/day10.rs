use std::iter::from_fn;

use aoc2023::grid::{Grid, Position2D};
use aoc2023::Set;

fn get_candidates(grid: &Grid, pos: Position2D) -> Vec<Position2D> {
    match grid.get(pos) {
        Some(b'S') => vec![pos.right(), pos.down(), pos.left(), pos.up()],
        Some(b'-') => vec![pos.right(), pos.left()],
        Some(b'|') => vec![pos.down(), pos.up()],
        Some(b'L') => vec![pos.right(), pos.up()],
        Some(b'J') => vec![pos.left(), pos.up()],
        Some(b'7') => vec![pos.down(), pos.left()],
        Some(b'F') => vec![pos.right(), pos.down()],
        _ => vec![],
    }
}

fn get_neighbours(grid: &Grid, pos: Position2D) -> Vec<Position2D> {
    let candidates = get_candidates(grid, pos);

    candidates
        .into_iter()
        .filter(|candidate| get_candidates(grid, *candidate).contains(&pos))
        .collect()
}

fn find_loop(grid: &Grid, start: Position2D) -> Vec<Position2D> {
    let mut loop_items = vec![];

    let mut stack = Vec::new();
    stack.push(start);
    while let Some(pos) = stack.pop() {
        if pos == start && loop_items.len() > 1 {
            break;
        }

        for neighbor in get_neighbours(grid, pos) {
            if Some(&neighbor) != loop_items.last() {
                stack.push(neighbor);
                break;
            }
        }
        loop_items.push(pos);
    }
    loop_items
}

fn find_max(grid: &Grid, start: Position2D) -> u64 {
    (find_loop(grid, start).len() / 2) as u64
}

fn enclosed_positions(grid: &Grid, mut lp: Vec<Position2D>) -> u64 {
    let mut inner_dots = Set::default();
    lp.push(lp[0]);

    for window in lp.windows(2) {
        let (item, next) = (window[0], window[1]);
        if next == item.right() {
            // inner_dots.extend(gen_dir(&grid, next, |p| p.down()));
            inner_dots.insert(item.down());
            inner_dots.insert(next.down());
        } else if next == item.down() {
            // inner_dots.extend(gen_dir(&grid, next, |p| p.left()));
            inner_dots.insert(item.left());
            inner_dots.insert(next.left());
        } else if next == item.left() {
            // inner_dots.extend(gen_dir(&grid, next, |p| p.up()));
            inner_dots.insert(item.up());
            inner_dots.insert(next.up());
            // inner_dots.insert(item.up());
        } else if next == item.up() {
            // inner_dots.extend(gen_dir(&grid, next, |p| p.right()));
            inner_dots.insert(item.right());
            inner_dots.insert(next.right());
        } else {
            panic!();
        }
    }

    let lp_set = lp.iter().copied().collect::<Set<_>>();
    let mut inner_positions = inner_dots
        .into_iter()
        .filter(|pos| !lp_set.contains(pos) && grid.contains_pos(*pos))
        .collect::<Set<_>>();
    // let mut grid2 = grid.clone();
    // for pos in &inner_positions {
    //     grid2.set(*pos, b'X');
    // }
    // println!("{grid2}");

    let mut filled_positions = Set::default();
    for pos in inner_positions {
        flood_fill(&grid, pos, &mut filled_positions);
    }

    // println!("{grid}");
    // let mut grid2 = grid.clone();
    // for pos in &inner_dots {
    //     grid2.set(*pos, b'x');
    // }
    // println!("{grid2}");
    // inner_dots.len() as u64
    filled_positions.len() as u64
}

fn gen_dir<F: Fn(Position2D) -> Position2D + 'static>(
    grid: &Grid,
    mut pos: Position2D,
    next_fn: F,
) -> impl Iterator<Item = Position2D> + '_ {
    from_fn(move || {
        pos = next_fn(pos);
        if grid.get(pos) == Some(b'.') {
            Some(pos)
        } else {
            None
        }
    })
}

fn hits<F: Fn(Position2D) -> Position2D>(
    grid: &Grid,
    lp_set: &Set<Position2D>,
    mut pos: Position2D,
    next_fn: F,
) -> bool {
    /*
    for (pos, item) in grid.items() {
        if item == b'.' && !filled_positions.contains(&pos) {
            let enclosed = hits(&grid, &lp_set, pos, |p| p.right())
                && hits(&grid, &lp_set, pos, |p| p.left())
                && hits(&grid, &lp_set, pos, |p| p.up())
                && hits(&grid, &lp_set, pos, |p| p.down());
            if enclosed {
                filled_positions.insert(pos);
            }
        }
    }
    */
    while grid.contains_pos(pos) {
        if lp_set.contains(&pos) {
            return true;
        }
        pos = next_fn(pos);
    }
    false
}

fn calc_enclosed(grid: &Grid, start: Position2D) {
    let mut grid = grid.clone();
    let mut lp = find_loop(&grid, start);
    let lp_set = lp.iter().copied().collect::<Set<_>>();
    for (pos, _) in grid.items() {
        if !lp_set.contains(&pos) {
            grid.set(pos, b'.');
        }
    }

    println!("{}", enclosed_positions(&grid, lp.clone()));
    lp.reverse();
    println!("{}", enclosed_positions(&grid, lp));
}

fn flood_fill(grid: &Grid, pos: Position2D, positions: &mut Set<Position2D>) {
    if !positions.insert(pos) {
        return;
    }
    for neighbor in [pos.up(), pos.down(), pos.left(), pos.right()] {
        if grid.get(neighbor) == Some(b'.') {
            flood_fill(grid, neighbor, positions);
        }
    }
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let grid = Grid::from_str(&input);
    let start = grid.find_pos(b'S');

    calc_enclosed(&grid, start);

    Ok(())
}
// 540 too low
// 831 wrong
// 1141 too high
// 5241 too high
