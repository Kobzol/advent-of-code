use aoc2023::grid::Grid;

// fn horizontal_reflect(grid: &Grid, mut row_index: isize) -> u64 {
//     let mut offset = 1;
//     let mut reflected = 0;
//     while row_index >= 0
//         && row_index + offset < grid.height() as isize
//         && grid.row(row_index as usize) == grid.row((row_index + offset) as usize)
//     {
//         reflected += 1;
//         row_index -= 1;
//         offset += 2;
//     }
//
//     reflected
// }

// fn vertical_reflect(grid: &Grid, mut col_index: isize) -> u64 {
//     let mut offset = 1;
//     let mut reflected = 0;
//     while col_index >= 0
//         && col_index + offset < grid.width() as isize
//         && grid.col(col_index as usize) == grid.col((col_index + offset) as usize)
//     {
//         reflected += 1;
//         col_index -= 1;
//         offset += 2;
//     }
//
//     reflected
// }

fn horizontal_reflect(grid: &Grid, mut row_index: isize) -> bool {
    let mut offset = 1;
    let mut reflected = 0;
    while row_index >= 0
        && row_index + offset < grid.height() as isize
        && grid.row(row_index as usize) == grid.row((row_index + offset) as usize)
    {
        row_index -= 1;
        offset += 2;
        reflected += 1;
    }

    reflected > 0 && (row_index == -1 || row_index + offset == grid.height() as isize)
}

fn vertical_reflect(grid: &Grid, mut col_index: isize) -> bool {
    let mut offset = 1;
    let mut reflected = 0;
    while col_index >= 0
        && col_index + offset < grid.width() as isize
        && grid.col(col_index as usize) == grid.col((col_index + offset) as usize)
    {
        reflected += 1;
        col_index -= 1;
        offset += 2;
    }

    reflected > 0 && (col_index == -1 || col_index + offset == grid.width() as isize)
}

fn reflection(grid: &Grid, ignore: Option<u64>) -> Option<u64> {
    for row_index in 0..grid.height() {
        let reflect = horizontal_reflect(grid, row_index as isize);
        if reflect {
            let value = Some((row_index + 1) as u64 * 100);
            if value != ignore {
                return value;
            }
        }
    }
    for col_index in 0..grid.width() {
        let reflect = vertical_reflect(grid, col_index as isize);
        if reflect {
            let value = Some((col_index + 1) as u64);
            if value != ignore {
                return value;
            }
        }
    }
    None
}

fn swap(c: u8) -> u8 {
    match c {
        b'.' => b'#',
        b'#' => b'.',
        _ => panic!(),
    }
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;

    let mut data = String::new();
    let mut grids = vec![];
    for line in input.lines() {
        if line.is_empty() {
            grids.push(Grid::from_str(&data));
            data.clear();
        } else {
            data.push_str(&format!("{line}\n"));
        }
    }
    assert!(!data.is_empty());
    grids.push(Grid::from_str(&data));

    let ret = grids
        .into_iter()
        .map(|mut grid| {
            let orig = reflection(&grid, None).unwrap();
            let result = grid.positions().iter().find_map(|pos| {
                let item = grid.get_force(*pos);
                grid.set(*pos, swap(item));
                let ret = reflection(&grid, Some(orig));
                grid.set(*pos, item);
                ret
            });
            result.unwrap()
        })
        .sum::<u64>();
    println!("{ret}");

    Ok(())
}
// 1203 wrong
// 35942 wrong
// 35113 wrong
// 50740 wrong
