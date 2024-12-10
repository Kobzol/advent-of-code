use aoc2024::grid::Grid;
use aoc2024::vector::Position2D;

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let grid = Grid::from_str(&file);
    let res = grid
        .items()
        .iter()
        .filter(|(pos, c)| *c == b'0')
        .map(|(pos, c)| get_score(&grid, *pos))
        .sum::<u64>();
    println!("{res}");

    Ok(())
}

fn get_score(grid: &Grid, pos: Position2D) -> u64 {
    let mut score = 0;
    assert_eq!(grid.get(pos), Some(b'0'));
    expand_path(&grid, pos, &mut score);
    score
}

fn expand_path(grid: &Grid, pos: Position2D, score: &mut u64) {
    let Some(val) = grid.get(pos) else {
        return;
    };
    let val = val - b'0';

    if val == 9 {
        *score += 1;
        return;
    }

    let next = (val + 1) + b'0';
    for neighbor in grid.neighbour_positions_4(pos) {
        if grid.get(neighbor) == Some(next) {
            expand_path(grid, neighbor, score);
        }
    }
}
