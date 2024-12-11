use aoc2024::StrExt;
use hashbrown::{HashMap, HashSet};
use indicatif::ProgressIterator;

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let mut nums: HashMap<u64, u64> = file
        .lines()
        .next()
        .unwrap()
        .split_nums_whitespace::<u64>()
        .into_iter()
        .map(|v| (v, 1))
        .collect();
    let mut next_nums = HashMap::new();

    for _ in 0..75 {
        next_nums.clear();
        for (&value, count) in &nums {
            let digits = format!("{value}");
            if value == 0 {
                *next_nums.entry(1).or_default() += count;
            } else if digits.len() % 2 == 0 {
                let a = digits[..digits.len() / 2].parse::<u64>()?;
                let b = digits[digits.len() / 2..].parse::<u64>()?;
                *next_nums.entry(a).or_default() += count;
                *next_nums.entry(b).or_default() += count;
            } else {
                *next_nums.entry(value * 2024).or_default() += count;
            }
        }
        // println!("{}", next_nums.len());
        // println!("{}", next_nums.iter().collect::<HashSet<&u64>>().len());
        std::mem::swap(&mut nums, &mut next_nums);
    }
    println!("{}", nums.values().sum::<u64>());

    Ok(())
}

fn expand(value: u64, nums: &mut Vec<u64>) {
    let digits = format!("{value}");
    if value == 0 {
        nums.push(1);
    } else if digits.len() % 2 == 0 {
        nums.push(digits[..digits.len() / 2].parse::<u64>().unwrap());
        nums.push(digits[digits.len() / 2..].parse::<u64>().unwrap());
    } else {
        nums.push(value * 2024);
    }
}
