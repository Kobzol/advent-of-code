pub struct Grid {
    rows: Vec<String>,
}

impl Grid {
    pub fn from_str(input: &str) -> Grid {
        Grid {
            rows: input.lines().map(|line| line.to_string()).collect(),
        }
    }

    pub fn width(&self) -> usize {
        self.rows[0].len()
    }
    pub fn height(&self) -> usize {
        self.rows.len()
    }

    pub fn get(&self, row: isize, col: isize) -> Option<char> {
        if row < 0 || col < 0 {
            return None;
        }

        self.rows
            .get(row as usize)
            .and_then(|row| row.as_bytes().get(col as usize).map(|&c| c as char))
    }
    pub fn get_force(&self, row: isize, col: isize) -> char {
        self.get(row, col).unwrap()
    }

    pub fn neighbours(&self, row: isize, col: isize) -> Vec<char> {
        self.neighbour_positions(row, col)
            .into_iter()
            .map(|pos| self.get_force(pos.row as isize, pos.col as isize))
            .collect()
    }

    pub fn neighbour_positions(&self, row: isize, col: isize) -> Vec<Position2D> {
        let mut positions = vec![];
        for rx in -1..2 {
            for cx in -1..2 {
                if rx == 0 && cx == 0 {
                    continue;
                }

                let r = row + rx;
                let c = col + cx;
                if self.get(r, c).is_some() {
                    positions.push(Position2D {
                        row: r as usize,
                        col: c as usize,
                    });
                }
            }
        }
        positions
    }

    pub fn for_each<F: FnMut(Position2D, char)>(&self, mut f: F) {
        for row in 0..self.height() {
            for col in 0..self.width() {
                f(
                    Position2D { row, col },
                    self.get_force(row as isize, col as isize),
                )
            }
        }
    }

    pub fn items(&self) -> Vec<(Position2D, char)> {
        let mut items = vec![];
        self.for_each(|position, ch| {
            items.push((position, ch));
        });
        items
    }
}

#[derive(Debug, Ord, PartialOrd, Eq, PartialEq)]
pub struct Position2D {
    pub row: usize,
    pub col: usize,
}

impl Position2D {
    pub fn irow(&self) -> isize {
        self.row as isize
    }
    pub fn icol(&self) -> isize {
        self.col as isize
    }
}
