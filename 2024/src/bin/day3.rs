use aoc2024::StrExt;
use regex::Regex;

fn main() -> anyhow::Result<()> {
    let nums = Regex::new(r#"mul\((?P<left>\d+),(?P<right>\d+)\)"#)?;
    let inst = Regex::new(r#"do[^n]|don't"#)?;

    let file = std::fs::read_to_string("input.txt")?;

    let mut inst_regex = inst.find_iter(&file).peekable();

    let mut sum = 0;
    let mut enabled = true;
    for capture in nums.captures_iter(&file) {
        while let Some(next_peek) = inst_regex.peek().cloned() {
            if capture.get(0).unwrap().start() > next_peek.start() {
                let next = inst_regex.next().unwrap();
                if next.as_str() == "don't" {
                    enabled = false;
                } else {
                    enabled = true;
                }
            } else {
                break;
            }
        }

        if enabled {
            let left = capture["left"].to_u32();
            let right = capture["right"].to_u32();
            sum += left * right;
        }
    }
    println!("{sum}");

    Ok(())
}
