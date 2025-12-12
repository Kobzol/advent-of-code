use aoc2025::{Map, Set, StrExt};
use indicatif::ParallelProgressIterator;
use rayon::iter::IntoParallelIterator;
use rayon::iter::ParallelIterator;
use std::fmt::{Debug, Display, Formatter};

#[derive(Copy, Clone, Default, PartialEq, Eq, Hash)]
struct Present {
    points: [bool; 9],
}

impl Present {
    fn get(&self, row: usize, col: usize) -> bool {
        self.points[row * 3 + col]
    }

    fn set(&mut self, row: usize, col: usize, value: bool) {
        self.points[row * 3 + col] = value;
    }

    /// x..    ..x
    /// .x. -> .x.
    /// x..    ..x
    fn flip_horizontal(&self) -> Self {
        let mut present = Present::default();
        for row in 0..3 {
            for col in 0..3 {
                present.set(row, 2 - col, self.get(row, col));
            }
        }
        present
    }

    fn flip_vertical(&self) -> Self {
        let mut present = Present::default();
        for row in 0..3 {
            for col in 0..3 {
                present.set(2 - row, col, self.get(row, col));
            }
        }
        present
    }

    /// x..    .xx
    /// x.x -> x..
    /// .x.    .x.
    fn rotate_right(&self) -> Self {
        let mut res = Self::default();
        for col in 0..3 {
            for row in 0..3 {
                res.set(col, 2 - row, self.get(row, col));
            }
        }
        res
    }

    /// x..    .x.
    /// x.x -> ..x
    /// .x.    xx.
    fn rotate_left(&self) -> Self {
        let mut res = Self::default();
        for col in 0..3 {
            for row in 0..3 {
                res.set(2 - col, row, self.get(row, col));
            }
        }
        res
    }

    fn generate_variants(&self) -> Set<Present> {
        let mut variants = Set::default();
        variants.insert(*self);
        variants.insert(self.flip_horizontal());
        variants.insert(self.flip_vertical());
        variants.insert(self.flip_vertical().flip_horizontal());
        variants.insert(self.flip_horizontal().flip_vertical());

        let mut v = *self;
        for _ in 0..3 {
            v = v.rotate_right();
            variants.insert(v);
            variants.insert(v.flip_horizontal());
            variants.insert(v.flip_vertical());
            variants.insert(v.flip_horizontal().flip_vertical());
        }

        // let mut v = *self;
        // for _ in 0..3 {
        //     v = v.rotate_left();
        //     assert!(variants.contains(&v));
        //     assert!(variants.contains(&v.flip_horizontal()));
        //     assert!(variants.contains(&v.flip_vertical()));
        //     assert!(variants.contains(&v.flip_horizontal().flip_vertical()));
        // }

        variants
    }
}

impl Display for Present {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        for row in 0..3 {
            for col in 0..3 {
                write!(f, "{}", if self.get(row, col) { '#' } else { '.' })?;
            }
            writeln!(f)?;
        }
        Ok(())
    }
}

impl Debug for Present {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        <Self as Display>::fmt(self, f)
    }
}

fn main() -> anyhow::Result<()> {
    let data = std::fs::read_to_string("input.txt")?;

    let mut present: Option<Present> = None;
    let mut present_row = 0;
    let mut presents = vec![];

    let mut inputs: Vec<(Tree, Vec<usize>)> = Vec::new();
    for mut line in data.lines() {
        line = line.trim();
        if let Some(p) = &mut present {
            if line.is_empty() {
                presents.push(*p);
                present = None;
            } else {
                for (index, c) in line.as_bytes().iter().enumerate() {
                    p.set(present_row, index, *c == b'#');
                }
                present_row += 1;
            }
        } else {
            if line.ends_with(":") {
                present = Some(Present::default());
                present_row = 0;
            } else if !line.is_empty() {
                assert!(line.contains("x"));
                let (dim, present_counts) = line.split_once(": ").unwrap();
                let [width, height] = dim.split_nums_by::<usize>('x').try_into().unwrap();
                let present_counts = present_counts.split_nums_whitespace::<usize>();
                inputs.push((
                    Tree {
                        placed: vec![false; width * height],
                        width,
                        height,
                    },
                    present_counts,
                ));
            }
        }
    }
    let fits = inputs
        .into_par_iter()
        .progress()
        .map(|(tree, present_counts)| {
            if solve(&presents, tree, &present_counts) {
                1
            } else {
                0
            }
        })
        .sum::<u64>();

    println!("{fits}");

    Ok(())
}

#[derive(Clone, Debug, Default)]
struct Tree {
    placed: Vec<bool>,
    width: usize,
    height: usize,
}

impl Tree {
    fn place(&mut self, row: usize, col: usize, value: bool) {
        assert!(row < self.height);
        assert!(col < self.width);
        self.placed[row * self.width + col] = value;
    }
    fn is_placed(&self, row: usize, col: usize) -> bool {
        self.placed[row * self.width + col]
    }
    fn is_placed_opt(&self, row: usize, col: usize) -> Option<bool> {
        if row >= self.height || col >= self.width {
            None
        } else {
            Some(self.placed[row * self.width + col])
        }
    }

    fn place_present(&mut self, row: usize, col: usize, present: &Present) -> bool {
        for r in 0..3 {
            for c in 0..3 {
                if present.get(r, c) && self.is_placed_opt(row + r, col + c) != Some(false) {
                    return false;
                }
            }
        }
        for r in 0..3 {
            for c in 0..3 {
                if present.get(r, c) {
                    self.place(row + r, col + c, true);
                }
            }
        }
        true
    }
    fn remove_present(&mut self, row: usize, col: usize, present: &Present) {
        for r in 0..3 {
            for c in 0..3 {
                if present.get(r, c) {
                    self.place(row + r, col + c, false);
                }
            }
        }
    }
}

fn solve(presents: &[Present], mut tree: Tree, counts: &[usize]) -> bool {
    let variants: Map<Present, Set<Present>> = presents
        .iter()
        .map(|p| (*p, p.generate_variants()))
        .collect();
    let mut to_place: Vec<_> = counts
        .iter()
        .enumerate()
        .flat_map(|(index, count)| std::iter::repeat(presents[index]).take(*count))
        .collect();
    place(&mut to_place, &variants, &mut tree, &mut 0)
}

fn place(
    to_place: &mut [Present],
    variants: &Map<Present, Set<Present>>,
    tree: &mut Tree,
    iters: &mut usize,
) -> bool {
    if to_place.is_empty() {
        return true;
    }
    let next = to_place[0];
    for variant in &variants[&next] {
        // loop {
        //     let row = rng().random_range(0..tree.height);
        //     let col = rng().random_range(0..tree.width);
        //     if tree.place_present(row, col, &variant) {
        //         if place(&mut to_place[1..], variants, tree.clone()) {
        //             return true;
        //         } else {
        //             tree.remove_present(row, col, &variant);
        //         }
        //     }
        // }
        for row in 0..=tree.height.saturating_sub(3) {
            for col in 0..=tree.width.saturating_sub(3) {
                if tree.place_present(row, col, &variant) {
                    // println!("Placed present at {row},{col}");
                    *iters += 1;
                    if *iters > 500000 {
                        return false;
                    }
                    if place(&mut to_place[1..], variants, tree, iters) {
                        return true;
                    } else {
                        tree.remove_present(row, col, &variant);
                    }
                }
            }
        }
    }
    false
}

// fn is_placement_ok(placement: &Map<Present, Position2D>, tree: &mut Tree) -> bool {
//     tree.placed.clear();
//     for (present, pos) in placement {
//         for row in 0..3 {
//             for col in 0..3 {
//                 let v = present.get(row, col);
//                 if v {
//                     let placed = *pos + Position2D::new(row as isize, col as isize);
//                     if !tree.placed.insert(placed) {
//                         return false;
//                     }
//                 }
//             }
//         }
//     }
//     true
// }
