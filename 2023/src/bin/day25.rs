use itertools::Itertools;
use pathfinding::prelude::connected_components;

use aoc2023::Map;

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;

    let to_break = vec![("lkf", "scf"), ("zxb", "zkv"), ("pgl", "mtl")];

    let mut edges: Map<String, Vec<String>> = Map::default();
    for line in input.lines() {
        let (src, targets) = line.split_once(": ").unwrap();
        let src = src.to_string();
        // lkf <-> scf
        // zxb <-> zkv
        // pgl <-> mtl
        for target in targets.split(" ").map(|t| t.trim().to_string()) {
            let mut add = true;
            for (a, b) in &to_break {
                if (*a, *b) == (src.as_str(), target.as_str())
                    || (*a, *b) == (target.as_str(), src.as_str())
                {
                    add = false;
                    break;
                }
            }
            if add {
                edges.entry(src.clone()).or_default().push(target.clone());
            }
        }
    }
    // println!("graph {{");
    // for (s, targets) in edges.iter() {
    //     for t in targets {
    //         println!("{s} -- {t} [ labeltooltip=\"{s} to {t}\", label=\"{s} to {t}\", tooltip=\"{s} to {t}\" ]");
    //     }
    // }
    // println!("}}");

    let nodes = edges.keys().cloned().collect_vec();
    let components =
        connected_components(&nodes, |node| edges.get(node).cloned().unwrap_or_default());
    println!("{}", components.len());
    let ret = components[0].len() * components[1].len();
    println!("{ret}");

    Ok(())
}
