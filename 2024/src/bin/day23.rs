use aoc2024::{Map, Set};
use itertools::Itertools;

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let mut graph: Map<&str, Set<&str>> = Map::default();
    let mut nodes = Set::default();
    for line in file.lines() {
        let items: Vec<_> = line.split('-').collect();
        let a = items[0];
        let b = items[1];
        graph.entry(a).or_default().insert(b);
        graph.entry(b).or_default().insert(a);
        nodes.insert(a);
        nodes.insert(b);
    }
    bron_kerbosch(&graph, Set::default(), nodes, Set::default());

    Ok(())
}

fn bron_kerbosch<'a>(
    graph: &Map<&'a str, Set<&'a str>>,
    r: Set<&'a str>,
    p: Set<&'a str>,
    mut x: Set<&'a str>,
) {
    if p.is_empty() && x.is_empty() {
        let mut res: Vec<&str> = r.into_iter().collect();
        res.sort_unstable();
        println!("{}", res.join(","));
        return;
    }
    let mut p2 = p.clone();
    for vertex in p {
        let neighbours: Set<&str> = graph[vertex].clone();
        let mut r = r.clone();
        r.insert(vertex);
        let p_tmp = p2
            .intersection(&neighbours)
            .into_iter()
            .map(|s| *s)
            .collect();
        let x_tmp = x
            .intersection(&neighbours)
            .into_iter()
            .map(|s| *s)
            .collect();
        bron_kerbosch(graph, r, p_tmp, x_tmp);
        p2.remove(&vertex);
        x.insert(vertex);
    }

    // if P and X are both empty then
    // report R as a maximal clique
    // for each vertex v in P do
    // BronKerbosch1(R ⋃ {v}, P ⋂ N(v), X ⋂ N(v))
    // P := P \ {v}
    // X := X ⋃ {v}
}

fn is_connected(graph: &Set<(&str, &str)>, a: &str, b: &str) -> bool {
    graph.contains(&(a, b)) || graph.contains(&(b, a))
}

fn part1(file: &str) {
    let graph: Set<(&str, &str)> = file
        .lines()
        .map(|l| {
            let items: Vec<_> = l.split('-').collect();
            (items[0], items[1])
        })
        .collect();
    let nodes: Set<&str> = graph.iter().map(|(a, b)| [*a, *b]).flatten().collect();

    let mut triples: Set<Vec<&str>> = Set::default();
    for &n0 in &nodes {
        for &n1 in &nodes {
            if n0 == n1 {
                continue;
            }
            for &n2 in &nodes {
                if n0 == n2 {
                    continue;
                }
                if is_connected(&graph, n0, n1)
                    && is_connected(&graph, n1, n2)
                    && is_connected(&graph, n0, n2)
                {
                    let mut triple = vec![n0, n1, n2];
                    triple.sort_unstable();
                    triples.insert(triple);
                }
            }
        }
    }

    println!(
        "{}",
        triples
            .into_iter()
            .filter(|s| s.iter().any(|n| n.starts_with('t')))
            .count()
    );
}
