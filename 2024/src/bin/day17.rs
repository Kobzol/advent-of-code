use aoc2024::StrExt;
use std::io::BufRead;
use std::ops::BitXor;
use z3::ast::Ast;
use z3::{ast, Config, Context, SatResult, Solver};

type Int = u64;

#[derive(Debug, Copy, Clone)]
enum Opcode {
    Adv,
    Bxl,
    Bst,
    Jnz,
    Bxc,
    Out,
    Bdv,
    Cdv,
}

#[derive(Debug, Copy, Clone)]
enum Operand {
    Literal(u8),
    Register(u8),
}

#[derive(Clone)]
struct Program {
    ip: usize,
    instructions: Vec<u8>,
    registers: [Int; 3],
}

impl Program {
    fn run(mut self) -> Vec<u8> {
        let mut output = vec![];
        while self.ip < self.instructions.len() {
            if let Some(out) = self.execute() {
                output.push(out);
            }
        }
        output
    }

    fn execute(&mut self) -> Option<u8> {
        let (opcode, operand) = self.decode();
        let operand_val = self.eval(operand);

        // println!(
        //     "IP[{}], {opcode:?} {operand:?}, {:?}",
        //     self.ip, self.registers
        // );

        match opcode {
            Opcode::Adv => {
                self.write_a(self.read_a() / 2u64.pow(operand_val as u32));
            }
            Opcode::Bxl => self.write_b(self.read_b().bitxor(&operand_val)),
            Opcode::Bst => {
                self.write_b(operand_val % 8);
            }
            Opcode::Jnz => {
                if self.read_a() != 0 {
                    self.ip = operand_val as usize;
                    return None;
                }
            }
            Opcode::Bxc => self.write_b(self.read_b().bitxor(&self.read_c())),
            Opcode::Out => {
                self.ip += 2;
                // println!("Outputting {}", operand_val % 8);
                return Some((operand_val % 8) as u8);
            }
            Opcode::Bdv => {
                self.write_b(self.read_a() / 2u64.pow(operand_val as u32));
            }
            Opcode::Cdv => {
                self.write_c(self.read_a() / 2u64.pow(operand_val as u32));
            }
        }
        self.ip += 2;
        None
    }

    fn decode(&self) -> (Opcode, Operand) {
        let opcode = match self.instructions[self.ip] {
            0 => Opcode::Adv,
            1 => Opcode::Bxl,
            2 => Opcode::Bst,
            3 => Opcode::Jnz,
            4 => Opcode::Bxc,
            5 => Opcode::Out,
            6 => Opcode::Bdv,
            7 => Opcode::Cdv,
            _ => panic!("Wrong opcode"),
        };
        let operand = match self.instructions[self.ip + 1] {
            v @ 0..=3 => Operand::Literal(v),
            v @ 4..=6 => Operand::Register(v - 4),
            _ => panic!("Wrong operand"),
        };
        (opcode, operand)
    }

    fn eval(&self, operand: Operand) -> Int {
        match operand {
            Operand::Literal(l) => l as Int,
            Operand::Register(r) => self.registers[r as usize] as Int,
        }
    }

    fn read_a(&self) -> Int {
        self.registers[0] as Int
    }
    fn read_b(&self) -> Int {
        self.registers[1] as Int
    }
    fn read_c(&self) -> Int {
        self.registers[2] as Int
    }

    fn write_a(&mut self, val: Int) {
        // println!("Writing {val} to A");
        self.registers[0] = val;
    }
    fn write_b(&mut self, val: Int) {
        // println!("Writing {val} to B");
        self.registers[1] = val;
    }
    fn write_c(&mut self, val: Int) {
        // println!("Writing {val} to C");
        self.registers[2] = val;
    }
}

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;

    let lines = file.lines();
    let registers = lines
        .clone()
        .take(3)
        .map(|l| l.split_once(": ").unwrap().1.to_u64() as Int)
        .collect::<Vec<_>>()
        .try_into()
        .unwrap();
    let instructions = lines
        .skip(4)
        .next()
        .unwrap()
        .split_once(": ")
        .unwrap()
        .1
        .replace(",", " ")
        .split_nums_whitespace::<u8>();

    let cfg = Config::new();
    let ctx = Context::new(&cfg);
    let solver = Solver::new(&ctx);

    let mut target = ast::BV::new_const(&ctx, "A", 64);
    // solver.assert(&target.bvult(&ast::BV::from_u64(&ctx, 37221334433268, 64)));

    let const0 = ast::BV::from_u64(&ctx, 0, 64);
    let const1 = ast::BV::from_u64(&ctx, 1, 64);
    let const2 = ast::BV::from_u64(&ctx, 2, 64);
    let const3 = ast::BV::from_u64(&ctx, 3, 64);
    let const8 = ast::BV::from_u64(&ctx, 8, 64);

    for (index, expected_out) in instructions.iter().enumerate() {
        let a = &target;
        let b = a.bvurem(&const8);
        let b = b.bvxor(&const2);

        // let b_minus_one = b.bvsub(&const1);
        let c = a.bvudiv(&const1.bvshl(&b));
        // println!("{c:?}");
        let b = b.bvxor(&const3);
        let b = b.bvxor(&c);
        let b = b.bvurem(&const8);

        let expected = ast::BV::from_u64(&ctx, *expected_out as u64, 64);
        solver.assert(&b._eq(&expected));
        target = target.bvudiv(&const8);
        // println!("t={target:?}, e={expected}");
    }
    solver.assert(&target._eq(&const0));

    let mut res = 0;
    while matches!(solver.check(), SatResult::Sat) {
        println!("SAT");
        let a = ast::BV::new_const(&ctx, "A", 64);
        res = solver
            .get_model()
            .unwrap()
            .eval(&a, true)
            .unwrap()
            .as_u64()
            .unwrap();

        solver.assert(&a.bvult(&ast::BV::from_u64(&ctx, res, 64)));
        println!("{res}");
    }

    let mut program = Program {
        ip: 0,
        instructions,
        registers,
    };
    program.registers[0] = res;
    println!("{:?}", program.instructions);
    println!("{:?}", program.run());
    return Ok(());

    let mut max_match = 0;
    for val in 8u64.pow(15).. {
        if is_copy(program.clone(), val, &mut max_match) {
            println!("{val}");
            break;
        }
        if val % 100000000 == 0 {
            println!("{val}");
        }
    }

    // println!(
    //     "{}",
    //     output
    //         .into_iter()
    //         .map(|v| v.to_string())
    //         .collect::<Vec<_>>()
    //         .join(",")
    // );

    Ok(())
}

fn is_copy(mut program: Program, initial_a: Int, max_match: &mut usize) -> bool {
    program.registers[0] = initial_a;

    let mut index = 0;
    while program.ip < program.instructions.len() {
        if let Some(output) = program.execute() {
            if index >= program.instructions.len() || output != program.instructions[index] {
                return false;
            }
            index += 1;
            if index > *max_match {
                *max_match = index;
                println!("{initial_a}: {:?}", &program.instructions[..index]);
                // std::io::stdin()
                //     .lock()
                //     .read_line(&mut String::new())
                //     .unwrap();
            }
        }
    }
    index == program.instructions.len()
}
// 614403000000
// 17868070400348700116 too high
// 9930333663003327988 too high
// 37222144523764 too high
// 37221334957556 wrong
// 37221334433268
