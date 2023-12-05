use aoc2023::StrExt;
use itertools::Itertools;

#[derive(Debug)]
struct Range {
    dest: u64,
    start: u64,
    length: u64,
}

impl Range {
    fn map(&self, value: u64) -> Option<u64> {
        if value >= self.start && value < self.start + self.length {
            Some(self.dest + (value - self.start))
        } else {
            None
        }
    }
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;

    let lines = input.lines().collect::<Vec<_>>();
    let seeds = lines[0]
        .split_by(b':')
        .1
        .trim()
        .split_ascii_whitespace()
        .map(|v| v.to_u64())
        .collect::<Vec<_>>();

    let mut maps = vec![];
    let mut map = vec![];

    for line in &lines[2..] {
        let line = line.trim();
        if line.is_empty() {
            continue;
        }
        if line.contains("map") {
            if !map.is_empty() {
                maps.push(map);
            }
            map = vec![];
            continue;
        }
        let nums = line
            .split_ascii_whitespace()
            .map(|v| v.to_u64())
            .collect::<Vec<_>>();
        let range = Range {
            dest: nums[0],
            start: nums[1],
            length: nums[2],
        };
        map.push(range);
    }
    maps.push(map);

    let ret = seeds
        .into_iter()
        .map(|mut v| {
            for map in &maps {
                v = map_range(map, v);
            }
            v
        })
        .min()
        .unwrap();
    println!("{ret}");

    Ok(())
}

fn map_range(ranges: &[Range], value: u64) -> u64 {
    let mapped = ranges
        .iter()
        .filter_map(|r| r.map(value))
        .collect::<Vec<_>>();
    assert!(mapped.len() <= 1);
    if mapped.is_empty() {
        value
    } else {
        mapped[0]
    }
}
