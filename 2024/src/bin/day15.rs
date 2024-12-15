use aoc2024::grid::Grid;
use aoc2024::vector::{Direction2D, Position2D};
use hashbrown::HashSet;
use itertools::Itertools;
use std::io::{BufRead, Read};

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let mut lines = file.lines();
    let mut grid = String::new();
    for line in &mut lines {
        if line.is_empty() {
            break;
        }
        grid.push_str(line);
        grid.push('\n');
    }
    let grid = Grid::from_str(&grid);
    let actions = lines.map(|l| l.chars()).flatten().collect::<String>();

    let mut walls = HashSet::new();
    let mut boxes = HashSet::new();
    let mut robot = None;

    for row in 0..grid.height() as isize {
        for col in 0..grid.width() as isize {
            let pos = Position2D {
                row: row,
                col: col * 2,
            };
            match grid.get_force(Position2D::new(row, col)) {
                b'#' => {
                    walls.insert(pos);
                    walls.insert(pos.right());
                }
                b'O' => {
                    boxes.insert(pos);
                }
                b'@' => {
                    robot = Some(pos);
                }
                _ => {}
            }
        }
    }

    let mut robot = robot.unwrap();

    let mut stdin = std::io::stdin().lock();
    for (index, action) in actions.chars().enumerate() {
        // render_wide(&grid, &boxes, &walls, robot);
        // if index > 193 {
        //     println!("{action} {index}");
        //     stdin.read_line(&mut String::new())?;
        // }

        let dir = match action {
            '^' => Direction2D::Up,
            '>' => Direction2D::Right,
            'v' => Direction2D::Down,
            '<' => Direction2D::Left,
            _ => panic!("Wrong action {action}"),
        };
        let next_pos = robot + dir;
        if walls.contains(&next_pos) {
            continue;
        }
        if get_box(&boxes, next_pos).is_none() {
            robot = next_pos;
            continue;
        }
        move_boxes_wide(dir, next_pos, &mut boxes, &walls);
        if get_box(&boxes, next_pos).is_none() {
            robot = next_pos;
        }
    }
    render_wide(&grid, &boxes, &walls, robot);

    let res = boxes
        .iter()
        .map(|pos| pos.row as u64 * 100 + pos.col as u64)
        .sum::<u64>();
    println!("{res}");

    Ok(())
}

fn move_boxes(
    direction: Direction2D,
    pos: Position2D,
    boxes: &mut HashSet<Position2D>,
    walls: &HashSet<Position2D>,
) {
    let len = boxes.len();
    assert!(boxes.contains(&pos));

    let mut free_pos = None;
    let mut end_pos = pos;
    loop {
        if walls.contains(&end_pos) {
            break;
        }
        if boxes.contains(&end_pos) {
            end_pos = end_pos + direction;
        } else {
            free_pos = Some(end_pos);
            break;
        }
    }
    if let Some(free_pos) = free_pos {
        boxes.remove(&pos);
        boxes.insert(free_pos);
    }
    assert_eq!(boxes.len(), len);
}

fn get_box(boxes: &HashSet<Position2D>, pos: Position2D) -> Option<Position2D> {
    boxes.get(&pos).or_else(|| boxes.get(&pos.left())).copied()
}

fn move_boxes_wide(
    direction: Direction2D,
    pos: Position2D,
    boxes: &mut HashSet<Position2D>,
    walls: &HashSet<Position2D>,
) {
    let len = boxes.len();
    assert!(get_box(boxes, pos).is_some());

    let mut to_move: Vec<Position2D> = vec![];

    if let Direction2D::Right | Direction2D::Left = direction {
        let mut free_pos = None;
        let mut end_pos = pos;
        loop {
            if walls.contains(&end_pos) {
                break;
            }
            if let Some(b) = get_box(boxes, end_pos) {
                end_pos = (end_pos + direction) + direction;
                to_move.push(b);
            } else {
                free_pos = Some(end_pos);
                break;
            }
        }
        if free_pos.is_none() {
            return;
        }
    } else {
        let mut horizont = vec![get_box(boxes, pos).unwrap()];
        let mut can_move = true;
        'outer: while !horizont.is_empty() {
            let mut next_horizont = vec![];
            for &pos in &horizont {
                to_move.push(pos);
                let next_pos = pos + direction;
                for pos in [next_pos, next_pos.right()] {
                    if walls.contains(&pos) {
                        can_move = false;
                        break 'outer;
                    }
                    if let Some(b) = get_box(boxes, pos) {
                        next_horizont.push(b);
                    }
                }
            }
            horizont = next_horizont;
        }
        if !can_move {
            return;
        }
    }

    for pos in &to_move {
        boxes.remove(pos);
    }
    for pos in &to_move {
        boxes.insert(*pos + direction);
    }

    assert_eq!(boxes.len(), len);
}

fn render(grid: &Grid, boxes: &HashSet<Position2D>, robot: Position2D) {
    for row in 0..grid.height() {
        for col in 0..grid.width() {
            let pos = Position2D::new(row as isize, col as isize);
            let c = if boxes.contains(&pos) {
                b'O'
            } else if robot == pos {
                b'@'
            } else {
                let c = grid.get_force(pos);
                if c == b'@' || c == b'O' {
                    b'.'
                } else {
                    c
                }
            };
            print!("{}", c as char);
        }
        println!();
    }
    println!();
}

fn render_wide(
    grid: &Grid,
    boxes: &HashSet<Position2D>,
    walls: &HashSet<Position2D>,
    robot: Position2D,
) {
    for row in 0..grid.height() {
        for col in 0..grid.width() * 2 {
            let pos = Position2D::new(row as isize, col as isize);
            let c = if boxes.contains(&pos) {
                b'['
            } else if boxes.contains(&pos.left()) {
                b']'
            } else if robot == pos {
                b'@'
            } else if walls.contains(&pos) {
                b'#'
            } else {
                b'.'
            };
            print!("{}", c as char);
        }
        println!();
    }
    println!();
}

fn part1(grid: &Grid, actions: &str) {
    let mut robot = grid.find_pos(b'@');
    let mut boxes = grid
        .items()
        .iter()
        .filter(|(pos, c)| *c == b'O')
        .map(|(pos, _)| *pos)
        .collect::<HashSet<Position2D>>();
    let walls = grid
        .items()
        .iter()
        .filter(|(pos, c)| *c == b'#')
        .map(|(pos, _)| *pos)
        .collect::<HashSet<Position2D>>();

    for action in actions.chars() {
        // render(&grid, &boxes, robot);
        let dir = match action {
            '^' => Direction2D::Up,
            '>' => Direction2D::Right,
            'v' => Direction2D::Down,
            '<' => Direction2D::Left,
            _ => panic!("Wrong action {action}"),
        };
        let next_pos = robot + dir;
        if walls.contains(&next_pos) {
            continue;
        }
        if !boxes.contains(&next_pos) {
            robot = next_pos;
            continue;
        }
        move_boxes(dir, next_pos, &mut boxes, &walls);
        if !boxes.contains(&next_pos) {
            robot = next_pos;
        }
    }
    render(&grid, &boxes, robot);
}
