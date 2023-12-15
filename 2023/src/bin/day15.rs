use aoc2023::StrExt;
use itertools::Itertools;

fn calculate_hash(input: &str) -> u64 {
    input.as_bytes().iter().fold(0, |mut acc, value| {
        acc += *value as u64;
        acc *= 17;
        acc %= 256;
        acc
    })
}

#[derive(Debug, Clone)]
enum Op {
    Set(u64),
    Remove,
}

#[derive(Debug, Clone)]
struct Step {
    label: String,
    op: Op,
}

#[derive(Debug, Clone)]
struct Lens {
    label: String,
    focal_length: u64,
}

impl Step {
    fn hash(&self) -> u64 {
        calculate_hash(&self.label)
    }
}

fn parse_step(input: &str) -> Step {
    if input.ends_with("-") {
        Step {
            label: input[..input.len() - 1].to_string(),
            op: Op::Remove,
        }
    } else {
        let (label, lens) = input.split_once("=").unwrap();
        Step {
            label: label.to_string(),
            op: Op::Set(lens.to_u64()),
        }
    }
}

#[derive(Default, Clone, Debug)]
struct Box {
    lenses: Vec<Lens>,
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let steps = input.split(",").map(parse_step).collect_vec();
    let mut boxes = vec![Box::default(); 256];
    for step in steps {
        let hash = step.hash() as usize;
        match step.op {
            Op::Set(focal_length) => {
                let existing = boxes[hash]
                    .lenses
                    .iter()
                    .position(|s| s.label == step.label);
                if let Some(pos) = existing {
                    boxes[hash].lenses[pos] = Lens {
                        label: step.label,
                        focal_length,
                    };
                } else {
                    boxes[hash].lenses.push(Lens {
                        label: step.label,
                        focal_length,
                    });
                }
            }
            Op::Remove => {
                boxes[hash].lenses.retain(|s| s.label != step.label);
            }
        }
    }
    let ret = boxes
        .into_iter()
        .enumerate()
        .flat_map(|(index, slot)| {
            slot.lenses
                .into_iter()
                .enumerate()
                .map(move |(slot_index, step)| {
                    (index as u64 + 1) * (slot_index as u64 + 1) * step.focal_length
                })
        })
        .sum::<u64>();
    println!("{ret}");

    Ok(())
}
