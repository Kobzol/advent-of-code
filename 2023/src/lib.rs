use std::fmt::Debug;
use std::str::FromStr;

pub mod grid;

pub trait StrExt {
    fn index(&self, c: u8) -> Option<usize>;

    fn split_by(&self, c: u8) -> (&str, &str);
    fn split_nums_whitespace<T: FromStr>(&self) -> Vec<T>
    where
        <T as FromStr>::Err: Debug;

    fn to_u32(&self) -> u32;
    fn to_u64(&self) -> u64;
}

impl StrExt for str {
    fn index(&self, c: u8) -> Option<usize> {
        self.as_bytes().iter().position(|&ch| ch == c)
    }
    fn split_by(&self, c: u8) -> (&str, &str) {
        let index = self.index(c).unwrap();
        (&self[..index], &self[index + 1..])
    }

    fn split_nums_whitespace<T: FromStr>(&self) -> Vec<T>
    where
        <T as FromStr>::Err: Debug,
    {
        self.split_ascii_whitespace()
            .map(|v| v.parse().unwrap())
            .collect()
    }

    fn to_u32(&self) -> u32 {
        self.parse().unwrap()
    }
    fn to_u64(&self) -> u64 {
        self.parse().unwrap()
    }
}

pub trait NumExt {
    fn num_digits(&self) -> u32;
}

impl NumExt for u32 {
    fn num_digits(&self) -> u32 {
        format!("{self}").len() as u32
    }
}
