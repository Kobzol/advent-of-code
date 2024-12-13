use aoc2024::StrExt;
use z3::ast::Ast;
use z3::{ast, Config, Context, SatResult, Solver};

fn parse(line: &str, prefix: &str) -> (u64, u64) {
    assert!(line.starts_with(prefix));
    let line = &line[prefix.len()..];
    let (x, y) = line.split_once(", ").unwrap();
    let x = x[2..].to_u64();
    let y = y[2..].to_u64();
    (x, y)
}

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let mut lines = file.lines();

    let mut tokens = 0;
    while let Some(button_a) = lines.next() {
        let btn_a = parse(button_a, "Button A: ");
        let btn_b = parse(lines.next().unwrap(), "Button B: ");
        let mut prize = parse(lines.next().unwrap(), "Prize: ");
        lines.next();

        prize.0 += 10000000000000;
        prize.1 += 10000000000000;
        println!("{btn_a:?} {btn_b:?} {prize:?}");
        tokens += solve(btn_a, btn_b, prize);
    }
    println!("{tokens}");

    Ok(())
}

fn solve(a: (u64, u64), b: (u64, u64), prize: (u64, u64)) -> u64 {
    let cfg = Config::new();
    let ctx = Context::new(&cfg);
    let solver = Solver::new(&ctx);

    let a_x = ast::Int::from_i64(&ctx, a.0 as i64);
    let a_y = ast::Int::from_i64(&ctx, a.1 as i64);

    let b_x = ast::Int::from_i64(&ctx, b.0 as i64);
    let b_y = ast::Int::from_i64(&ctx, b.1 as i64);

    let p_x = ast::Int::from_i64(&ctx, prize.0 as i64);
    let p_y = ast::Int::from_i64(&ctx, prize.1 as i64);

    let zero = ast::Int::from_i64(&ctx, 0);
    // let hundred = ast::Int::from_i64(&ctx, 100);
    let three = ast::Int::from_i64(&ctx, 3);

    let press_a = ast::Int::new_const(&ctx, "press_a");
    let press_b = ast::Int::new_const(&ctx, "press_b");

    solver.assert(&press_a.ge(&zero));
    // solver.assert(&press_a.le(&hundred));
    solver.assert(&press_b.ge(&zero));
    // solver.assert(&press_b.le(&hundred));

    solver.assert(&(a_x * &press_a + b_x * &press_b)._eq(&p_x));
    solver.assert(&(a_y * &press_a + b_y * &press_b)._eq(&p_y));

    let tokens = ast::Int::new_const(&ctx, "tokens");
    solver.assert(&tokens._eq(&(press_a * three + press_b)));

    match solver.check() {
        SatResult::Sat => solver
            .get_model()
            .unwrap()
            .eval(&tokens, true)
            .unwrap()
            .as_i64()
            .unwrap() as u64,
        _ => 0,
    }
}
