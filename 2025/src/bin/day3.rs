use aoc2025::NumExt;
use hashbrown::HashMap;

fn main() -> anyhow::Result<()> {
    let data = std::fs::read_to_string("input.txt")?;

    let mut cache: HashMap<(&str, u64), u64> = HashMap::new();
    let sum = data
        .lines()
        // .skip(1)
        // .take(1)
        .map(|l| dbg!(joltage(dbg!(l), 12, &mut cache)))
        .sum::<u64>();
    println!("{sum}");
    Ok(())
}

fn joltage<'a>(line: &'a str, length: u64, cache: &mut HashMap<(&'a str, u64), u64>) -> u64 {
    if let Some(ret) = cache.get(&(line, length)) {
        return *ret;
    }

    if length == 1 {
        // println!("{line} ... {length}");
        let res = line.bytes().map(|b| b - b'0').max().unwrap_or(0) as u64;
        cache.insert((line, length), res);
        return res;
    }

    let mut max = 0;
    let bytes = line.as_bytes();
    for i in 0..bytes.len() - 1 {
        let subjoltage = joltage(&line[i + 1..], length - 1, cache);
        let value = (bytes[i] - b'0') as u64 * 10_u64.pow(subjoltage.num_digits()) + subjoltage;
        max = value.max(max);
    }

    cache.insert((line, length), max);
    max
}
