use aoc2023::Map;

#[derive(Debug)]
struct Node<'a> {
    left: &'a str,
    right: &'a str,
}

struct Directions<'a> {
    dirs: &'a str,
    index: usize,
}

impl<'a> Iterator for Directions<'a> {
    type Item = (u8, usize);

    fn next(&mut self) -> Option<Self::Item> {
        let char = self.dirs.as_bytes()[self.index];
        let index = self.index;
        self.index = (self.index + 1) % self.dirs.as_bytes().len();
        Some((char, index))
    }
}

// Taken from https://github.com/TheAlgorithms/Rust/blob/master/src/math/lcm_of_n_numbers.rs
pub fn lcm(nums: &[usize]) -> usize {
    if nums.len() == 1 {
        return nums[0];
    }
    let a = nums[0];
    let b = lcm(&nums[1..]);
    a * b / gcd_of_two_numbers(a, b)
}

fn gcd_of_two_numbers(a: usize, b: usize) -> usize {
    if b == 0 {
        return a;
    }
    gcd_of_two_numbers(b, a % b)
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let mut lines = input.lines();
    let directions = lines.next().unwrap();
    lines.next().unwrap();

    let mut node_map: Map<&str, Node> = Map::default();
    for line in lines {
        let (key, dirs) = line.split_once(" = ").unwrap();
        let dirs = dirs.trim();
        let dirs = &dirs[1..dirs.len() - 1];
        let (left, right) = dirs.split_once(", ").unwrap();

        node_map.insert(key.trim(), Node { left, right });
    }

    let mut nodes = node_map
        .keys()
        .filter(|k| k.ends_with("A"))
        .copied()
        .collect::<Vec<_>>();

    let multiples = nodes
        .into_iter()
        .map(|node| {
            let mut nodes = vec![node];
            let mut steps = 0usize;
            for dir in directions.chars().cycle() {
                nodes = match dir {
                    'L' => nodes.into_iter().map(|node| node_map[node].left).collect(),
                    'R' => nodes.into_iter().map(|node| node_map[node].right).collect(),
                    _ => panic!(),
                };
                steps += 1;
                if nodes.iter().all(|n| n.ends_with("Z")) {
                    break;
                }
            }
            steps
        })
        .collect::<Vec<_>>();
    // CVA -> KJZ (22357)
    // AAA -> ZZZ (20093)
    // LDA -> XLZ (16697)
    // VGA -> PQZ (20659)
    // LHA -> BKZ (14999)
    // RHA -> XNZ (17263)

    println!("{}", lcm(&multiples));

    Ok(())
}
// 40122189937608935807829251 too high
