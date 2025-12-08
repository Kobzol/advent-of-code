use aoc2025::StrExt;
use aoc2025::vector::Position3D;
use union_find::{QuickUnionUf, UnionByRankSize, UnionFind};

#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
struct Box {
    index: usize,
    pos: Position3D,
}

fn main() -> anyhow::Result<()> {
    let data = std::fs::read_to_string("input.txt")?;
    let mut positions = data
        .lines()
        .enumerate()
        .map(|(index, line)| {
            let nums = line.split_nums_by::<i64>(',');
            Box {
                index,
                pos: Position3D(nums[0], nums[1], nums[2]),
            }
        })
        .collect::<Vec<_>>();

    let mut pairs: Vec<(Box, Box)> = positions
        .iter()
        .enumerate()
        .flat_map(|(i0, p0)| positions[i0 + 1..].iter().map(|p1| (*p0, *p1)))
        .collect();
    pairs.sort_by(|a, b| {
        a.0.pos
            .euclidean_squared(a.1.pos)
            .cmp(&b.0.pos.euclidean_squared(b.1.pos))
    });

    let mut result = 0;
    let mut uf: QuickUnionUf<UnionByRankSize> = QuickUnionUf::new(positions.len());
    for (p0, p1) in pairs.iter() {
        if uf.find(p0.index) == uf.find(p1.index) {
            continue;
        }
        uf.union(p0.index, p1.index);
        result = p0.pos.0 * p1.pos.0;
    }
    println!("{result}");

    // let mut circuits: Map<usize, Vec<Box>> = Map::default();
    // for pos in &positions {
    //     let repr = uf.find(pos.index);
    //     circuits.entry(repr).or_default().push(*pos);
    // }
    // let mut circuits: Vec<Vec<Box>> = circuits.into_values().collect();
    // circuits.sort_by(|a, b| a.len().cmp(&b.len()).reverse());
    // for c in &circuits {
    //     println!("{}: {c:?}", c.len());
    // }
    // let result = circuits
    //     .iter()
    //     .map(|c| c.len())
    //     .take(3)
    //     .fold(1, |a, b| a * b);
    // println!("Circuit len: {}", circuits.len());
    // assert_eq!(
    //     circuits.iter().map(|c| c.len()).sum::<usize>(),
    //     positions.len()
    // );
    // println!("{result}");

    Ok(())
}
