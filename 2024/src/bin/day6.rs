use hashbrown::HashSet;
use aoc2024::grid::Grid;
use aoc2024::vector::Position2D;

#[derive(Copy, Clone, Debug, Hash, PartialEq, Eq)]
struct Guard {
    position: Position2D,
    dir: Position2D
}

impl Guard {
    fn next_pos(&self) -> Position2D {
        self.position + self.dir
    }
    fn rotate_right(&mut self) {
        std::mem::swap(&mut self.dir.row, &mut self.dir.col);
        self.dir.col *= -1;
    }
}

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let mut grid = Grid::from_str(&file);
    let guard = Guard {
        position: grid.items().into_iter().find(|(pos, c)| *c == b'^').unwrap().0,
        dir: Position2D::new(-1, 0)
    };
    let count = grid.items()
        .into_iter()
        .filter(|(pos, c)| {
            *c == b'.'
        })
        .filter(|(pos, c)| {
            let mut grid = grid.clone();
            grid.set(*pos, b'#');
            has_loop(grid, guard)
        })
        .count();
    println!("{count}");

    Ok(())
}

fn part_1(grid: &Grid, mut guard: Guard) {
    let mut visited: HashSet<Position2D> = HashSet::default();
    let mut moves = 0;
    while grid.contains_pos(guard.position) {
        visited.insert(guard.position);
        guard = perform_move(&grid, guard);
        moves += 1;
    }
    println!("{grid}");
    println!("{}", visited.len());

}

fn has_loop(grid: Grid, mut guard: Guard) -> bool {
    let mut visited: HashSet<Guard> = HashSet::default();
    let mut moves = 0;
    while grid.contains_pos(guard.position) && moves < 100000 {
        if !visited.insert(guard) {
            return true;
        }
        guard = perform_move(&grid, guard);
    }
    false
}

fn perform_move(grid: &Grid, mut guard: Guard) -> Guard {
    while grid.get(guard.next_pos()) == Some(b'#') {
        guard.rotate_right();
    }
    guard.position = guard.next_pos();
    guard
}
