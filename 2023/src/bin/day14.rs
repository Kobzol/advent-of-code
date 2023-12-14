use aoc2023::grid::Grid;
use aoc2023::Map;

fn tilt_north(grid: &mut Grid) {
    for c in 0..grid.width() {
        for r in 0..grid.height() {
            if grid.get_force((r, c)) == b'O' {
                let mut r2 = r;
                while r2 > 0 && grid.get_force((r2 - 1, c)) == b'.' {
                    r2 -= 1;
                }
                grid.swap((r, c), (r2, c));
            }
        }
    }
}

fn tilt_south(grid: &mut Grid) {
    for c in 0..grid.width() {
        for r in 0..grid.height() {
            let r = grid.height() - 1 - r;
            if grid.get_force((r, c)) == b'O' {
                let mut r2 = r;
                while r2 < grid.height() - 1 && grid.get_force((r2 + 1, c)) == b'.' {
                    r2 += 1;
                }
                grid.swap((r, c), (r2, c));
            }
        }
    }
}

fn tilt_west(grid: &mut Grid) {
    for r in 0..grid.height() {
        for c in 0..grid.width() {
            if grid.get_force((r, c)) == b'O' {
                let mut c2 = c;
                while c2 > 0 && grid.get_force((r, c2 - 1)) == b'.' {
                    c2 -= 1;
                }
                grid.swap((r, c), (r, c2));
            }
        }
    }
}

fn tilt_east(grid: &mut Grid) {
    for r in 0..grid.height() {
        for c in 0..grid.width() {
            let c = grid.width() - 1 - c;

            if grid.get_force((r, c)) == b'O' {
                let mut c2 = c;
                while c2 < grid.width() - 1 && grid.get_force((r, c2 + 1)) == b'.' {
                    c2 += 1;
                }
                grid.swap((r, c), (r, c2));
            }
        }
    }
}

fn cycle(grid: &mut Grid) {
    tilt_north(grid);
    tilt_west(grid);
    tilt_south(grid);
    tilt_east(grid);
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let mut grid = Grid::from_str(&input);

    let mut target_cycles = 1000000000;
    let mut cycle_size = 0;
    let mut map = Map::default();
    let mut index = 0;

    for i in (0..target_cycles) {
        let hash = grid.flatten();
        if let Some(prev_index) = map.get(&hash) {
            cycle_size = i - prev_index;
            break;
        }
        map.insert(hash, i);

        cycle(&mut grid);
        index += 1;
    }

    let remaining = (target_cycles - index) % cycle_size;
    for _ in 0..remaining {
        cycle(&mut grid);
    }

    let ret = grid
        .items()
        .into_iter()
        .filter(|(pos, c)| *c == b'O')
        .map(|(pos, _)| grid.height() as isize - pos.row)
        .sum::<isize>();
    println!("{ret}");

    Ok(())
}
