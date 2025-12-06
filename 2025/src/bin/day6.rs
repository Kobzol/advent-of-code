use aoc2025::StrExt;

#[derive(Copy, Clone, Debug, PartialEq, Eq)]
enum Op {
    Add,
    Mul,
}

fn main() -> anyhow::Result<()> {
    let data = std::fs::read_to_string("input.txt")?;
    let rows = data.lines().collect::<Vec<_>>();
    let mut ops = vec![];
    let mut splits = vec![];
    for (index, col) in rows.last().unwrap().chars().enumerate() {
        if col == '*' {
            ops.push(Op::Mul);
            if index > 0 {
                splits.push(index - 1);
            }
        } else if col == '+' {
            ops.push(Op::Add);
            if index > 0 {
                splits.push(index - 1);
            }
        }
    }

    let row_count = rows.len() - 1;
    let longest_col = rows.iter().take(row_count).map(|l| l.len()).max().unwrap();
    let mut num_rows = vec![];
    for row in rows.iter().take(row_count) {
        let mut row = row.replace(" ", "Z").as_bytes().to_vec();
        row.extend(std::iter::repeat(b'Z').take(longest_col.saturating_sub(row.len())));

        for split in &splits {
            row[*split] = b'x';
        }
        let row = String::from_utf8(row)
            .unwrap()
            .split("x")
            .map(|s| s.to_owned())
            .collect::<Vec<_>>();
        eprintln!("{row:?}");
        num_rows.push(row);
    }

    let mut result = 0;
    for bigcol in 0..num_rows[0].len() {
        let op = ops[bigcol];
        let init = if op == Op::Mul { 1 } else { 0 };
        let op = if op == Op::Mul {
            |a, b| a * b
        } else {
            |a, b| a + b
        };
        let width = num_rows[0][bigcol].len();
        let nums = (0..width)
            .rev()
            .map(|c| {
                let mut num = 0u64;
                let items = (0..row_count)
                    .map(|r| num_rows[r][bigcol].as_bytes()[c])
                    .collect::<Vec<_>>();
                for (index, v) in items.iter().enumerate() {
                    let v = match v {
                        b'Z' => 0,
                        v => {
                            assert!(v.is_ascii_digit());
                            *v - b'0'
                        }
                    };
                    num *= 10;
                    num += v as u64;
                    if items[index + 1..].iter().all(|c| *c == b'Z') {
                        break;
                    }
                }
                num
            })
            .collect::<Vec<_>>();
        eprintln!("{nums:?}");
        result += dbg!(nums.iter().fold(init, op));
    }
    println!("{result}");

    Ok(())
}

fn part1(data: &str) {
    let rows = data
        .lines()
        .map(|l| l.split(" ").filter(|v| *v != "").collect::<Vec<_>>())
        .collect::<Vec<_>>();
    let cols = rows[0].len();

    let mut result = 0;
    for col in 0..cols {
        let op = rows.last().unwrap()[col];
        let init = if op == "*" { 1 } else { 0 };
        let op = if op == "*" {
            |a, b| a * b
        } else {
            |a, b| a + b
        };
        let value = rows
            .iter()
            .take(rows.len() - 1)
            .map(|r| dbg!(r[col].to_u64()))
            .fold(init, op);
        result += value;
    }
    println!("{result}");
}
