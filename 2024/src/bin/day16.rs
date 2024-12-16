use aoc2024::grid::Grid;
use aoc2024::vector::Direction2D;
use hashbrown::HashSet;

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let grid = Grid::from_str(&file);
    let start = grid.find_pos(b'S');
    let end = grid.find_pos(b'E');
    let dir = Direction2D::Right;

    let shortest = 72428;
    let paths = pathfinding::directed::yen::yen(
        &(start, dir),
        |(pos, mut dir)| {
            let mut candidates = vec![];
            let next = *pos + dir;
            if matches!(grid.get(next), Some(b'.' | b'S' | b'E')) {
                candidates.push(((next, dir), 1));
            }
            for _ in 0..3 {
                dir = dir.turn_right();
                candidates.push(((*pos, dir), 1000));
            }

            candidates
        },
        |(pos, dir)| *pos == end,
        10,
    );
    let paths: Vec<_> = paths.into_iter().filter(|(_, c)| *c == shortest).collect();
    let mut tiles = HashSet::new();
    for path in paths {
        for (pos, _) in path.0 {
            tiles.insert(pos);
        }
    }

    println!("{}", tiles.len());

    Ok(())
}
