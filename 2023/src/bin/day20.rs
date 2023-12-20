use aoc2023::Map;
use itertools::Itertools;
use std::collections::VecDeque;

#[derive(Clone, Debug)]
enum Module {
    FlipFlop {
        on: bool,
        outputs: Vec<String>,
    },
    Conjunction {
        inputs: Map<String, Pulse>,
        outputs: Vec<String>,
    },
    Broadcaster {
        outputs: Vec<String>,
    },
}

impl Module {
    fn update(&mut self, signal: Signal, signals: &mut VecDeque<Signal>) {
        match self {
            Module::FlipFlop { on, outputs } => {
                if matches!(signal.pulse, Pulse::Low) {
                    let pulse = match *on {
                        true => Pulse::Low,
                        false => Pulse::High,
                    };
                    *on = !*on;
                    for output in outputs {
                        signals.push_back(Signal {
                            src: signal.dest.clone(),
                            dest: output.clone(),
                            pulse,
                        });
                    }
                }
            }
            Module::Conjunction { inputs, outputs } => {
                *inputs.get_mut(&signal.src).unwrap() = signal.pulse;
                let pulse = if inputs.values().all(|p| p.is_high()) {
                    Pulse::Low
                } else {
                    Pulse::High
                };
                for output in outputs {
                    signals.push_back(Signal {
                        src: signal.dest.clone(),
                        dest: output.clone(),
                        pulse,
                    });
                }
            }
            _ => panic!(),
        }
    }
}

#[derive(Copy, Clone, Debug, Default)]
enum Pulse {
    #[default]
    Low,
    High,
}

impl Pulse {
    fn is_high(&self) -> bool {
        matches!(self, Pulse::High)
    }
    fn is_low(&self) -> bool {
        !self.is_high()
    }
}

#[derive(Debug)]
struct Signal {
    pulse: Pulse,
    src: String,
    dest: String,
}

#[derive(Debug, Default)]
struct Counter {
    low: u64,
    high: u64,
}

impl Counter {
    fn update(&mut self, pulse: Pulse) {
        match pulse {
            Pulse::Low => self.low += 1,
            Pulse::High => self.high += 1,
        }
    }
}

struct State {
    modules: Map<String, Module>,
}

fn propagate_button(modules: &mut Map<String, Module>, counter: &mut Counter) {
    counter.low += 1;

    let mut signals = VecDeque::new();
    if let Module::Broadcaster { outputs } = modules.get("broadcaster").unwrap() {
        for output in outputs {
            signals.push_back(Signal {
                pulse: Pulse::Low,
                src: "broadcaster".to_string(),
                dest: output.to_string(),
            });
        }
    } else {
        panic!();
    }

    while let Some(signal) = signals.pop_front() {
        counter.update(signal.pulse);

        if let Some(dest) = modules.get_mut(&signal.dest) {
            dest.update(signal, &mut signals);
        }
    }
}

fn propagate_button_cycle(mut modules: Map<String, Module>, start: &str) -> u64 {
    let mut buttons = 0;
    loop {
        buttons += 1;
        let mut signals = VecDeque::new();
        if let Module::Broadcaster { outputs } = modules.get("broadcaster").unwrap() {
            for output in outputs {
                if output == start {
                    signals.push_back(Signal {
                        pulse: Pulse::Low,
                        src: "broadcaster".to_string(),
                        dest: output.to_string(),
                    });
                }
            }
        } else {
            panic!();
        }

        while let Some(signal) = signals.pop_front() {
            if signal.pulse.is_high() && signal.dest == "hb" {
                return buttons;
            }

            if let Some(dest) = modules.get_mut(&signal.dest) {
                dest.update(signal, &mut signals);
            }
        }
    }
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let mut modules = Map::default();
    for line in input.lines() {
        let (module, outputs) = line.split_once(" -> ").unwrap();
        let outputs = outputs.split(", ").map(|s| s.to_string()).collect_vec();

        let (name, module) = match module {
            "broadcaster" => ("broadcaster", Module::Broadcaster { outputs }),
            n if n.starts_with("%") => (&n[1..], Module::FlipFlop { on: false, outputs }),
            n if n.starts_with("&") => (
                &n[1..],
                Module::Conjunction {
                    inputs: Default::default(),
                    outputs,
                },
            ),
            _ => panic!(),
        };
        let name = name.to_string();
        modules.insert(name, module);
    }
    for (name, module) in modules.clone() {
        let outputs = match module {
            Module::FlipFlop { outputs, .. } => outputs,
            Module::Conjunction { outputs, .. } => outputs,
            Module::Broadcaster { outputs } => outputs,
        };
        for output in outputs {
            if let Some(Module::Conjunction { inputs, .. }) = modules.get_mut(&output) {
                inputs.insert(name.clone(), Pulse::Low);
            }
        }
    }
    let presses_a = propagate_button_cycle(modules.clone(), "nd");
    let presses_b = propagate_button_cycle(modules.clone(), "mc");
    let presses_c = propagate_button_cycle(modules.clone(), "lf");
    let presses_d = propagate_button_cycle(modules.clone(), "fx");
    println!("{}", presses_a * presses_b * presses_c * presses_d);

    Ok(())
}
