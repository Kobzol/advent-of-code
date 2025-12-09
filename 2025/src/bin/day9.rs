use aoc2025::vector::{Direction2D, Position2D};
use aoc2025::{Map, Set, StrExt};

#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
struct Boundary {
    min: isize,
    max: isize,
}

impl Boundary {
    fn is_within(&self, point: isize) -> bool {
        self.min <= point && point <= self.max
    }
}

fn main() -> anyhow::Result<()> {
    let data = std::fs::read_to_string("input.txt")?;
    let positions: Vec<Position2D> = data
        .lines()
        .map(|line| {
            let nums = line.split_nums_by(',');
            Position2D::new(nums[1], nums[0])
        })
        .collect();

    let mut row_boundaries = Map::default();
    let mut col_boundaries = Map::default();

    fn insert_boundary(boundaries: &mut Map<isize, Boundary>, key: isize, value: isize) {
        let boundary = boundaries.entry(key).or_insert(Boundary {
            min: value,
            max: value,
        });
        boundary.min = boundary.min.min(value);
        boundary.max = boundary.max.max(value);
    }

    let mut edges = vec![];
    for (mut p0, p1) in positions
        .iter()
        .copied()
        .zip(positions.iter().copied().cycle().skip(1))
    {
        loop {
            insert_boundary(&mut row_boundaries, p0.row, p0.col);
            insert_boundary(&mut col_boundaries, p0.col, p0.row);

            edges.push(p0);
            let dir = get_dir(p0, p1);
            p0 = p0 + dir.as_pos();

            if p0 == p1 {
                break;
            }
        }
    }

    let mut max = 0;
    for (i0, p0) in positions.iter().enumerate() {
        for &p1 in &positions[i0 + 1..] {
            if p0.row == p1.row || p0.col == p1.col {
                let dist = (p0.row.abs_diff(p1.row) + 1) * (p0.col.abs_diff(p1.col) + 1);
                max = dist.max(max);
                continue;
            }

            let mut left = *p0;
            let mut right = p1;
            if left.col > right.col {
                (left, right) = (right, left);
            }
            let mut top = *p0;
            let mut bottom = p1;
            if top.row > bottom.row {
                (top, bottom) = (bottom, top);
            }

            let top_left = left.with_row(top.row);
            let top_right = right.with_row(top.row);
            let bottom_left = bottom.with_col(left.col);
            let bottom_right = bottom.with_col(right.col);

            // down
            if !check_edge(top_left, bottom_left, Direction2D::Down, &row_boundaries) {
                continue;
            }
            // right
            if !check_edge(
                bottom_left,
                bottom_right,
                Direction2D::Right,
                &col_boundaries,
            ) {
                continue;
            }
            // up
            if !check_edge(bottom_right, top_right, Direction2D::Up, &row_boundaries) {
                continue;
            }
            // left
            if !check_edge(top_right, top_left, Direction2D::Left, &col_boundaries) {
                continue;
            }

            let dist = (p0.row.abs_diff(p1.row) + 1) * (p0.col.abs_diff(p1.col) + 1);
            max = dist.max(max);
        }
    }
    println!("{max}");

    Ok(())
}

fn check_edge(
    start: Position2D,
    end: Position2D,
    dir: Direction2D,
    boundaries: &Map<isize, Boundary>,
) -> bool {
    for point in iter_points(start, end, dir) {
        match dir {
            Direction2D::Down => {
                let anchor = boundaries[&point.row];
                if !anchor.is_within(point.col) {
                    return false;
                }
            }
            Direction2D::Right => {
                let anchor = boundaries[&point.col];
                if !anchor.is_within(point.row) {
                    return false;
                }
            }
            Direction2D::Up => {
                let anchor = boundaries[&point.row];
                if !anchor.is_within(point.col) {
                    return false;
                }
            }
            Direction2D::Left => {
                let anchor = boundaries[&point.col];
                if !anchor.is_within(point.row) {
                    return false;
                }
            }
        }
    }
    true
}

fn iter_points(
    mut start: Position2D,
    end: Position2D,
    dir: Direction2D,
) -> impl Iterator<Item = Position2D> {
    let mut next_end = false;
    std::iter::from_fn(move || {
        if next_end {
            None
        } else {
            let next = start + dir;
            if next == end {
                next_end = true;
            }
            start = next;
            Some(next)
        }
    })
}

fn get_dir(p0: Position2D, p1: Position2D) -> Direction2D {
    if p0.row < p1.row {
        Direction2D::Down
    } else if p0.col > p1.col {
        Direction2D::Left
    } else if p0.row > p1.row {
        Direction2D::Up
    } else if p0.col < p1.col {
        Direction2D::Right
    } else {
        unreachable!();
    }
}

#[derive(Copy, Clone, Debug)]
struct Rect(Position2D, Position2D);

fn is_rect_ok(rect: Rect, edges: &[Position2D], edge_set: &Set<Position2D>) -> bool {
    let rect_edge = rect_edge(rect);
    eprintln!("{rect:?}");
    eprintln!("{rect_edge:?}");
    true
}

fn rect_edge(rect: Rect) -> Vec<Position2D> {
    fn rect_half_edge(mut start: Position2D, end: Position2D) -> Vec<Position2D> {
        let mut edge = vec![start];
        loop {
            let dir = get_dir(start, end);
            start += dir.as_pos();
            if start == end {
                break;
            } else {
                edge.push(start);
            }
        }
        edge
    }

    let mut v = rect_half_edge(rect.0, rect.1);
    if rect.0.col != rect.1.col && rect.0.row != rect.1.row {
        v.extend(rect_half_edge(rect.1, rect.0));
    } else {
        v.push(rect.1);
    }
    v
}

fn is_edge(rect: Rect, pos: Position2D) -> bool {
    pos.row == rect.0.row || pos.row == rect.1.row || pos.col == rect.0.col || pos.col == rect.1.col
}

fn part1(positions: &[Position2D]) {
    let mut max = 0;
    for (i0, p0) in positions.iter().enumerate() {
        for p1 in &positions[i0 + 1..] {
            let dist = (p0.row.abs_diff(p1.row) + 1) * (p0.col.abs_diff(p1.col) + 1);
            max = dist.max(max);
        }
    }
    println!("{max}");
}
