use aoc2024::grid::Grid;
use aoc2024::vector::{Direction2D, Position2D};
use aoc2024::StrExt;
use indicatif::ProgressIterator;
use pathfinding::prelude::bfs;

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let positions: Vec<Position2D> = file
        .lines()
        .map(|l| {
            let nums = l.replace(",", " ").split_nums_whitespace::<isize>();
            Position2D::new(nums[1], nums[0])
        })
        .collect();

    // let positions = &positions[..1024];
    let start = Position2D::new(0, 0);
    // let end = Position2D::new(6, 6);
    let end = Position2D::new(70, 70);

    let mut grid = Grid::from_rows(vec![
        vec![b'.'; (end.col + 1) as usize];
        (end.row + 1) as usize
    ]);

    for &pos in positions.iter().progress() {
        grid.set(pos, b'#');
        let has_path = bfs(
            &start,
            |&p| {
                let mut neighbours = vec![];
                for dir in Direction2D::all() {
                    let newpos = p + dir;
                    if grid.get(newpos) == Some(b'.') {
                        neighbours.push(newpos);
                    }
                }
                neighbours
            },
            |p| *p == end,
        )
        .is_some();
        if !has_path {
            println!("{pos}");
            break;
        }
    }
    // for pos in path {
    //     grid.set(pos.0, b'O');
    // }
    // println!("{grid}");
    // println!("{cost}");

    Ok(())
}

fn is_empty(positions: &[Position2D], pos: Position2D, time: usize) -> bool {
    !positions[..time.min(positions.len())].contains(&pos)
}
