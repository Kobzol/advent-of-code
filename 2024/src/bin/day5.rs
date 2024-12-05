use aoc2024::StrExt;
use hashbrown::{HashMap, HashSet};
use itertools::Itertools;
use topological_sort::TopologicalSort;

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;

    let mut lines = file.lines();

    let mut precedence: HashMap<u32, HashSet<u32>> = HashMap::new();
    while let Some(line) = lines.next() {
        let line = line.trim();
        if line.is_empty() {
            break;
        }
        let nums = line.replace("|", " ").split_nums_whitespace::<u32>();
        precedence.entry(nums[0]).or_default().insert(nums[1]);
    }

    let res = lines
        .collect::<Vec<_>>()
        .into_iter()
        .map(|line| line.replace(",", " ").split_nums_whitespace::<u32>())
        // .progress()
        .filter(|nums| !is_ordered(nums, &precedence))
        .map(|nums| {
            let mut toposort = TopologicalSort::<u32>::new();
            for (&pre, post) in &precedence {
                for &val in post {
                    if nums.contains(&pre) && nums.contains(&val) {
                        toposort.add_dependency(pre, val);
                    }
                }
            }
            let mut result = vec![];
            loop {
                let items = toposort.pop_all();
                if items.is_empty() {
                    break;
                }
                result.extend(items);
            }
            result

            // let len = nums.len();
            // nums.into_iter()
            //     .permutations(len)
            //     .par_bridge()
            //     .find_any(|nums| is_ordered(nums, &precedence))
        })
        .map(|nums| nums[nums.len() / 2])
        .sum::<u32>();
    println!("{res}");

    Ok(())
}

fn is_ordered(nums: &[u32], precedence: &HashMap<u32, HashSet<u32>>) -> bool {
    let mut visited = HashSet::new();
    for &num in nums {
        if let Some(must_be_before) = precedence.get(&num) {
            if !must_be_before.is_disjoint(&visited) {
                return false;
            }
        }
        visited.insert(num);
    }
    true
}
