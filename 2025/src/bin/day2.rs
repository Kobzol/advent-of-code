use aoc2025::{NumExt, StrExt};

fn main() -> anyhow::Result<()> {
    let data = std::fs::read_to_string("input.txt")?;
    let ranges: Vec<u64> = data
        .split(",")
        .flat_map(|r| {
            let (start, end) = r.split_by(b'-');
            let start = start.to_u64();
            let end = end.to_u64();
            start..=end
        })
        .collect();
    let invalid_sum = ranges.into_iter().filter(is_invalid).sum::<u64>();
    println!("{invalid_sum}");

    Ok(())
}

fn is_invalid(num: &u64) -> bool {
    let num_digits = num.num_digits();
    let str = num.to_string();

    for c in 1..=num_digits / 2 {
        let c = c as usize;
        let start = &str[..c];
        let len_rem = str[c..].len();
        if (len_rem % start.len() == 0) && &str[c..] == start.repeat(len_rem / start.len()) {
            println!("{num}");
            return true;
        }
    }

    false
}
