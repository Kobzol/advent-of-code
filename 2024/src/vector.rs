use std::fmt::{Display, Formatter};
use std::ops::{Add, Mul};

#[derive(Debug, Ord, PartialOrd, Eq, PartialEq, Copy, Clone, Hash)]
pub struct Position2D {
    pub row: isize,
    pub col: isize,
}

impl Position2D {
    pub const fn new(row: isize, col: isize) -> Self {
        Self { row, col }
    }

    pub fn urow(&self) -> usize {
        self.row.try_into().unwrap()
    }
    pub fn ucol(&self) -> usize {
        self.col.try_into().unwrap()
    }

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

    pub fn manhattan(&self, other: Self) -> u64 {
        let row = (other.row - self.row).abs();
        let col = (other.col - self.col).abs();
        (row + col) as u64
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

impl Add for Position2D {
    type Output = Position2D;

    fn add(self, rhs: Self) -> Self::Output {
        Self {
            row: self.row + rhs.row,
            col: self.col + rhs.col,
        }
    }
}

impl Mul<isize> for Position2D {
    type Output = Position2D;

    fn mul(self, rhs: isize) -> Self::Output {
        Self {
            row: self.row * rhs,
            col: self.col * rhs,
        }
    }
}

#[derive(Copy, Clone, Debug, Eq, PartialEq, Hash)]
pub struct Position3D(pub i64, pub i64, pub i64);

impl Position3D {
    pub fn x(&self) -> i64 {
        self.dim(0)
    }
    pub fn y(&self) -> i64 {
        self.dim(1)
    }
    pub fn z(&self) -> i64 {
        self.dim(2)
    }

    pub fn dim(&self, index: usize) -> i64 {
        match index {
            0 => self.0,
            1 => self.1,
            2 => self.2,
            _ => panic!(),
        }
    }
    pub fn with_dim(&self, index: usize, value: i64) -> Self {
        let mut new = *self;
        *new.mut_dim_ref(index) = value;
        new
    }

    pub fn mut_dim_ref(&mut self, index: usize) -> &mut i64 {
        match index {
            0 => &mut self.0,
            1 => &mut self.1,
            2 => &mut self.2,
            _ => panic!(),
        }
    }
}

impl Add for Position3D {
    type Output = Self;

    fn add(self, rhs: Self) -> Self::Output {
        Self(self.0 + rhs.0, self.1 + rhs.1, self.2 + rhs.2)
    }
}

impl Mul<i64> for Position3D {
    type Output = Self;

    fn mul(self, rhs: i64) -> Self::Output {
        Self(self.0 * rhs, self.1 * rhs, self.2 * rhs)
    }
}
