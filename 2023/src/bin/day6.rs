use aoc2023::StrExt;

#[derive(Debug)]
struct Race {
    time: u64,
    distance: u64,
}

impl Race {
    fn count_distance(&self, hold_time: u64) -> u64 {
        assert!(hold_time <= self.time);
        let speed = hold_time;
        speed * (self.time - hold_time)
    }

    fn ways_to_win(&self) -> u64 {
        (1..=self.time)
            .map(|hold| self.count_distance(hold))
            .filter(|&d| d > self.distance)
            .count() as u64
    }
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let mut lines = input.lines();
    let time = lines
        .next()
        .unwrap()
        .replace(" ", "")
        .split_by(b':')
        .1
        .parse::<u64>()?;
    let distance = lines
        .next()
        .unwrap()
        .replace(" ", "")
        .split_by(b':')
        .1
        .parse::<u64>()?;
    let race = Race { time, distance };
    println!("{}", race.ways_to_win());

    Ok(())
}
