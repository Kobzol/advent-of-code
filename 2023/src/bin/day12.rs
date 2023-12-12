use hashbrown::HashMap;
use indicatif::{ProgressIterator, ProgressStyle};
use itertools::Itertools;

use aoc2023::StrExt;

#[derive(Debug, Clone, Eq, PartialEq, Hash)]
struct HashState {
    run: u64,
    remaining: Vec<u8>,
    count_index: usize,
}

#[derive(Debug, Clone)]
struct Record {
    symbols: Vec<u8>,
    counts: Vec<u64>,
    result: Option<u64>,
    multiplier: u64,
    cache: HashMap<HashState, u64>,
}

impl Record {
    fn has_placeholder(&self) -> bool {
        self.placeholder_index().is_some()
    }
    fn placeholder_index(&self) -> Option<usize> {
        self.symbols.iter().position(|&c| c == b'?')
    }

    fn symbol(&self, index: usize) -> u8 {
        self.symbols[index]
    }
    fn count(&self, index: usize) -> u64 {
        self.counts[index]
    }

    fn normalize(self, repeat: usize) -> Self {
        // let mut smallest_count = self.counts.iter().copied().min().unwrap();

        // let end_hash = self
        //     .symbols
        //     .iter()
        //     .rev()
        //     .take_while(|&&c| c == b'#' || c == b'?')
        //     .count();
        // let start_hash = self
        //     .symbols
        //     .iter()
        //     .take_while(|&&c| c == b'#' || c == b'?')
        //     .count();
        // let total_hash = end_hash + start_hash + 1;
        //
        // let easy_repeat = total_hash < smallest_count as usize;
        // let result = if easy_repeat {
        //     Some(count(&mut self).pow(repeat as u32))
        // } else {
        //     None
        // };

        let mut symbols = vec![];
        for _ in 0..repeat {
            symbols.extend(self.symbols.clone());
            symbols.push(b'?');
        }
        symbols.pop().unwrap();

        // let mut multiplier = 1;
        // let ends_with_dot = self.symbols.last() == Some(&b'.');
        // if ends_with_dot {
        //     symbols = symbols[self.symbols.len()..].iter().copied().collect_vec();
        //     repeat -= 1;
        //     multiplier = count(&mut self);
        // }
        // let starts_with_dot = self.symbols.first() == Some(&b'.');
        // let ends_with_hashes = self.symbols.last() == Some(&b'#')
        //     && self.symbols.iter().rev().skip_while(|&&c| c == b'#').next() != Some(&b'?');
        // if starts_with_dot && ends_with_hashes {
        //     symbols = symbols[self.symbols.len()..].iter().copied().collect_vec();
        //     repeat -= 1;
        //     multiplier = count(&mut self);
        // }

        let counts = vec![self.counts; repeat]
            .into_iter()
            .flatten()
            .collect_vec();

        Self {
            symbols,
            counts,
            result: None,
            multiplier: 1,
            cache: Default::default(),
        }
    }

    fn is_valid(&self) -> bool {
        let mut runs = vec![];
        let mut current_run = None;

        for &item in &self.symbols {
            if item == b'#' {
                if current_run.is_none() {
                    current_run = Some(0);
                }
                *current_run.as_mut().unwrap() += 1;
            } else if item == b'.' {
                if let Some(run) = current_run {
                    runs.push(run);
                    current_run = None
                }
            } else {
                assert!(false);
            }
        }
        if let Some(run) = current_run {
            runs.push(run);
        }
        // println!(
        //     "{}: r={:?} c={:?}",
        //     String::from_utf8_lossy(&self.symbols),
        //     runs,
        //     self.counts
        // );
        runs == self.counts
    }
}

fn count(record: &mut Record) -> u64 {
    if !record.has_placeholder() {
        return if record.is_valid() { 1 } else { 0 };
    }
    let index = record.placeholder_index().unwrap();
    let mut s = 0;
    record.symbols[index] = b'.';
    s += count(record);
    record.symbols[index] = b'#';
    s += count(record);
    record.symbols[index] = b'?';
    s
}

#[derive(Copy, Clone, Debug, Default)]
struct State {
    symbol_index: usize,
    // active or next active count index
    count_index: usize,
    run: u64,
}

fn count_inc(record: &mut Record, state: State) -> u64 {
    let State {
        symbol_index,
        count_index,
        run,
    } = state;

    if symbol_index == record.symbols.len() {
        if run == 0 && count_index == record.counts.len() {
            // finished correctly, last is dot
            return 1;
        } else if run > 0
            && count_index == record.counts.len() - 1
            && run == record.count(count_index)
        {
            // finished correctly, last is hash
            return 1;
        }
        // finished incorrectly
        return 0;
    }
    if run > 0 {
        if count_index >= record.counts.len() {
            // too many runs
            return 0;
        }
        let count = record.count(count_index);
        if run > count {
            // too long run
            return 0;
        }
        let possible_length = record.symbols[symbol_index..]
            .iter()
            .take_while(|&&c| c == b'#' || c == b'?')
            .count() as u64;
        if run + possible_length < count {
            // cannot finish the current run
            return 0;
        }
    } else if count_index > record.counts.len() {
        if record.symbols[symbol_index..]
            .iter()
            .all(|&c| c == b'.' || c == b'?')
        {
            return 1;
        }
        return 0;
    }
    if count_index < record.counts.len() {
        let remaining_chars = record.symbols.len() - symbol_index;
        let remaining_counts = &record.counts[count_index..];
        let required_remaining = (remaining_counts.len() as u64).saturating_sub(1)
            + remaining_counts.iter().sum::<u64>()
            - run;
        if remaining_chars < required_remaining as usize {
            return 0;
        }
    }
    let hash_key = HashState {
        run,
        remaining: record.symbols[symbol_index..].iter().copied().collect_vec(),
        count_index,
    };
    if let Some(v) = record.cache.get(&hash_key) {
        return *v;
    }

    let symbol = record.symbol(symbol_index);

    let mut s = 0;
    match symbol {
        b'.' => {
            if run > 0 && run != record.count(count_index) {
                // Wrong run length
                return s;
            }
            let count_index = if run == 0 {
                count_index
            } else {
                count_index + 1
            };
            s += count_inc(
                record,
                State {
                    symbol_index: symbol_index + 1,
                    count_index,
                    run: 0,
                },
            );
        }
        b'#' => {
            s += count_inc(
                record,
                State {
                    symbol_index: symbol_index + 1,
                    count_index,
                    run: run + 1,
                },
            );
        }
        b'?' => {
            let (dot_valid, hash_valid) = match (run, count_index) {
                (0, _) => {
                    // starting a new run
                    (true, true)
                }
                (run, count_index) => {
                    let count = record.count(count_index);
                    assert!(run <= count);
                    // finish run
                    let dot = run == count;
                    // continue run
                    let hash = run < count;
                    (dot, hash)
                }
            };

            if hash_valid {
                record.symbols[symbol_index] = b'#';
                s += count_inc(
                    record,
                    State {
                        symbol_index: symbol_index + 1,
                        count_index,
                        run: run + 1,
                    },
                );
            }
            if dot_valid {
                record.symbols[symbol_index] = b'.';
                let count_index = if run == 0 {
                    count_index
                } else {
                    count_index + 1
                };
                s += count_inc(
                    record,
                    State {
                        symbol_index: symbol_index + 1,
                        count_index,
                        run: 0,
                    },
                );
            }
            record.symbols[symbol_index] = b'?';
        }
        _ => panic!(),
    }

    record.cache.insert(hash_key, s);
    s
}

const REPEAT: usize = 5;

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let lines = input
        .lines()
        .map(|l| {
            let (symbols, counts) = l.split_by(b' ');
            // let symbols = vec![symbols.to_string(); REPEAT].join("?");
            let symbols = symbols.as_bytes().to_vec();
            let counts = counts.split(",").map(|c| c.to_u64()).collect_vec();
            // .repeat(REPEAT);

            Record {
                symbols,
                counts,
                result: None,
                multiplier: 0,
                cache: Default::default(),
            }
            .normalize(REPEAT)
        })
        .collect_vec();
    let ret = lines.into_iter().progress_with_style(
        ProgressStyle::with_template(
            "elapsed:[{elapsed_precise}] rem:[{eta_precise}] [{per_sec}] {bar:40.cyan/blue} {pos:>7}/{len:7} {msg}",
        )
            .unwrap(),
    ).map(|mut r| {
        match r.result {
            Some(r) => r,
            None => {
                // println!("{} {:?}", String::from_utf8_lossy(&r.symbols), r.counts);
                // println!("{}", String::from_utf8_lossy(&r.symbols));
                let c = count_inc(&mut r, State::default()) * r.multiplier;
                // println!("{c}");
                c
            }
        }
    })
    .sum::<u64>();
    println!("{ret}");
    Ok(())
}
// 1835248844160 too low
// 1909291258644
