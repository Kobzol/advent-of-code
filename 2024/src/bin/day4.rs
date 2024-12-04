use aoc2024::grid::Grid;
use aoc2024::vector::Position2D;
use std::collections::VecDeque;

fn part1(grid: &Grid) {
    let mut count = 0;
    let dirs = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1),
    ];
    for pos in grid.positions() {
        for dir in &dirs {
            if contains_word(&grid, pos, *dir, b"XMAS") {
                count += 1;
            }
        }
    }
    println!("{count}");
}

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let grid = Grid::from_str(&file);

    let mut count = 0;
    for pos in grid.positions() {
        if grid.get(pos) == Some(b'A') {
            let topleft = pos + Position2D::new(-1, -1);
            let left_diagonal = contains_word(&grid, topleft, (1, 1), b"MAS")
                || contains_word(&grid, topleft, (1, 1), b"SAM");
            if !left_diagonal {
                continue;
            }
            let topright = pos + Position2D::new(-1, 1);
            let right_diagonal = contains_word(&grid, topright, (1, -1), b"MAS")
                || contains_word(&grid, topright, (1, -1), b"SAM");
            if !right_diagonal {
                continue;
            }
            count += 1;
        }
    }
    println!("{count}");

    Ok(())
}

fn contains_word(grid: &Grid, mut pos: Position2D, dir: (isize, isize), word: &[u8]) -> bool {
    let mut needle: VecDeque<u8> = word.into_iter().copied().collect();
    while let Some(expected) = needle.pop_front() {
        if grid.get(pos) != Some(expected) {
            return false;
        }
        pos += Position2D::new(dir.0, dir.1);
    }
    true
}
// 2793 too high
