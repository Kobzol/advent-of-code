enum Rotation {
    Left(i32),
    Right(i32),
}

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;

    let rotations = file
        .lines()
        .map(|line| {
            let mut it = line.bytes();
            let dir = it.next().unwrap();
            let count = String::from_utf8(it.collect::<Vec<_>>())
                .unwrap()
                .parse::<i32>()
                .unwrap();
            match dir {
                b'L' => Rotation::Left(count),
                b'R' => Rotation::Right(count),
                _ => unreachable!(),
            }
        })
        .collect::<Vec<Rotation>>();

    let mut dial = 50i32;
    let mut password = 0;
    for rotation in rotations {
        match rotation {
            Rotation::Left(c) => {
                for _ in 0..c {
                    dial = dial - 1;
                    if dial == 0 {
                        password += 1;
                    } else if dial == -1 {
                        dial = 99;
                    }
                }
            }
            Rotation::Right(c) => {
                for _ in 0..c {
                    dial = (dial + 1) % 100;
                    if dial == 0 {
                        password += 1;
                    }
                }
            }
        }
        // println!("{dial}");
    }
    println!("{password}");

    Ok(())
}
