use aoc2023::grid::{Grid, Position2D};
use aoc2023::Set;
use fxhash::FxBuildHasher;
use hashbrown::HashSet;
use itertools::Itertools;

fn expand(grid: Grid) -> Grid {
    Grid::from_rows(
        grid.into_rows()
            .into_iter()
            .flat_map(|row| {
                if row.iter().all(|&c| c == b'.') {
                    vec![row.clone(), row]
                } else {
                    vec![row]
                }
            })
            .collect(),
    )
}

fn shortest_path_expanded(a: Position2D, b: Position2D) -> u64 {
    let row = a.row.abs_diff(b.row);
    let col = a.col.abs_diff(b.col);
    (row + col) as u64
}

fn shortest_path_unexpanded(
    a: Position2D,
    b: Position2D,
    empty_rows: &Set<usize>,
    empty_cols: &Set<usize>,
) -> u64 {
    const EXPAND: usize = 1000000;

    let mut start = a;
    let mut dist = 0;
    while start.col != b.col {
        let offset = if empty_cols.contains(&start.ucol()) {
            EXPAND
        } else {
            1
        };

        let dir = (b.col - start.col).signum();
        start.col += dir;
        dist += offset;
    }
    while start.row != b.row {
        let offset = if empty_rows.contains(&start.urow()) {
            EXPAND
        } else {
            1
        };

        let dir = (b.row - start.row).signum();
        start.row += dir;
        dist += offset;
    }

    dist as u64
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let grid = Grid::from_str(&input);
    // let grid = expand(expand(grid).transpose()).transpose();

    let mut empty_rows = Set::default();
    let mut empty_cols = Set::default();
    for row in 0..grid.height() {
        if (0..grid.width()).all(|col| grid.get_force((row, col)) == b'.') {
            empty_rows.insert(row);
        }
    }
    for col in 0..grid.width() {
        if (0..grid.height()).all(|row| grid.get_force((row, col)) == b'.') {
            empty_cols.insert(col);
        }
    }
    println!("{empty_rows:?} {empty_cols:?}");

    let galaxies = grid
        .items()
        .iter()
        .filter_map(|(pos, item)| (*item == b'#').then(|| *pos))
        .collect::<Vec<_>>();
    let ret = galaxies
        .iter()
        .combinations(2)
        .map(|c| shortest_path_unexpanded(*c[0], *c[1], &empty_rows, &empty_cols))
        .sum::<u64>();
    println!("{ret}");

    Ok(())
}
