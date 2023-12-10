use std::fmt::{Display, Formatter};

#[derive(Debug, Clone)]
pub struct Grid {
    rows: Vec<Vec<u8>>,
}

impl Grid {
    pub fn from_str(input: &str) -> Grid {
        Grid {
            rows: input.lines().map(|line| line.as_bytes().to_vec()).collect(),
        }
    }

    pub fn width(&self) -> usize {
        self.rows[0].len()
    }
    pub fn height(&self) -> usize {
        self.rows.len()
    }

    pub fn get<P: Into<Position2D>>(&self, pos: P) -> Option<u8> {
        let Position2D { row, col } = pos.into();
        if row < 0 || col < 0 {
            return None;
        }

        self.rows
            .get(row as usize)
            .and_then(|row| row.get(col as usize).copied())
    }
    pub fn get_force<P: Into<Position2D>>(&self, pos: P) -> u8 {
        self.get(pos).unwrap()
    }

    pub fn set<P: Into<Position2D>>(&mut self, pos: P, c: u8) {
        let Position2D { row, col } = pos.into();
        if let Some(row) = self.rows.get_mut(row as usize) {
            row[col as usize] = c;
        }
    }

    pub fn neighbours<P: Into<Position2D>>(&self, pos: P) -> Vec<u8> {
        self.neighbour_positions(pos)
            .into_iter()
            .map(|pos| self.get_force(pos))
            .collect()
    }

    pub fn neighbour_positions<P: Into<Position2D>>(&self, pos: P) -> Vec<Position2D> {
        let pos = pos.into();
        let mut positions = vec![];
        for rx in -1..2 {
            for cx in -1..2 {
                if rx == 0 && cx == 0 {
                    continue;
                }

                let r = pos.row + rx;
                let c = pos.col + cx;
                if self.get((r, c)).is_some() {
                    positions.push(Position2D { row: r, col: c });
                }
            }
        }
        positions
    }

    pub fn for_each<F: FnMut(Position2D, u8)>(&self, mut f: F) {
        for row in 0..self.height() as isize {
            for col in 0..self.width() as isize {
                let pos = Position2D { row, col };
                f(pos, self.get_force(pos))
            }
        }
    }

    pub fn items(&self) -> Vec<(Position2D, u8)> {
        let mut items = vec![];
        self.for_each(|position, ch| {
            items.push((position, ch));
        });
        items
    }

    pub fn find_pos(&self, c: u8) -> Position2D {
        self.items()
            .iter()
            .filter(|(_, item)| *item == c)
            .map(|(pos, _)| *pos)
            .next()
            .unwrap()
    }

    pub fn contains_pos<P: Into<Position2D>>(&self, pos: P) -> bool {
        self.get(pos).is_some()
    }
}

impl Display for Grid {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        for row in &self.rows {
            writeln!(f, "{}", std::str::from_utf8(row).unwrap())?;
        }
        Ok(())
    }
}

#[derive(Debug, Ord, PartialOrd, Eq, PartialEq, Copy, Clone, Hash)]
pub struct Position2D {
    pub row: isize,
    pub col: isize,
}

impl Position2D {
    pub fn up(&self) -> Position2D {
        Position2D {
            row: self.row - 1,
            col: self.col,
        }
    }
    pub fn down(&self) -> Position2D {
        Position2D {
            row: self.row + 1,
            col: self.col,
        }
    }
    pub fn left(&self) -> Position2D {
        Position2D {
            row: self.row,
            col: self.col - 1,
        }
    }
    pub fn right(&self) -> Position2D {
        Position2D {
            row: self.row,
            col: self.col + 1,
        }
    }
}

impl From<(isize, isize)> for Position2D {
    fn from((row, col): (isize, isize)) -> Self {
        Self { row, col }
    }
}

impl From<(usize, usize)> for Position2D {
    fn from((row, col): (usize, usize)) -> Self {
        Self {
            row: row as isize,
            col: col as isize,
        }
    }
}

impl Display for Position2D {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "({}, {})", self.row, self.col)
    }
}
