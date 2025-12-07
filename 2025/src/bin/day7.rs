use aoc2025::grid::Grid;
use aoc2025::vector::Position2D;
use aoc2025::{Map, Set};

fn main() -> anyhow::Result<()> {
    let data = std::fs::read_to_string("input.txt")?;
    let mut grid = Grid::from_str(&data);
    let start = grid.find_pos(b'S');
    let timelines = move_beams_part2(&mut grid, start);
    println!("{timelines}");
    // println!("{grid}");

    Ok(())
}

// 479948638263 too low

fn move_beams_part1(grid: &Grid, beams: Set<Position2D>, splits: &mut u32) -> Set<Position2D> {
    let mut next_beams = Set::default();
    for beam in beams {
        let next = beam.down();
        if let Some(c) = grid.get(next) {
            if c == b'.' {
                next_beams.insert(next);
            } else if c == b'^' {
                let left = next.left();
                let right = next.right();
                assert!(grid.contains_pos(left));
                assert!(grid.contains_pos(right));
                next_beams.extend([left, right]);
                *splits += 1;
            } else {
                unreachable!();
            }
        }
    }
    next_beams
}

fn move_beams_part2(grid: &mut Grid, beam: Position2D) -> u64 {
    struct Beam {
        pos: Position2D,
        parent_timelines: u64,
    }

    impl Beam {
        fn with(&self, pos: Position2D) -> Self {
            Self {
                pos,
                parent_timelines: self.parent_timelines,
            }
        }
    }

    let mut beams = vec![Beam {
        pos: beam,
        parent_timelines: 1,
    }];

    let mut timelines = 0;
    while !beams.is_empty() {
        println!("-----");
        for beam in &beams {
            println!("{}: {}", beam.pos, beam.parent_timelines);
        }
        println!("-----");
        let mut next_beams: Map<Position2D, u64> = Map::default();
        for beam in beams {
            grid.set(beam.pos, (beam.parent_timelines % 10) as u8 + b'0');
            let next = beam.pos.down();
            if let Some(c) = grid.get(next) {
                if c == b'.' {
                    *next_beams.entry(next).or_default() += beam.parent_timelines;
                } else if c == b'^' {
                    let left = next.left();
                    *next_beams.entry(left).or_default() += beam.parent_timelines;
                    let right = next.right();
                    *next_beams.entry(right).or_default() += beam.parent_timelines;
                } else {
                    unreachable!();
                }
            } else {
                timelines += beam.parent_timelines;
            }
        }
        beams = next_beams
            .into_iter()
            .map(|(pos, parent_timelines)| Beam {
                pos,
                parent_timelines,
            })
            .collect();
    }

    timelines
}

fn move_beams_cache(grid: &Grid, beam: Position2D) -> u64 {
    let mut timelines = 0;
    let path = Path(vec![beam]);
    let mut visited = Set::default();
    run(grid, beam, path, &mut visited, &mut timelines);
    timelines
}

#[derive(PartialEq, Eq, Hash, Debug, Default, Clone)]
struct Path(Vec<Position2D>);

impl Path {
    fn with(&self, pos: Position2D) -> Self {
        let mut path = self.clone();
        path.0.push(pos);
        path
    }
}

fn run(
    grid: &Grid,
    mut beam: Position2D,
    mut path: Path,
    visited: &mut Set<Path>,
    timelines: &mut u64,
) {
    loop {
        if visited.contains(&path) {
            eprintln!("hit");
            return;
        }
        visited.insert(path.clone());

        let next = beam.down();
        if let Some(c) = grid.get(next) {
            match c {
                b'.' => {
                    beam = next;
                    path.0.push(beam);
                }
                b'^' => {
                    let left = next.left();
                    let right = next.right();
                    let mut visited = Set::default();
                    run(grid, left, path.with(left), &mut visited, timelines);
                    run(grid, right, path.with(right), &mut visited, timelines);
                    break;
                }
                _ => unreachable!(),
            }
        } else {
            *timelines += 1;
            break;
        }
    }
}
