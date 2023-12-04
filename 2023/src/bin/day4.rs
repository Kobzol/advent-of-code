use aoc2023::StrExt;
use std::collections::HashSet;

#[derive(Debug)]
struct ScratchCard {
    id: u32,
    winning: HashSet<u32>,
    numbers: HashSet<u32>,
}

impl ScratchCard {
    fn matching(&self) -> u32 {
        self.winning.intersection(&self.numbers).count() as u32
    }

    fn score(&self) -> u32 {
        let mut s = 0;
        for _ in 0..self.matching() {
            if s == 0 {
                s = 1;
            } else {
                s = s * 2;
            }
        }
        s
    }
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let cards: Vec<ScratchCard> = input
        .lines()
        .map(|line| {
            let (id, line) = line.split_by(b':');
            let mut id = id.split_ascii_whitespace();
            id.next().unwrap();
            let id = id.next().unwrap().to_u32();

            let line = line.trim();
            let (winning, numbers) = line.split_by(b'|');
            let winning = winning
                .trim()
                .split(' ')
                .filter(|c| !c.is_empty())
                .map(|n| n.to_u32())
                .collect::<HashSet<_>>();
            let numbers = numbers
                .trim()
                .split(' ')
                .filter(|c| !c.is_empty())
                .map(|n| n.to_u32())
                .collect::<HashSet<_>>();
            ScratchCard {
                id,
                winning,
                numbers,
            }
        })
        .collect();

    let mut copies = vec![1; cards.len()];
    for (index, card) in cards.iter().enumerate() {
        let matching = card.matching() as usize;
        for i in index + 1..index + 1 + matching {
            copies[i] += copies[index];
        }
    }
    let ret = copies.iter().sum::<u32>();
    println!("{ret}");

    Ok(())
}
