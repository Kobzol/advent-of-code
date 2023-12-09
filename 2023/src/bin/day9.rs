use aoc2023::StrExt;

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let ret = input
        .lines()
        .map(|l| {
            let nums = l
                .split_ascii_whitespace()
                .map(|v| v.trim().to_i64())
                .collect::<Vec<_>>();
            calculate_diff_back(nums)
        })
        .sum::<i64>();
    println!("{ret}");
    Ok(())
}

fn calculate_diff_back(mut nums: Vec<i64>) -> i64 {
    let mut first_nums = vec![*nums.first().unwrap()];
    while !nums.iter().all(|&v| v == 0) {
        nums = adjacent_diff(&nums).collect();
        first_nums.push(*nums.first().unwrap());
    }
    first_nums.iter().rev().fold(0, |acc, v| v - acc)
}

fn calculate_diff(mut nums: Vec<i64>) -> i64 {
    let mut last_nums = vec![*nums.last().unwrap()];
    while !nums.iter().all(|&v| v == 0) {
        nums = adjacent_diff(&nums).collect();
        last_nums.push(*nums.last().unwrap());
    }
    last_nums.into_iter().sum()
}

fn adjacent_diff(items: &[i64]) -> impl Iterator<Item = i64> + '_ {
    let it1 = items.iter();
    let it2 = items.iter().skip(1);
    it1.zip(it2).map(|(a, b)| b - a)
}
