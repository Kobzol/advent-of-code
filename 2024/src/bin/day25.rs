use aoc2024::grid::Grid;
use aoc2024::vector::Position2D;
use std::fmt::Write;

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let mut locks: Vec<[u64; 5]> = vec![];
    let mut keys: Vec<[u64; 5]> = vec![];

    let mut grids = vec![];
    let mut grid = String::new();
    for line in file.lines() {
        if line.is_empty() {
            grids.push(Grid::from_str(&grid));
            grid.clear();
        } else {
            writeln!(grid, "{line}")?;
        }
    }
    grids.push(Grid::from_str(&grid));
    for grid in grids {
        let (is_key, bitcode) = to_bitcode(grid);
        if is_key {
            keys.push(bitcode);
        } else {
            locks.push(bitcode);
        }
    }

    let mut count = 0;
    for key in &keys {
        for lock in &locks {
            if key.iter().zip(lock).all(|(a, b)| a + b <= 5) {
                count += 1;
            }
        }
    }
    println!("{count}");

    Ok(())
}

// (is_key, bitcode)
fn to_bitcode(grid: Grid) -> (bool, [u64; 5]) {
    let is_key = grid.get(Position2D::new(0, 0)) == Some(b'.');
    let mut bitcode = [0; 5];
    for col in 0..5 {
        let height = if is_key {
            (1..grid.height() - 1)
                .rev()
                .take_while(|row| grid.get(Position2D::new(*row as isize, col)) == Some(b'#'))
                .count()
        } else {
            (1..grid.height())
                .take_while(|row| grid.get(Position2D::new(*row as isize, col)) == Some(b'#'))
                .count()
        };
        bitcode[col as usize] = height as u64;
    }

    (is_key, bitcode)
}
