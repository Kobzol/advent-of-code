fn get_num(input: &str, start: bool) -> u32 {
    let digits = [
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    ];
    let mut indices = (0..input.len()).collect::<Vec<_>>();
    if !start {
        indices.reverse();
    }

    for index in indices {
        if input.as_bytes()[index].is_ascii_digit() {
            return input
                .chars()
                .nth(index)
                .unwrap()
                .to_string()
                .parse::<u32>()
                .unwrap();
        }
        for (num_index, digit) in digits.iter().enumerate() {
            if input[index..].starts_with(digit) {
                return (num_index + 1) as u32;
            }
        }
    }

    panic!()
}

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let ret = file
        .lines()
        .map(|l| {
            let fc = get_num(l, true);
            let lc = get_num(l, false);
            fc * 10 + lc
        })
        .sum::<u32>();
    println!("{ret}");

    Ok(())
}
