use aoc2025::StrExt;
use hashbrown::HashSet;
use std::collections::VecDeque;
use std::fmt::{Display, Formatter};

#[derive(Debug, PartialEq, Eq, Hash, Copy, Clone)]
struct FreshIngredientRange {
    start: u64,
    end: u64,
}

impl FreshIngredientRange {
    fn empty() -> Self {
        Self { start: 0, end: 0 }
    }
    fn new(start: u64, end: u64) -> Self {
        Self { start, end }
    }

    fn contains(&self, ingredient: u64) -> bool {
        self.start <= ingredient && ingredient < self.end
    }
    fn size(&self) -> usize {
        (self.end - self.start) as usize
    }
    fn is_empty(&self) -> bool {
        self.start == self.end
    }
    fn intersects(&self, range: &FreshIngredientRange) -> bool {
        if self.end <= range.start {
            false
        } else if self.start >= range.end {
            false
        } else {
            true
        }
    }
    fn covers(&self, range: &FreshIngredientRange) -> bool {
        self.start <= range.start && self.end >= range.end
    }
}

impl Display for FreshIngredientRange {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        f.write_fmt(format_args!("({}, {})", self.start, self.end))
    }
}

#[derive(Default, Debug)]
struct RangeSet {
    ranges: HashSet<FreshIngredientRange>,
}

impl RangeSet {
    fn merge(&mut self, mut add: FreshIngredientRange) {
        let mut to_add = VecDeque::from([add]);

        while let Some(add) = to_add.pop_front() {
            let intersects = self.ranges.iter().find(|r| r.intersects(&add)).copied();
            if let Some(range) = intersects {
                if add.covers(&range) {
                    eprintln!("{add} covers {range}");
                    self.ranges.remove(&range);
                    to_add.push_front(add);
                } else if range.covers(&add) {
                    eprintln!("{range} already covers {add}, skipping");
                    // Don't do anything, we already have `add` covered
                } else {
                    let r1_start = range.start.min(add.start);
                    let r1_end = range.start.max(add.start);
                    let r1 = FreshIngredientRange::new(r1_start, r1_end);

                    let r2_end = range.end.min(add.end);
                    let r2 = FreshIngredientRange::new(r1.end, r2_end);

                    let r3_end = range.end.max(add.end);
                    let r3 = FreshIngredientRange::new(r2.end, r3_end);

                    eprintln!("Splitting {range} and {add} into {:?}", [r1, r2, r3]);

                    assert!(!r1.intersects(&r2));
                    assert!(!r1.intersects(&r3));
                    assert!(!r2.intersects(&r3));

                    self.ranges.remove(&range);
                    to_add.extend([r1, r2, r3]);
                }
            } else {
                eprintln!("{add} doesn't intersect, adding");
                self.ranges.insert(add);
            }
        }
    }
}

fn main() -> anyhow::Result<()> {
    let data = std::fs::read_to_string("input.txt")?;
    let mut iter = data.lines();
    let ranges: Vec<FreshIngredientRange> = (&mut iter)
        .take_while(|l| l.trim() != "")
        .map(|line| {
            let (s, e) = line.split_by(b'-');
            FreshIngredientRange::new(s.to_u64(), e.to_u64() + 1)
        })
        .collect();
    // let ingredients = iter.map(|line| line.to_u64()).collect::<Vec<u64>>();
    // let fresh = ingredients
    //     .iter()
    //     .filter(|i| is_fresh(&ranges, **i))
    //     .count();
    // println!("{fresh}");

    let mut set = RangeSet::default();
    for range in ranges {
        set.merge(range);
    }
    for (index, i) in set.ranges.iter().enumerate() {
        for j in set.ranges.iter().skip(index + 1) {
            if i.intersects(j) {
                panic!("Intersection of {i} and {j}");
            }
        }
    }
    eprintln!("{set:?}");
    let count = set.ranges.iter().map(|r| r.size()).sum::<usize>();
    println!("{count}");

    Ok(())
}

fn is_fresh(fresh: &[FreshIngredientRange], ingredient: u64) -> bool {
    fresh.iter().any(|range| range.contains(ingredient))
}
