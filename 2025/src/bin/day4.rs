use aoc2025::grid::Grid;

fn main() -> anyhow::Result<()> {
    let data = std::fs::read_to_string("input.txt")?;
    let mut grid = Grid::from_str(&data);
    let mut removed = 0;

    loop {
        let (next, removed_now) = remove(grid);
        if removed_now == 0 {
            break;
        }
        removed += removed_now;
        grid = next;
    }
    println!("{removed}");

    Ok(())
}

fn remove(grid: Grid) -> (Grid, u64) {
    let mut next = grid.clone();
    let to_remove = grid
        .items()
        .into_iter()
        .filter(|(pos, c)| *c == b'@')
        .filter(|(pos, c)| {
            grid.neighbours_9(*pos)
                .iter()
                .filter(|c| **c == b'@')
                .count()
                < 4
        })
        .collect::<Vec<_>>();
    let removed = to_remove.len() as u64;
    for (pos, _) in to_remove {
        next.set(pos, b'x');
    }

    (next, removed)
}
