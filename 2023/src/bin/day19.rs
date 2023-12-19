use itertools::Itertools;
use rayon::prelude::*;

use aoc2023::{Map, StrExt};

#[derive(Debug)]
enum Action {
    Reject,
    Accept,
    MoveToWorkflow(String),
}

#[derive(Debug)]
struct Rule {
    part: char,
    value: u64,
    less: bool,
    action: Action,
}

#[derive(Debug)]
struct Workflow {
    rules: Vec<Rule>,
    final_action: Action,
}

fn parse_action(input: &str) -> Action {
    match input {
        "R" => Action::Reject,
        "A" => Action::Accept,
        _ => Action::MoveToWorkflow(input.to_string()),
    }
}

#[derive(Debug)]
struct Part {
    items: Map<char, u64>,
}

impl Part {
    fn rating(&self) -> u64 {
        self.items.values().sum()
    }
}

// XMAS

#[derive(Debug)]
enum Node {
    Accept,
    Reject,
    Condition {
        part: char,
        less: bool,
        value: u64,
        left: Box<Node>,
        right: Box<Node>,
    },
}

#[derive(Copy, Clone, Debug)]
struct Bounds {
    min: u64,
    max: u64,
}

impl Bounds {
    fn count(&self) -> u64 {
        ((self.max - self.min) + 1) as u64
    }
    fn is_valid(&self) -> bool {
        self.min <= self.max
    }

    fn apply_bound(&self, value: u64, less: bool, negate: bool) -> Self {
        if less {
            if !negate {
                Self {
                    min: self.min,
                    max: value - 1,
                }
            } else {
                Self {
                    min: value,
                    max: self.max,
                }
            }
        } else {
            if !negate {
                Self {
                    min: value + 1,
                    max: self.max,
                }
            } else {
                Self {
                    min: self.min,
                    max: value,
                }
            }
        }
    }
}

#[derive(Copy, Clone, Debug)]
struct Combination {
    x: Bounds,
    m: Bounds,
    a: Bounds,
    s: Bounds,
}

impl Combination {
    fn apply_bound(mut self, part: char, value: u64, less: bool, negate: bool) -> Option<Self> {
        let bounds = match part {
            'x' => &mut self.x,
            'm' => &mut self.m,
            'a' => &mut self.a,
            's' => &mut self.s,
            _ => panic!(),
        };
        *bounds = bounds.apply_bound(value, less, negate);
        if bounds.is_valid() {
            Some(self)
        } else {
            None
        }
    }
    fn combinations(&self) -> u64 {
        self.x.count() * self.m.count() * self.a.count() * self.s.count()
    }
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let mut workflows = Map::default();

    let mut line_it = input.lines();
    for line in &mut line_it {
        if line.is_empty() {
            break;
        }
        let line = &line[..line.len() - 1];
        let (name, rest) = line.split_by(b'{');
        let mut rule_it = rest.split(",");
        let mut final_action = None;
        let mut rules = vec![];
        while let Some(rule) = rule_it.next() {
            if rule.contains(':') {
                let (rule, action) = rule.split_by(b':');
                let action = parse_action(action);
                let part = rule.chars().next().unwrap();
                let less = rule.as_bytes()[1] == b'<';
                let value = rule[2..].to_u64();
                rules.push(Rule {
                    part,
                    value,
                    less,
                    action,
                });
            } else {
                final_action = Some(parse_action(rule));
                break;
            }
        }
        workflows.insert(
            name.to_string(),
            Workflow {
                rules,
                final_action: final_action.unwrap(),
            },
        );
    }

    let node = build_tree(&workflows, workflows.get("in").unwrap(), 0);
    let start = Combination {
        x: Bounds { min: 1, max: 4000 },
        m: Bounds { min: 1, max: 4000 },
        a: Bounds { min: 1, max: 4000 },
        s: Bounds { min: 1, max: 4000 },
    };
    let mut combinations = eval(&node, start);
    println!("{combinations}");

    Ok(())
}

fn eval(node: &Node, mut item: Combination) -> u64 {
    match node {
        Node::Accept => item.combinations(),
        Node::Reject => 0,
        Node::Condition {
            value,
            part,
            less,
            left,
            right,
        } => {
            let mut sum = 0;
            if let Some(item) = item.apply_bound(*part, *value, *less, false) {
                sum += eval(&left, item);
            }
            if let Some(item) = item.apply_bound(*part, *value, *less, true) {
                sum += eval(&right, item);
            }
            sum
        }
    }
}

fn build_tree(
    workflows: &Map<String, Workflow>,
    mut workflow: &Workflow,
    mut index: usize,
) -> Node {
    let (rule, action) = if index >= workflow.rules.len() {
        (None, &workflow.final_action)
    } else {
        (Some(&workflow.rules[index]), &workflow.rules[index].action)
    };
    if let Some(rule) = rule {
        let left = Box::new(match &rule.action {
            Action::Accept => Node::Accept,
            Action::Reject => Node::Reject,
            Action::MoveToWorkflow(wf) => {
                build_tree(workflows, workflows.get(wf.as_str()).unwrap(), 0)
            }
        });
        let right = Box::new(build_tree(workflows, workflow, index + 1));

        return Node::Condition {
            part: rule.part,
            less: rule.less,
            value: rule.value,
            left,
            right,
        };
    }
    match action {
        Action::Accept => Node::Accept,
        Action::Reject => Node::Reject,
        Action::MoveToWorkflow(wf) => build_tree(workflows, workflows.get(wf.as_str()).unwrap(), 0),
    }
}

// fn part1() {
//     let parts = line_it
//         .map(|line| {
//             let line = &line[1..line.len() - 1];
//             let items = line
//                 .split(",")
//                 .map(|item| {
//                     let (name, value) = item.split_by(b'=');
//                     let value = value.to_u64();
//                     let name = name.chars().next().unwrap();
//                     (name, value)
//                 })
//                 .collect();
//             Part { items }
//         })
//         .collect_vec();
//     let ret = parts
//         // .into_par_iter()
//         .into_iter()
//         .filter(|p| is_accepted(&workflows, p))
//         .map(|p| p.rating())
//         .sum::<u64>();
//     println!("{ret}");
// }

fn is_accepted(workflows: &Map<String, Workflow>, part: &Part) -> bool {
    let mut workflow = workflows.get("in").unwrap();
    let mut index = 0;

    loop {
        let (rule, action) = if index >= workflow.rules.len() {
            (None, &workflow.final_action)
        } else {
            (Some(&workflow.rules[index]), &workflow.rules[index].action)
        };
        if let Some(rule) = rule {
            let matched = match rule.less {
                true => part.items[&rule.part] < rule.value,
                false => part.items[&rule.part] > rule.value,
            };
            if !matched {
                index += 1;
                continue;
            }
        }
        match action {
            Action::Accept => return true,
            Action::Reject => return false,
            Action::MoveToWorkflow(wf) => {
                workflow = workflows.get(wf.as_str()).unwrap();
                index = 0;
            }
        }
    }
}
