use aoc2024::StrExt;

#[derive(Copy, Clone, Debug)]
enum Operator {
    Add,
    Multiply,
    Concatenate,
}

#[derive(Debug)]
struct Equation {
    nums: Vec<u64>,
    operators: Vec<Operator>,
}

impl Equation {
    fn new(nums: Vec<u64>, operators: Vec<Operator>) -> Self {
        assert_eq!(operators.len(), nums.len() - 1);
        Self { nums, operators }
    }

    fn evaluate(&self) -> u64 {
        let mut nums = self.nums.iter().peekable();
        let mut ops = self.operators.iter();
        let mut num = *nums.next().unwrap();

        while nums.peek().is_some() {
            let op = ops.next().unwrap();
            let next = nums.next().unwrap();
            match op {
                Operator::Add => {
                    num = num + *next;
                }
                Operator::Multiply => {
                    num = num * *next;
                }
                Operator::Concatenate => num = num * 10u64.pow(num_digits(*next)) + *next,
            }
        }
        num
    }
}

// https://stackoverflow.com/a/69298721/1107768
fn num_digits(value: u64) -> u32 {
    value.checked_ilog10().unwrap_or(0) + 1
}

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;

    let res = file
        .lines()
        .filter_map(|line| {
            let (target, line) = line.split_once(':').unwrap();
            let target = target.to_u64();
            let atoms = line.split_nums_whitespace::<u64>();
            if generate_equations(atoms)
                .into_iter()
                .any(|eq| eq.evaluate() == target)
            {
                Some(target)
            } else {
                None
            }
        })
        .sum::<u64>();
    println!("{res}");

    Ok(())
}

fn generate_equations(nums: Vec<u64>) -> Vec<Equation> {
    let mut equations = vec![];
    fill_equations(&mut equations, &nums, &mut vec![]);
    // println!("{equations:?}");
    equations
}

fn fill_equations(equations: &mut Vec<Equation>, nums: &[u64], operators: &mut Vec<Operator>) {
    if operators.len() == nums.len() - 1 {
        equations.push(Equation::new(nums.to_vec(), operators.clone()));
        return;
    }
    operators.push(Operator::Add);
    fill_equations(equations, nums, operators);
    operators.pop();
    operators.push(Operator::Multiply);
    fill_equations(equations, nums, operators);
    operators.pop();
    operators.push(Operator::Concatenate);
    fill_equations(equations, nums, operators);
    operators.pop();
}
