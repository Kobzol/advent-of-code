use aoc2024::StrExt;
use rayon::iter::IntoParallelIterator;
use rayon::iter::ParallelIterator;
use std::ops::BitXor;
use std::sync::atomic::{AtomicU64, Ordering};

#[derive(Debug)]
struct Monkey {
    diffs: Vec<i8>,
    prices: Vec<u64>,
}

impl Monkey {
    fn value(&self, diff: &[i8]) -> Option<u64> {
        for index in 0..self.diffs.len() - diff.len() {
            if &self.diffs[index..index + diff.len()] == diff {
                return Some(self.prices[index]);
            }
        }

        None
    }
}

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let monkeys = file
        .lines()
        .map(|l| l.to_u64())
        .map(|n| generate_sequence(n, 2000))
        .collect::<Vec<_>>();

    let mut max = AtomicU64::new(0);
    (-9..=9).into_par_iter().for_each(|v0| {
        for v1 in -9..=9 {
            for v2 in -9..=9 {
                for v3 in -9..=9 {
                    let seq = &[v0, v1, v2, v3];
                    let res = monkeys.iter().filter_map(|m| m.value(seq)).sum::<u64>();
                    max.fetch_max(res, Ordering::Relaxed);
                }
            }
        }
    });

    println!("{}", max.load(Ordering::Relaxed));

    Ok(())
}

fn generate_sequence(mut secret: u64, n: u64) -> Monkey {
    let mut diffs = vec![];
    let mut prices = vec![];

    let mut last = secret;
    for _ in 0..n {
        secret = next_val(secret);

        let digit = secret % 10;
        let last_digit = last % 10;
        let diff = digit as i8 - last_digit as i8;
        diffs.push(diff);
        if diffs.len() >= 4 {
            prices.push(digit);
        }
        last = secret;
    }
    Monkey { diffs, prices }
}

fn nth_next_val(mut secret: u64, n: u64) -> u64 {
    for _ in 0..n {
        secret = next_val(secret);
    }
    secret
}

fn next_val(secret: u64) -> u64 {
    let val = secret * 64;
    let secret = secret.bitxor(val);
    let secret = secret % 16777216;
    let val = secret / 32;
    let secret = secret.bitxor(val);
    let secret = secret % 16777216;
    let val = secret * 2048;
    let secret = secret.bitxor(val);
    let secret = secret % 16777216;
    secret
}
