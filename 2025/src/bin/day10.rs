use aoc2025::StrExt;
use pathfinding::prelude::dfs;
use z3::Optimize;
use z3::ast::Int;

#[derive(Default, Debug, PartialEq, Eq, Hash, Clone)]
struct State {
    lights: Vec<bool>,
}

impl State {
    fn next(&self, button: &Button) -> Self {
        let mut lights = self.lights.clone();
        for &index in &button.0 {
            lights[index as usize] = !lights[index as usize];
        }
        Self { lights }
    }
}

#[derive(Default, Debug, PartialEq, Eq, Hash, Clone)]
struct Joltage {
    values: Vec<u32>,
}

impl Joltage {
    fn next(&self, button: &Button) -> Self {
        let mut lights = self.values.clone();
        for &index in &button.0 {
            lights[index as usize] += 1;
        }
        Self { values: lights }
    }
}

#[derive(Debug)]
struct Button(Vec<u8>);

fn main() -> anyhow::Result<()> {
    let data = std::fs::read_to_string("input.txt")?;

    let sum = data
        .lines()
        .map(|line| {
            let mut split = line.split(" ");
            let state = split.next().unwrap();
            let state = &state[1..state.len() - 1];
            let _state = State {
                lights: state.as_bytes().iter().map(|&b| b == b'#').collect(),
            };
            let mut buttons = vec![];
            let mut joltage = None;
            while let Some(item) = split.next() {
                let value = &item[1..item.len() - 1];
                if item.starts_with('(') {
                    buttons.push(Button(value.split_nums_by(',')));
                } else {
                    assert!(item.starts_with('{'));
                    joltage = Some(Joltage {
                        values: value.split_nums_by(','),
                    });
                }
            }
            (joltage.unwrap(), buttons)
        })
        .map(|(target, mut buttons)| {
            let solver = Optimize::new();

            let mut target_presses = vec![vec![]; target.values.len()];
            let mut button_presses = vec![];
            for (index, button) in buttons.iter().enumerate() {
                let press = Int::new_const(format!("button-{index}"));
                for &b in &button.0 {
                    target_presses[b as usize].push(press.clone());
                }
                solver.assert(&press.ge(0));
                button_presses.push(press);
            }
            for (index, position) in target_presses.iter().enumerate() {
                if position.is_empty() {
                    panic!();
                }
                let mut expr = None;
                for press in position.iter() {
                    match expr {
                        None => {
                            expr = Some(press.clone());
                        }
                        Some(e) => {
                            expr = Some(e + press);
                        }
                    }
                }
                if let Some(expr) = expr {
                    solver.assert(&expr.eq(target.values[index]));
                } else {
                    panic!();
                }
            }

            let mut press_sum = button_presses[0].clone();
            for press in button_presses.iter().skip(1) {
                press_sum = press_sum + press;
            }

            solver.minimize(&press_sum);
            solver.check(&[]);
            let model = solver.get_model().unwrap();
            let presses = button_presses
                .iter()
                .map(|b| dbg!(model.eval(b, true).unwrap().as_u64().unwrap() as usize))
                .collect::<Vec<_>>();
            let mut state = Joltage {
                values: vec![0; target.values.len()],
            };
            for (p, button) in presses.iter().zip(&buttons) {
                for _ in 0..*p {
                    state = state.next(button);
                }
            }
            assert_eq!(state, target);

            return dbg!(presses.into_iter().sum());

            // for solution in solver.solutions(&button_presses, true) {
            //     let solution: Vec<u64> = solution
            //         .iter()
            //         .map(Int::as_u64)
            //         .map(Option::unwrap)
            //         .collect();
            //     return dbg!(solution.into_iter().map(|v| v as usize).sum());
            // }

            buttons.sort_by(|a, b| a.0.len().cmp(&b.0.len()).reverse());

            fn dist(a: &Joltage, b: &Joltage) -> u32 {
                a.values
                    .iter()
                    .zip(&b.values)
                    .map(|(a, b)| a.abs_diff(*b))
                    .sum::<u32>()
            }

            let len = dfs(
                Joltage {
                    values: vec![0; target.values.len()],
                },
                |s| {
                    if s.values.iter().zip(&target.values).any(|(a, b)| a > b) {
                        return vec![];
                    }

                    let mut next = vec![];
                    for button in &buttons {
                        let n = s.next(button);
                        // let dist = dist(&n, &target);
                        // next.push((n, dist));
                        next.push(n);
                    }
                    next
                },
                // |s| dist(s, &target),
                |s| *s == target,
            )
            .unwrap()
            // .0
            .len()
                - 1;
            dbg!(len)
        })
        .sum::<usize>();
    println!("{sum}");

    Ok(())
}
