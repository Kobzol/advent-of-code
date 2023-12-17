use std::collections::VecDeque;

use pathfinding::prelude::dijkstra;

use aoc2023::grid::{Grid, Position2D};

#[derive(Eq, PartialEq, Hash, Clone)]
struct Node {
    position: Position2D,
    last_moves: VecDeque<Position2D>,
}

impl Node {
    fn straight_count(&self) -> Option<(bool, u64)> {
        if self.last_moves.is_empty() {
            return None;
        }

        let reference_point = self.last_moves.back().unwrap();
        let rows = self
            .last_moves
            .iter()
            .rev()
            .take_while(|p| p.row == reference_point.row)
            .count();
        if rows > 1 {
            return Some((true, rows as u64));
        }
        let cols = self
            .last_moves
            .iter()
            .rev()
            .take_while(|p| p.col == reference_point.col)
            .count();
        if cols > 1 {
            return Some((false, cols as u64));
        }
        None
    }

    fn can_turn(&self) -> bool {
        self.straight_count()
            .map(|(_, count)| count >= 4)
            .unwrap_or(false)
    }
    fn can_stop(&self) -> bool {
        let rows = self
            .last_moves
            .iter()
            .rev()
            .take_while(|p| p.row == self.position.row)
            .count()
            >= 4;
        let cols = self
            .last_moves
            .iter()
            .rev()
            .take_while(|p| p.col == self.position.col)
            .count()
            >= 4;
        rows || cols
    }
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let mut grid = Grid::from_str(&input);

    let start = Node {
        position: Position2D::new(0, 0),
        last_moves: VecDeque::new(),
    };
    let end = Position2D::new(grid.height() as isize - 1, grid.width() as isize - 1);
    let path = dijkstra(
        &start,
        |node| {
            grid.neighbour_positions_4(node.position)
                .into_iter()
                .filter(move |p| {
                    if Some(p) == node.last_moves.back() {
                        return false;
                    }
                    if let Some(end) = node.last_moves.back() {
                        if let Some((is_horizontal, count)) = node.straight_count() {
                            let is_next_line = (is_horizontal && p.row == end.row)
                                || (!is_horizontal && p.col == end.col);

                            if count >= 10 && is_next_line {
                                return false;
                            }
                            if !node.can_turn() && !is_next_line {
                                return false;
                            }
                        }
                    }

                    true
                })
                .map(|pos| {
                    let mut last_moves = node.last_moves.clone();
                    last_moves.push_back(node.position);
                    if last_moves.len() > 10 {
                        last_moves.pop_front();
                    }
                    let cost = to_cost(grid.get_force(pos));
                    (
                        Node {
                            position: pos,
                            last_moves,
                        },
                        cost,
                    )
                })
                .collect::<Vec<_>>()
        },
        |n| n.can_stop() && n.position == end,
    )
    .unwrap();
    // println!("{}", path.0.last().unwrap().can_turn());
    // println!("{:?}", path.0.last().unwrap().last_moves);
    render_path(&mut grid, &path);
    println!("{grid}");

    let ret = path.1;
    println!("{ret}");

    Ok(())
}

fn render_path(grid: &mut Grid, path: &(Vec<Node>, u64)) {
    for node in &path.0 {
        grid.set(node.position, b'x');
    }
}

fn to_cost(c: u8) -> u64 {
    (c - 48) as u64
}
