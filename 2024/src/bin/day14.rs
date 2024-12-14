use hashbrown::{HashMap, HashSet};
use aoc2024::StrExt;
use aoc2024::vector::Position2D;

#[derive(Debug)]
struct Robot {
    position: Position2D,
    velocity: Position2D
}

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let mut robots: Vec<Robot> = file.lines()
        .map(|line| {
            let (pos, vel) = line.split_once(' ').unwrap();
            let position = pos[2..].replace(',', " ").split_nums_whitespace::<i64>();
            let velocity = vel[2..].replace(',', " ").split_nums_whitespace::<i64>();
            Robot {
                position: Position2D::new(position[1] as isize, position[0] as isize),
                velocity: Position2D::new(velocity[1] as isize, velocity[0] as isize),
            }
        }).collect();
    // println!("{robots:?}");
    // let width = 11;
    // let height = 7;
    let width = 101;
    let height = 103;
    let steps = 100000;

    // 502
    // 603
    // 704
    // 805

    let mut step = 0;
    for _ in 0..502 {
        move_robots(&mut robots, width, height);
        step += 1;
    }
    paint(&robots, width, height);

    for _ in 0..100 {
        for _ in 0..101 {
            move_robots(&mut robots, width, height);
            step += 1;
        }
        paint(&robots, width, height);
        println!("{step}");
    }
    return Ok(());

    for step in 0..steps {
        for _ in 0..1 {
            move_robots(&mut robots, width, height);
        }
        paint(&robots, width, height);
        println!("{step}");
    }

    let mut quadrants = [0; 4];
    for robot in &robots {
        if robot.position.row == height / 2 || robot.position.col == width / 2 {
            continue;
        }
        let left = (robot.position.col < width / 2) as usize;
        let up = (robot.position.row < height / 2) as usize;
        let index = left + up * 2;
        quadrants[index] += 1;
    }
    let positions = robots.iter().map(|r| r.position).fold(HashMap::<Position2D, u64>::new(),
    |mut acc, value| {
        *acc.entry(value).or_default() += 1;
        acc
    });
    // println!("{positions:?}");

    // println!("{quadrants:?}");
    // let res = quadrants.into_iter().product::<u64>();
    // println!("{res}");

    Ok(())
}

fn move_robots(robots: &mut Vec<Robot>, width: isize, height: isize) {
    for robot in robots {
        robot.position.row = ((robot.position.row + robot.velocity.row) + height) % height;
        robot.position.col = ((robot.position.col + robot.velocity.col) + width) % width;
    }
}
// 93857400 too low

fn paint(robots: &[Robot], width: isize, height: isize) {
    let positions = robots.iter().map(|r| r.position).collect::<HashSet<Position2D>>();

    println!("\x1b[2J");
    let mut buffer = String::with_capacity(width as usize);
    for row in 0..height {
        buffer.clear();
        for col in 0..width {
            let key = Position2D::new(row, col);
            if positions.contains(&key) {
                buffer.push('X');
            } else {
                buffer.push('.');
            }
        }
        println!("{buffer}");
    }
    println!();
}
// 100000 too high
// 10000000 too high
// 1000000000 too high
