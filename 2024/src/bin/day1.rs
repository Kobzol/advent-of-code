use aoc2024::StrExt;

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;

    let mut lists = (vec![], vec![]);
    let ret = file.lines().for_each(|l| {
        let nums = l.split_nums_whitespace::<u32>();
        lists.0.push(nums[0]);
        lists.1.push(nums[1]);
    });
    lists.0.sort();
    lists.1.sort();

    println!(
        "{}",
        lists
            .0
            .into_iter()
            .map(|a| lists.1.iter().filter(|b| **b == a).count() as u32 * a)
            .sum::<u32>()
    );

    Ok(())
}
