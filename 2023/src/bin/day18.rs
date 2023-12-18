use indicatif::ProgressIterator;
use itertools::Itertools;
use std::collections::VecDeque;
use std::fmt::{Debug, Formatter};

use aoc2023::grid::{Grid, Position2D};
use aoc2023::{Map, Set};

struct Point {
    position: Position2D,
    color: String,
}

fn flood_fill(grid: &mut Grid, position: Position2D) {
    let mut candidates = vec![position];
    while let Some(pos) = candidates.pop() {
        if grid.get_force(pos) == b'.' {
            grid.set(pos, b'#');
            for neighbour in grid.neighbour_positions_4(pos) {
                candidates.push(neighbour);
            }
        }
    }
}

#[derive(Hash, Eq, PartialEq, Debug, Copy, Clone)]
enum RunOrBorder {
    Border(isize),
    Run { start: isize, end: isize },
}

impl RunOrBorder {
    fn start(&self) -> isize {
        match self {
            RunOrBorder::Border(c) => *c,
            RunOrBorder::Run { start, .. } => *start,
        }
    }
    fn is_border(&self) -> bool {
        matches!(self, RunOrBorder::Border(_))
    }
}

#[derive(Hash, Eq, PartialEq, Debug, Copy, Clone)]
struct Run {
    start: isize,
    end: isize,
}

#[derive(Hash, Eq, PartialEq, Copy, Clone, PartialOrd, Ord)]
struct Column {
    start_row: isize,
    start_col: isize,
    end_col: isize,
    end_row: Option<isize>,
}

impl Column {
    fn check(&self) {
        assert!(self.start_col < self.end_col);
    }

    fn area(&self) -> u64 {
        let width = (self.end_col - self.start_col) + 1;
        assert!(width > 1);
        let height = (self.end_row.unwrap() - self.start_row) + 1;
        assert!(height > 1);
        width as u64 * height as u64
    }

    fn edge_points(&self) -> Vec<Position2D> {
        let mut points = vec![];
        for c in self.start_col..self.end_col + 1 {
            points.push(Position2D::new(self.start_row, c));
            points.push(Position2D::new(self.end_row.unwrap(), c));
        }
        for r in self.start_row + 1..self.end_row.unwrap() {
            points.push(Position2D::new(r, self.start_col));
            points.push(Position2D::new(r, self.end_col));
        }
        points
    }

    fn overlaps(&self, other: &Column) -> bool {
        if self.end_col < other.start_col {
            return false;
        }
        if self.start_col > other.end_col {
            return false;
        }
        if self.end_row.unwrap() < other.start_row {
            return false;
        }
        if self.start_row > other.end_row.unwrap() {
            return false;
        }
        if self.end_col == other.start_col || self.start_col == other.end_col
        // || self.end_row.unwrap() == other.start_row
        // || self.start_row == other.end_row.unwrap()
        {
            return false;
        }

        true
    }
}

impl Debug for Column {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "[({}-{}), (r{},{})]",
            self.start_col,
            self.end_col,
            self.start_row,
            self.end_row.unwrap_or(-1)
        )
    }
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let mut position = Position2D::new(0, 0);

    let mut rows: Map<isize, Set<Run>> = Map::default();

    for line in input.lines() {
        let (_, hex) = line.split_once("#").unwrap();
        let hex = &hex[..hex.len() - 1];
        let count = u64::from_str_radix(&hex[..5], 16)?;
        let dir = &hex[5..];
        let dir = match dir {
            "0" => Position2D::new(0, 1),
            "1" => Position2D::new(1, 0),
            "2" => Position2D::new(0, -1),
            "3" => Position2D::new(-1, 0),
            _ => panic!(),
        };

        let is_horizontal = dir.row == 0;
        if is_horizontal {
            let next_position = position + (dir * count as isize);
            let start = position.col.min(next_position.col);
            let end = position.col.max(next_position.col);
            rows.entry(position.row)
                .or_default()
                .insert(Run { start, end });
            position = next_position;
        } else {
            position = position + (dir * count as isize);
        }
    }
    let mut rows = rows.into_iter().collect::<Vec<_>>();
    rows.sort_by_key(|r| r.0);

    let mut finished_cols: Vec<Column> = vec![];
    let mut active_columns: VecDeque<Column> = VecDeque::new();
    for (row, runs) in rows {
        let mut runs = runs.into_iter().collect::<Vec<_>>();
        runs.sort_by_key(|r| r.start);
        let mut runs = runs.into_iter().collect::<VecDeque<_>>();

        let mut last_c = active_columns.front();
        for c in active_columns.iter().skip(1) {
            assert!(c.start_col >= last_c.unwrap().end_col);
            assert!(c.start_col >= last_c.unwrap().start_col);
            last_c = Some(c);
        }

        // println!("Row {row}");
        // println!("Columns: {active_columns:?}");
        // println!("Runs: {runs:?}");
        // Ordered by start
        let mut next_columns = VecDeque::new();

        loop {
            let column = active_columns.pop_front();
            match column {
                Some(mut column) => loop {
                    match runs.front().copied() {
                        Some(run) => {
                            assert!(run.start < run.end);
                            if run.end <= column.start_col {
                                // Add run to columns
                                next_columns.push_back(Column {
                                    start_row: row,
                                    start_col: run.start,
                                    end_col: run.end,
                                    end_row: None,
                                });
                                runs.pop_front();
                            } else if run.start >= column.end_col {
                                // Move to next column
                                next_columns.push_back(column);
                                break;
                            } else {
                                // Split
                                if run.start == column.start_col {
                                    if run.end == column.end_col {
                                        runs.pop_front();
                                        finished_cols.push(Column {
                                            start_col: column.start_col,
                                            end_col: run.end,
                                            start_row: column.start_row,
                                            end_row: Some(row),
                                        });
                                    } else if run.end < column.end_col {
                                        active_columns.push_front(Column {
                                            start_col: run.end,
                                            ..column
                                        });
                                        runs.pop_front();
                                        finished_cols.push(Column {
                                            start_col: column.start_col,
                                            end_col: run.end,
                                            start_row: column.start_row,
                                            end_row: Some(row),
                                        });
                                    } else if run.end > column.end_col {
                                        // Split run
                                        runs.pop_front();
                                        runs.push_front(Run {
                                            start: column.end_col,
                                            end: run.end,
                                        });
                                        finished_cols.push(Column {
                                            start_col: column.start_col,
                                            end_col: column.end_col,
                                            start_row: column.start_row,
                                            end_row: Some(row),
                                        });
                                    }
                                    break;
                                } else if run.start > column.start_col {
                                    next_columns.push_back(Column {
                                        end_col: run.start,
                                        ..column
                                    });
                                    active_columns.push_front(Column {
                                        start_col: run.start,
                                        ..column
                                    });
                                    break;
                                } else {
                                    assert!(false);
                                }
                            }
                        }
                        None => {
                            next_columns.push_back(column);
                            break;
                        }
                    }
                },
                None => {
                    // Start new columns for the rest
                    for run in runs {
                        next_columns.push_back(Column {
                            start_row: row,
                            start_col: run.start,
                            end_col: run.end,
                            end_row: None,
                        });
                    }
                    break;
                }
            }
        }
        for c in &active_columns {
            c.check();
        }
        // println!("Finished cols: {finished_cols:?}");
        // println!("Next cols: {next_columns:?}");
        // println!();
        active_columns = next_columns;
    }
    assert!(active_columns.is_empty());

    finished_cols.sort_by_key(|c| (c.start_row, c.start_col));
    for cols in finished_cols.iter().combinations(2) {
        if cols[0].overlaps(cols[1]) {
            println!("{:?} overlaps with {:?}", cols[0], cols[1]);
            assert!(false);
        }
    }

    println!("{}", finished_cols.len());
    let mut visited = Set::default();
    let mut count = 0;
    for col in finished_cols.iter().progress() {
        count += col.area();
        for point in col.edge_points() {
            for edge in &visited {
                if contains(edge, point) {
                    count -= 1;
                }
            }
        }

        // top edge
        visited.insert((
            Position2D::new(col.start_row, col.start_col),
            Position2D::new(col.start_row, col.end_col),
        ));
        // bottom edge
        visited.insert((
            Position2D::new(col.end_row.unwrap(), col.start_col),
            Position2D::new(col.end_row.unwrap(), col.end_col),
        ));
        // left edge
        visited.insert((
            Position2D::new(col.start_row + 1, col.start_col),
            Position2D::new(col.end_row.unwrap() - 1, col.start_col),
        ));
        // right edge
        visited.insert((
            Position2D::new(col.start_row + 1, col.end_col),
            Position2D::new(col.end_row.unwrap() - 1, col.end_col),
        ));
    }
    println!("{count}");

    Ok(())
}

fn contains(edge: &(Position2D, Position2D), pos: Position2D) -> bool {
    // vertical edge
    if edge.0.col == edge.1.col {
        if edge.0.col == pos.col && edge.0.row <= pos.row && edge.1.row >= pos.row {
            return true;
        }
        return false;
    }
    // horizontal edge
    else if edge.0.row == edge.1.row {
        if edge.0.row == pos.row && edge.0.col <= pos.col && edge.1.col >= pos.col {
            return true;
        }
        return false;
    } else {
        panic!();
    }
}

fn row_scan() {
    // let mut full_rows = vec![];
    // let mut last_row: Vec<(isize, isize)> = vec![];
    // for row in min_row..max_row + 1 {
    //     let mut runs = rows.remove(&row).unwrap().into_iter().collect::<Vec<_>>();
    //     runs.sort_by_key(|r| r.start());
    //     // if row == min_row {
    //     //     full_rows.push(runs);
    //     //     continue;
    //     // }
    //
    //     // let last_row = full_rows.last().unwrap().as_slice();
    //
    //     let mut next_last_row = vec![];
    //     let mut last_col: Option<isize> = None;
    //     for run in runs {
    //         match run {
    //             RunOrBorder::Border(c) => {
    //                 match last_col {
    //                     Some(prev_c) => {
    //                         let length = c - prev_c;
    //                         let inside = contains(&last_row, c - 1);
    //                         if inside {
    //                             count += length;
    //                             next_last_row.push((prev_c, c));
    //                         }
    //                     }
    //                     None => {}
    //                 };
    //                 last_col = Some(c);
    //             }
    //             RunOrBorder::Run { start, end } => {
    //                 if let Some(prev_c) = last_col {
    //                     if contains(&last_row, start - 1) {
    //                         count += start - prev_c;
    //                         next_last_row.push((prev_c, start));
    //                     }
    //                 }
    //                 last_col = Some(end);
    //                 count += end - start;
    //                 next_last_row.push((start, end));
    //             }
    //         }
    //     }
    //     last_row = next_last_row;
    //     count += 1;
    // }
}

// 85052 too high
