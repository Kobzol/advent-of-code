use std::fmt::{Debug, Formatter};

use itertools::Itertools;
use z3::ast::Ast;
use z3::{ast, Config, Context, SatResult, Solver};

use aoc2023::vector::Position3D;
use aoc2023::StrExt;

#[derive(Copy, Clone)]
struct Hailstone {
    position: Position3D,
    speed: Position3D,
}

impl Hailstone {
    fn start_2d(&self) -> (f64, f64) {
        (self.position.x() as f64, self.position.y() as f64)
    }
    fn end_2d(&self) -> (f64, f64) {
        let end = self.position + self.speed;
        (end.x() as f64, end.y() as f64)
    }
}

impl Debug for Hailstone {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{},{},{} @ {},{},{}",
            self.position.x(),
            self.position.y(),
            self.position.z(),
            self.speed.x(),
            self.speed.y(),
            self.speed.z()
        )
    }
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let hailstones = input
        .lines()
        .map(|line| {
            let (position, speed) = line.split_once(" @ ").unwrap();
            let position = position
                .split(", ")
                .map(|v| v.trim().to_i64())
                .collect_vec();
            let position = Position3D(position[0], position[1], position[2]);
            let speed = speed.split(", ").map(|v| v.trim().to_i64()).collect_vec();
            let speed = Position3D(speed[0], speed[1], speed[2]);
            Hailstone { position, speed }
        })
        .collect_vec();

    // let start = 7f64;
    // let end = 27f64;
    let start = 200000000000000f64;
    let end = 400000000000000f64;

    let cfg = Config::new();
    let ctx = Context::new(&cfg);
    let solver = Solver::new(&ctx);
    let zero = ast::Int::from_i64(&ctx, 0);
    let mut positions = vec![];

    for (index, hailstone) in hailstones.iter().enumerate() {
        let x = ast::Int::from_i64(&ctx, hailstone.position.x());
        let y = ast::Int::from_i64(&ctx, hailstone.position.y());
        let z = ast::Int::from_i64(&ctx, hailstone.position.z());
        let vx = ast::Int::from_i64(&ctx, hailstone.speed.x());
        let vy = ast::Int::from_i64(&ctx, hailstone.speed.y());
        let vz = ast::Int::from_i64(&ctx, hailstone.speed.z());

        let n = ast::Int::new_const(&ctx, format!("n_{index}"));
        solver.assert(&n.ge(&zero));

        let px = x + vx * n.clone();
        let py = y + vy * n.clone();
        let pz = z + vz * n.clone();
        positions.push((n, (px, py, pz)));
    }

    let xs = ast::Int::new_const(&ctx, "x_s");
    let ys = ast::Int::new_const(&ctx, "y_s");
    let zs = ast::Int::new_const(&ctx, "z_s");
    let vxs = ast::Int::new_const(&ctx, "vx_s");
    let vys = ast::Int::new_const(&ctx, "vy_s");
    let vzs = ast::Int::new_const(&ctx, "vz_s");

    let mut time_values = vec![];
    for (n, (x, y, z)) in positions.into_iter() {
        let px = xs.clone() + vxs.clone() * n.clone();
        let py = ys.clone() + vys.clone() * n.clone();
        let pz = zs.clone() + vzs.clone() * n.clone();
        solver.assert(&px._eq(&x));
        solver.assert(&py._eq(&y));
        solver.assert(&pz._eq(&z));
        time_values.push(n);
    }

    assert_eq!(solver.check(), SatResult::Sat);
    let model = solver.get_model().unwrap();
    let x_model = model.eval(&xs, true).unwrap().as_i64().unwrap();
    let y_model = model.eval(&ys, true).unwrap().as_i64().unwrap();
    let z_model = model.eval(&zs, true).unwrap().as_i64().unwrap();

    let vx_model = model.eval(&vxs, true).unwrap().as_i64().unwrap();
    let vy_model = model.eval(&vys, true).unwrap().as_i64().unwrap();
    let vz_model = model.eval(&vzs, true).unwrap().as_i64().unwrap();

    println!("pos={x_model}, {y_model}, {z_model}");
    println!("vel={vx_model}, {vy_model}, {vz_model}");

    for (n, hailstone) in time_values.iter().zip(hailstones) {
        let n = model.eval(n, true).unwrap().as_i64().unwrap();
        println!("{n}");
        let intersection_point_s = Position3D(
            x_model + vx_model * n,
            y_model + vy_model * n,
            z_model + vz_model * n,
        );
        let intersection_point_ray = hailstone.position + hailstone.speed * n;
        assert_eq!(intersection_point_s, intersection_point_ray);
    }

    let ret = x_model + y_model + z_model;
    println!("{ret}");

    // let mut intersections = 0;
    // for lines in hailstones.iter().combinations(2) {
    //     let a = lines[0];
    //     let b = lines[1];
    //
    //     let ray_a = LineInterval::ray(Line {
    //         start: a.start_2d().into(),
    //         end: a.end_2d().into(),
    //     });
    //
    //     let ray_b = LineInterval::ray(Line {
    //         start: b.start_2d().into(),
    //         end: b.end_2d().into(),
    //     });
    //     let intersection = ray_a.relate(&ray_b).unique_intersection();
    //     if let Some(intersection) = intersection {
    //         if intersection.x() >= start
    //             && intersection.x() <= end
    //             && intersection.y() >= start
    //             && intersection.y() <= end
    //         {
    //             intersections += 1;
    //         }
    //     }
    // }
    // println!("{intersections}");

    Ok(())
}
