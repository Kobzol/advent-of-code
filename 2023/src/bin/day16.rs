use itertools::Itertools;
use rayon::prelude::*;

use aoc2023::grid::{Grid, Position2D};
use aoc2023::Set;

const RIGHT: Position2D = Position2D { row: 0, col: 1 };
const LEFT: Position2D = Position2D { row: 0, col: -1 };
const UP: Position2D = Position2D { row: -1, col: 0 };
const DOWN: Position2D = Position2D { row: 1, col: 0 };

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash, Ord, PartialOrd)]
struct Ray {
    position: Position2D,
    direction: Position2D,
}

impl Ray {
    fn forward(self) -> Self {
        Self {
            position: self.position + self.direction,
            direction: self.direction,
        }
    }

    fn with_dir(self, direction: Position2D) -> Self {
        Self {
            position: self.position,
            direction,
        }
    }
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let grid = Grid::from_str(&input);

    let mut starting_positions = vec![];
    for col in 0..grid.width() {
        starting_positions.push(vec![Ray {
            position: Position2D {
                row: -1,
                col: col as isize,
            },
            direction: DOWN,
        }]);
        starting_positions.push(vec![Ray {
            position: Position2D {
                row: grid.height() as isize,
                col: col as isize,
            },
            direction: UP,
        }]);
    }
    for row in 0..grid.height() {
        starting_positions.push(vec![Ray {
            position: Position2D {
                row: row as isize,
                col: -1,
            },
            direction: RIGHT,
        }]);
        starting_positions.push(vec![Ray {
            position: Position2D {
                row: row as isize,
                col: grid.width() as isize,
            },
            direction: LEFT,
        }]);
    }
    let ret = starting_positions
        .into_par_iter()
        // .into_iter()
        .map(|mut rays| {
            let mut energized: Set<Position2D> = Set::default();
            let mut visited = Set::default();
            loop {
                move_rays(&grid, &mut rays, &mut energized);
                let hash = calc_hash(&rays);
                if visited.contains(&hash) {
                    break;
                }
                visited.insert(hash);
            }
            energized.len()
        })
        .max()
        .unwrap();
    println!("{ret}");

    Ok(())
}

fn calc_hash(rays: &[Ray]) -> String {
    let mut rays = rays.iter().collect_vec();
    rays.sort();
    let mut hash = String::new();
    for ray in rays {
        hash.push_str(&format!(
            "{}-{};{}-{}x",
            ray.position.row, ray.position.col, ray.direction.row, ray.direction.col
        ));
    }
    hash
}

fn move_rays(grid: &Grid, rays: &mut Vec<Ray>, energized: &mut Set<Position2D>) {
    let mut next_ray_set = Set::default();
    for ray in rays.iter() {
        if grid.contains_pos(ray.position) {
            energized.insert(ray.position);
        }
        let next_ray = ray.forward();
        if let Some(c) = grid.get(next_ray.position) {
            match c {
                b'.' => {
                    next_ray_set.insert(next_ray);
                }
                b'|' if is_vertical(next_ray.direction) => {
                    next_ray_set.insert(next_ray);
                }
                b'-' if is_horizontal(next_ray.direction) => {
                    next_ray_set.insert(next_ray);
                }
                b'|' => {
                    next_ray_set.insert(next_ray.with_dir(UP));
                    next_ray_set.insert(next_ray.with_dir(DOWN));
                }
                b'-' => {
                    next_ray_set.insert(next_ray.with_dir(LEFT));
                    next_ray_set.insert(next_ray.with_dir(RIGHT));
                }
                b'/' => {
                    let next_dir = match next_ray.direction {
                        UP => RIGHT,
                        LEFT => DOWN,
                        RIGHT => UP,
                        DOWN => LEFT,
                        _ => panic!(),
                    };
                    next_ray_set.insert(next_ray.with_dir(next_dir));
                }
                b'\\' => {
                    let next_dir = match next_ray.direction {
                        UP => LEFT,
                        LEFT => UP,
                        RIGHT => DOWN,
                        DOWN => RIGHT,
                        _ => panic!(),
                    };
                    next_ray_set.insert(next_ray.with_dir(next_dir));
                }
                _ => panic!(),
            }
        }
    }

    *rays = next_ray_set.into_iter().collect();
}

fn is_vertical(direction: Position2D) -> bool {
    direction == UP || direction == DOWN
}

fn is_horizontal(direction: Position2D) -> bool {
    direction == LEFT || direction == RIGHT
}
