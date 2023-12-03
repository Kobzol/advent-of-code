use aoc2023::{grid::Grid, grid::Position2D, NumExt};

#[derive(Debug)]
struct PartNumber {
    value: u32,
    start: Position2D,
}

impl PartNumber {
    fn positions(&self) -> Vec<Position2D> {
        (0..self.value.num_digits())
            .map(|v| Position2D {
                row: self.start.row,
                col: self.start.col + v as usize,
            })
            .collect()
    }
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let grid = Grid::from_str(&input);
    let numbers = extract_numbers(&grid);
    let part_numbers = numbers
        .into_iter()
        .filter(|pn| {
            pn.positions().into_iter().any(|pos| {
                grid.neighbours(pos.row as isize, pos.col as isize)
                    .iter()
                    .any(|&c| c == '*')
            })
        })
        .collect::<Vec<_>>();
    let sum = grid
        .items()
        .iter()
        .filter(|(_, ch)| *ch == '*')
        .filter_map(|(position, _)| {
            let neighbours = part_numbers
                .iter()
                .filter(|pn| {
                    grid.neighbour_positions(position.irow(), position.icol())
                        .into_iter()
                        .any(|pos| pn.positions().contains(&pos))
                })
                .collect::<Vec<_>>();
            (neighbours.len() == 2).then(|| neighbours[0].value * neighbours[1].value)
        })
        .sum::<u32>();
    println!("{sum}");

    Ok(())
}

fn extract_numbers(grid: &Grid) -> Vec<PartNumber> {
    let mut numbers = vec![];
    let mut number: Option<u32> = None;
    let mut position = None;

    for row in 0..grid.height() {
        for col in 0..grid.width() {
            let c = grid.get_force(row as isize, col as isize);
            if c.is_ascii_digit() {
                match &number {
                    Some(value) => {
                        number = Some(value * 10 + c.to_digit(10).unwrap());
                    }
                    None => {
                        number = Some(c.to_digit(10).unwrap());
                        position = Some(Position2D { row, col });
                    }
                }
            } else {
                if let Some(num) = number {
                    numbers.push(PartNumber {
                        value: num,
                        start: position.unwrap(),
                    });
                    number = None;
                    position = None;
                }
            }
        }
        if let Some(num) = number {
            numbers.push(PartNumber {
                value: num,
                start: position.unwrap(),
            });
            number = None;
            position = None;
        }
    }

    numbers
}
