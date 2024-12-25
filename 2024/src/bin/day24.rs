use aoc2024::{Map, StrExt};
use std::cell::LazyCell;
use std::ops::{BitOr, BitXor};
use std::sync::atomic::{AtomicU64, Ordering};

#[derive(Copy, Clone, Debug, Eq, PartialEq, Hash)]
struct Gate<'a> {
    left: &'a str,
    right: &'a str,
    op: &'a str,
}

impl<'a> Gate<'a> {
    fn new(left: &'a str, right: &'a str, op: &'a str) -> Self {
        Gate {
            left: if left < right { left } else { right },
            right: if left < right { right } else { left },
            op,
        }
    }
}

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let mut wires: Map<&str, bool> = Map::default();
    let mut lines = file.lines();
    for line in &mut lines {
        if line.is_empty() {
            break;
        }
        let (name, value) = line.split_once(": ").unwrap();
        let value = value == "1";
        wires.insert(name, value);
    }

    let mut gates = Map::default();
    for line in lines {
        let (start, target) = line.split_once(" -> ").unwrap();
        let [left, op, right] = start.splitn(3, " ").collect::<Vec<_>>().try_into().unwrap();
        gates.insert(Gate::new(left, right, op), target);
    }

    // let mut file = std::fs::File::create("graph.dot")?;
    // writeln!(file, "digraph {{")?;
    // for gate in &gates {
    //     writeln!(
    //         file,
    //         "{} -> {} [label=\"{}\"]",
    //         gate.left, gate.target, gate.op
    //     )?;
    //     writeln!(
    //         file,
    //         "{} -> {} [label=\"{}\"]",
    //         gate.right, gate.target, gate.op
    //     )?;
    // }
    // writeln!(file, "}}")?;

    let mut replaced = vec![];
    swap_target(&mut gates, "mvb", "z08", &mut replaced);
    swap_target(&mut gates, "rds", "jss", &mut replaced);
    swap_target(&mut gates, "wss", "z18", &mut replaced);
    swap_target(&mut gates, "bmn", "z23", &mut replaced);
    find(gates, 0, "c0", vec![]);
    replaced.sort();
    println!("{}", replaced.join(","));

    Ok(())
}

// x18 AND y18 -> z18
// x18, y18 -> wrong
// sjd XOR mcr -> mvb SWAP mcr AND sjd -> z08

static MAX_BIT: AtomicU64 = AtomicU64::new(0);

fn find<'a>(
    mut gates: Map<Gate<'a>, &'a str>,
    bit: u64,
    c: &'a str,
    mut replaced: Vec<String>,
) -> bool {
    println!("{bit}");
    if bit > MAX_BIT.load(Ordering::Relaxed) {
        MAX_BIT.store(bit, Ordering::Relaxed);
        // println!("{bit}");
    }
    if bit == 46 {
        assert_eq!(replaced.len(), 8);
        replaced.sort();
        println!("{}", replaced.join(","));
        return true;
    }
    if replaced.len() > 8 {
        return false;
    }
    let x = format!("x{bit:02}");
    let y = format!("y{bit:02}");
    let c_next = if bit == 45 {
        assert_eq!(c, "z45");
        return true;
    } else if bit == 0 {
        let a = gates[&Gate::new(&x, &y, "XOR")];
        let b = gates[&Gate::new(&x, &y, "AND")];
        assert_eq!(a, &format!("z{bit:02}"));
        b
    } else {
        let a = gates[&Gate::new(&x, &y, "XOR")];
        let b = gates[&Gate::new(&x, &y, "AND")];
        let z = gates[&Gate::new(a, &c, "XOR")];
        // let (a, b, gate) = loop {
        //     let a = gates[&Gate::new(&x, &y, "XOR")];
        //     let b = gates[&Gate::new(&x, &y, "AND")];
        // if let Some(gate) = gates.get(&Gate::new(a, &c, "XOR")) {
        //     break (a, b, *gate);
        // } else {
        // let targets = targets(&gates);
        // for &target in &targets {
        //     if a != target {
        //         let mut replaced2 = replaced.clone();
        //         swap_target(&mut gates, a, target, &mut replaced2);
        //         if find(gates.clone(), bit, c, replaced2) {
        //             return true;
        //         }
        //         swap_target(&mut gates, a, target, &mut replaced);
        //     }
        // }
        // for &target in &targets {
        //     if target != b {
        //         let mut replaced2 = replaced.clone();
        //         swap_target(&mut gates, b, target, &mut replaced2);
        //         if find(gates.clone(), bit, c, replaced2) {
        //             return true;
        //         }
        //         swap_target(&mut gates, b, target, &mut replaced);
        //     }
        // }
        // }
        // };
        let expected_z = format!("z{bit:02}");
        assert_eq!(z, expected_z);
        // if expected_z != z {
        //     swap_target(&mut gates, z, &expected_z, &mut replaced);
        // }
        let d = gates[&Gate::new(a, &c, "AND")];
        gates[&Gate::new(d, b, "OR")]
    };
    find(gates, bit + 1, c_next, replaced)
}

fn targets<'a>(targets: &Map<Gate<'a>, &'a str>) -> Vec<&'a str> {
    targets.values().copied().collect()
}

fn swap_target<'a, 'b>(
    gates: &mut Map<Gate<'a>, &'a str>,
    a: &'a str,
    b: &'b str,
    replaced: &mut Vec<String>,
) {
    println!("swapping {a} and {b}");
    assert_ne!(a, b);
    let items: Vec<_> = gates
        .iter()
        .filter(|(gate, t)| **t == a || **t == b)
        .map(|(g, t)| (*g, *t))
        .collect();
    assert_eq!(items.len(), 2);
    replaced.push(a.to_string());
    replaced.push(b.to_string());
    gates.insert(items[0].0, items[1].1);
    gates.insert(items[1].0, items[0].1);
}

// fn part1<'a>(mut wires: Map<&'a str, bool>, mut gates: Vec<Gate<'a>>) {
//     while !gates.is_empty() {
//         gates.retain(|g| {
//             let Some(&val_l) = wires.get(g.left) else {
//                 return true;
//             };
//             let Some(&val_r) = wires.get(g.right) else {
//                 return true;
//             };
//
//             let res = match g.op {
//                 "AND" => val_l && val_r,
//                 "OR" => val_l || val_r,
//                 "XOR" => val_l.bitxor(val_r),
//                 _ => unreachable!(),
//             };
//             wires.insert(g.target, res);
//
//             false
//         })
//     }
//     println!("{wires:?}");
//     let mut res = 0u64;
//     for (wire, bit) in wires {
//         if bit {
//             if let Some(rest) = wire.strip_prefix('z') {
//                 let index = rest.to_u64();
//                 res = res.bitor(1 << index);
//             }
//         }
//     }
//     println!("{res}");
// }
