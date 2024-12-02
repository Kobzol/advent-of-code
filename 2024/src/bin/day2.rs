use aoc2024::StrExt;

fn is_safe(level: &[u64]) -> bool {
    let diff = level.windows(2).all(|v| {
        let diff = v[0].abs_diff(v[1]);
        diff >= 1 && diff <= 3
    });
    let up = level.windows(2).all(|v| v[1] > v[0]);
    let down = level.windows(2).all(|v| v[1] < v[0]);

    diff && (up || down)
}

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;

    let ret = file
        .lines()
        .filter(|l| {
            let nums = l.split_nums_whitespace::<u64>();

            let safe = is_safe(&nums);
            if safe {
                true
            } else {
                for index in 0..nums.len() {
                    let mut nums2 = nums.clone();
                    nums2.remove(index);
                    if is_safe(&nums2) {
                        return true;
                    }
                }
                false
            }
        })
        .count();
    println!("{ret}");
    Ok(())
}
