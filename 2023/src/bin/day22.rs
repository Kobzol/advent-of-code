use aoc2023::{Map, Set, StrExt};
use indicatif::ProgressIterator;
use itertools::{Itertools, Position};
use std::ops::Add;
use std::os::unix::raw::mode_t;

#[derive(Copy, Clone, Debug, Eq, PartialEq, Hash)]
struct Position3D(i32, i32, i32);

impl Position3D {
    fn x(&self) -> i32 {
        self.dim(0)
    }
    fn y(&self) -> i32 {
        self.dim(1)
    }
    fn z(&self) -> i32 {
        self.dim(2)
    }

    fn dim(&self, index: usize) -> i32 {
        match index {
            0 => self.0,
            1 => self.1,
            2 => self.2,
            _ => panic!(),
        }
    }
    fn with_dim(&self, index: usize, value: i32) -> Self {
        let mut new = *self;
        *new.mut_dim_ref(index) = value;
        new
    }

    fn mut_dim_ref(&mut self, index: usize) -> &mut i32 {
        match index {
            0 => &mut self.0,
            1 => &mut self.1,
            2 => &mut self.2,
            _ => panic!(),
        }
    }
}

impl Add for Position3D {
    type Output = Self;

    fn add(self, rhs: Self) -> Self::Output {
        Self(self.0 + rhs.0, self.1 + rhs.1, self.2 + rhs.2)
    }
}

#[derive(Copy, Clone, Debug, Eq, PartialEq, Hash)]
struct Brick {
    index: usize,
    start: Position3D,
    end: Position3D,
}

impl Brick {
    fn offset(&self, dir: Position3D) -> Self {
        Self {
            index: self.index,
            start: self.start + dir,
            end: self.end + dir,
        }
    }
    fn min_dim(&self, index: usize) -> i32 {
        self.start.dim(index).min(self.end.dim(index))
    }
    fn max_dim(&self, index: usize) -> i32 {
        self.start.dim(index).max(self.end.dim(index))
    }
    fn points(&self) -> Vec<Position3D> {
        let dim = (0..3).find(|d| self.start.dim(*d) != self.end.dim(*d));
        match dim {
            Some(dim) => {
                let dir = (self.end.dim(dim) - self.start.dim(dim)).signum();
                let mut brick = self.start;
                let mut points = vec![brick];
                while brick != self.end {
                    brick = brick.with_dim(dim, brick.dim(dim) + dir);
                    points.push(brick);
                }
                points
            }
            None => {
                assert_eq!(self.start, self.end);
                vec![self.start]
            }
        }
    }
    fn point_set(&self) -> Set<Position3D> {
        self.points().into_iter().collect()
    }
    fn is_on_ground(&self) -> bool {
        self.points().iter().any(|p| p.z() == 1)
    }
    fn rests_upon(&self, other: &Self) -> bool {
        let other_points = other.point_set();
        let dir = Position3D(0, 0, -1);
        for point in self.points() {
            if other_points.contains(&(point + dir)) {
                return true;
            }
        }
        false
    }
    fn overlaps(&self, other: &Self) -> bool {
        !self.point_set().is_disjoint(&other.point_set())
    }
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let mut bricks = input
        .lines()
        .enumerate()
        .map(|(index, line)| {
            let (s, e) = line.split_by(b'~');
            let s = s.split(",").map(|s| s.to_u32()).collect_vec();
            let e = e.split(",").map(|s| s.to_u32()).collect_vec();
            Brick {
                index,
                start: Position3D(s[0] as i32, s[1] as i32, s[2] as i32),
                end: Position3D(e[0] as i32, e[1] as i32, e[2] as i32),
            }
        })
        .collect_vec();
    let mut bricks = bricks.into_iter().enumerate().collect();
    assert!(fall(&mut bricks) > 0);

    let mut fallen = 0;
    for i in (0..bricks.len()).progress() {
        let mut bricks2 = bricks.clone();
        bricks2.remove(&i);
        fallen += fall(&mut bricks2);
    }

    println!("{fallen}");

    Ok(())
}

fn fall(bricks: &mut Map<usize, Brick>) -> u64 {
    let mut indices = bricks.keys().copied().collect_vec();
    indices.sort_by_key(|index| bricks.get(index).unwrap().min_dim(2));

    let mut finished = Set::default();

    let mut moved = Set::default();
    while finished.len() != bricks.len() {
        indices.retain(|index| {
            let brick = bricks.get(index).unwrap();
            if brick.is_on_ground()
                || finished
                    .iter()
                    .any(|fi| brick.rests_upon(bricks.get(fi).unwrap()))
            {
                finished.insert(*index);
                false
            } else {
                true
            }
        });
        for index in &indices {
            let brick = bricks.get_mut(index).unwrap();
            *brick = brick.offset(Position3D(0, 0, -1));
            moved.insert(*index);
        }
        // for i in indices.iter().combinations(2) {
        //     assert!(!bricks
        //         .get(i[0])
        //         .unwrap()
        //         .overlaps(bricks.get(i[1]).unwrap()));
        // }
    }
    moved.len() as u64
}

fn render<It: IntoIterator<Item = Brick>>(bricks: It, dim: usize) {
    let bricks: Vec<Brick> = bricks.into_iter().collect::<Vec<_>>();
    let min = bricks.iter().map(|b| b.min_dim(dim)).min().unwrap();
    let max = bricks.iter().map(|b| b.max_dim(dim)).max().unwrap();
    let max_z = bricks.iter().map(|b| b.max_dim(2)).max().unwrap();

    let mut map: Map<Brick, Vec<Position3D>> = Map::default();
    for brick in &bricks {
        map.insert(*brick, brick.points());
    }

    let width = (max - min) + 1;

    for z in 0..max_z {
        let z = max_z - z;
        for col in min..max + 1 {
            let mut found = false;
            for brick in &bricks {
                if map
                    .get(brick)
                    .unwrap()
                    .iter()
                    .any(|p| p.dim(2) == z && p.dim(dim) == col)
                {
                    print!("{}", brick.index);
                    found = true;
                    break;
                }
            }
            if !found {
                print!(".");
            }
        }
        println!();
    }

    println!("{}", "-".repeat(width as usize));
}
