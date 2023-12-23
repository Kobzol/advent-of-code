use std::fmt::{Debug, Formatter};

use itertools::Itertools;

use aoc2023::grid::{Grid, Position2D};
use aoc2023::{Map, Set};

#[derive(Copy, Clone, Eq, PartialEq, Hash)]
struct Position {
    position: Position2D,
    level_vert: i64,
    level_hort: i64,
}

impl Position {
    fn level(&self) -> Level {
        (self.level_vert, self.level_hort)
    }
}

type Level = (i64, i64);

impl Debug for Position {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "({},{})/{:?}",
            self.position.row,
            self.position.col,
            self.level()
        )
    }
}

fn reachable(grid: &Grid, position: Position2D, steps: u64) -> u64 {
    let mut spots = Set::default();
    spots.insert(Position {
        position,
        level_vert: 0,
        level_hort: 0,
    });
    for step in 0..steps {
        spots = move_spots(&grid, spots);
    }
    spots.iter().filter(|p| p.level() == (0, 0)).count() as u64
}

// fn reachable(grid: &Grid, position: Position2D, steps: u64) -> u64 {
//     let mut shortest_paths = dijkstra_all(&position, |node| {
//         grid.neighbour_positions_4(*node)
//             .iter()
//             .filter(|p| grid.get_force(**p) == b'.')
//             .copied()
//             .map(|p| (p, 1))
//             .collect_vec()
//     });
//     shortest_paths.insert(position, (position, 0));
//     shortest_paths.values().filter(|c| c.1 < steps).count() as u64
// }

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let mut grid = Grid::from_str(&input);
    let mut position = grid
        .items()
        .iter()
        .find(|(p, c)| *c == b'S')
        .unwrap()
        .0
        .clone();
    let mut spots = Set::default();
    spots.insert(Position {
        position,
        level_vert: 0,
        level_hort: 0,
    });
    grid.set(position, b'.');

    // let mut shortest_paths = dijkstra_all(&position, |node| {
    //     grid.neighbour_positions_4(*node)
    //         .iter()
    //         .filter(|p| grid.get_force(**p) == b'.')
    //         .copied()
    //         .map(|p| (p, 1))
    //         .collect_vec()
    // });
    // shortest_paths.insert(position, (position, 0));

    // from https://www.reddit.com/r/adventofcode/comments/18nol3m/2023_day_21_a_geometric_solutionexplanation_for/
    // let odd = shortest_paths.values().filter(|c| (c.1 % 2) == 1).count();
    // let even = shortest_paths.values().filter(|c| (c.1 % 2) == 0).count();
    // let odd_far = shortest_paths
    //     .iter()
    //     .filter(|(pos, c)| (c.1 % 2) == 1 && pos.manhattan(Position2D::new(65, 65)) > 65)
    //     .count()
    //     + 1;
    // let even_far = shortest_paths
    //     .iter()
    //     .filter(|(pos, c)| (c.1 % 2) == 0 && pos.manhattan(Position2D::new(65, 65)) > 65)
    //     .count();
    // let total = ((n + 1) * (n + 1)) * odd + (n * n) * even - ((n + 1) * odd_far) + (n * even_far);
    let n = 202300u64;
    let w = grid.width() as u64;
    let e = reachable(&grid, position, 3 * w);
    let o = reachable(&grid, position, 3 * w + 1);
    println!("e: {e}, o: {o}");

    let sa = (3 * w - 3) / 2;
    let sa2 = 131 + 64;
    // let sb = (w - 3) / 2;
    let sb = 65;
    let sb2 = 65;
    let st = 130;
    println!("sa {sa}, sa2 {sa2}, sb {sb}, sb2 {sb2}");

    let a1 = reachable(&grid, Position2D::new(0, 0), sa);
    let a2 = reachable(&grid, Position2D::new(0, 130), sa);
    let a3 = reachable(&grid, Position2D::new(130, 0), sa);
    let a4 = reachable(&grid, Position2D::new(130, 130), sa);
    let a = a1 + a2 + a3 + a4;
    println!("{a1} {a2} {a3} {a4} {a}");

    let b1 = reachable(&grid, Position2D::new(0, 0), sb);
    let b2 = reachable(&grid, Position2D::new(0, 130), sb);
    let b3 = reachable(&grid, Position2D::new(130, 0), sb);
    let b4 = reachable(&grid, Position2D::new(130, 130), sb);
    let b = b1 + b2 + b3 + b4;
    println!("{b1} {b2} {b3} {b4} {b}");

    let t1 = reachable(&grid, Position2D::new(0, 65), st);
    let t2 = reachable(&grid, Position2D::new(65, 0), st);
    let t3 = reachable(&grid, Position2D::new(65, 130), st);
    let t4 = reachable(&grid, Position2D::new(130, 65), st);
    let t = t1 + t2 + t3 + t4;
    println!("{t1} {t2} {t3} {t4} {t}");

    let total = ((n - 1) * (n - 1)) * o + (n * n) * e + (n - 1) * a + n * b + t;
    println!("{}", total);
    return Ok(());
    // 612905550066489
    // 612928028479806 wrong
    // 612941110899440 low
    // 612941112342073 wrong
    // 612941134797231 wrong
    // 612941134797232 ?
    // 612941134797233 wrong
    // 612941134797262 wrong
    // 612941134999532 wrong
    // 612941135201832 wrong
    // 612941135209208 wrong
    // 612941160286999 wrong
    // 612941160290831 wrong
    // 612941189822769 wrong
    // 612941189822799 wrong
    // 612941995381156 wrong
    // 612947170623657 high
    // 612947194521597 wrong
    // 612947220011460
    // 613145186415629 wrong
    // 613145186415630

    // Example
    let mut unique = vec![
        vec![Position2D::new(0, 0)],
        vec![Position2D::new(0, 3)],
        vec![Position2D::new(0, 10)],
        vec![
            Position2D::new(0, 10),
            Position2D::new(4, 10),
            Position2D::new(10, 10),
        ],
        vec![Position2D::new(0, 10), Position2D::new(10, 10)],
        vec![Position2D::new(4, 0)],
        vec![Position2D::new(4, 10)],
        vec![Position2D::new(5, 5)], // start, index 7, not repeated
        vec![Position2D::new(10, 0)],
        vec![Position2D::new(10, 0), Position2D::new(10, 10)],
        vec![Position2D::new(10, 8)],
        vec![Position2D::new(10, 10)],
    ];

    // Input
    let mut unique = vec![
        vec![Position2D::new(0, 0)],
        vec![Position2D::new(0, 65)],
        vec![Position2D::new(0, 130)],
        vec![Position2D::new(65, 0)],
        vec![Position2D::new(65, 65)], // start, index 4, not repeated
        vec![Position2D::new(65, 130)],
        vec![Position2D::new(130, 0)],
        vec![Position2D::new(130, 65)],
        vec![Position2D::new(130, 130)],
    ];

    // let mut level_count_to_step = Map::default();
    let mut last_level_step = 0;
    let mut last_level = 0;
    let levels_of_interest = vec![
        // (0, 0),
        (-1, -1),
        (-2, -2),
        (1, 1),
        (2, 2),
        (0, 1),
        (0, 2),
        (0, -1),
        (0, -2),
        (-1, 0),
        (-2, 0),
        (1, 0),
        (2, 0),
    ];
    let mut level_to_hashes: Map<Level, Map<Vec<Position2D>, i32>> = Map::default();
    let mut last_even = 1;
    let mut last_odd = 0;
    let mut last_even_signum_step = 0;
    let mut last_odd_signum_step = 0;
    // let mut levels_visited = Set::default();
    // let mut level_initializers: Map<Level, Vec<Position2D>> = Map::default();
    let steps = 1000i32;
    let mut level_start: Map<Level, i32> = Map::default();
    // let mut level_to_init = Map::default();
    let mut visited_levels: Set<Level> = Set::default();
    for step in 0..steps {
        spots = move_spots(&grid, spots);
        let step = step + 1;

        // if step.saturating_sub(16) % 11 == 0 {
        //     println!("step 1: {step}, length: {}", spots.len());
        // }
        // if step.saturating_sub(22) % 11 == 0 {
        //     println!("step 2: {step}, length: {}", spots.len());
        // }
        // if step.saturating_sub(23) % 11 == 0 {
        //     println!("step 3: {step}, length: {}", spots.len());
        // }
        println!("{step} {}", spots.len());

        // let new_levels = spots
        //     .iter()
        //     .filter(|p| !levels_visited.contains(&p.level()))
        //     .map(|p| p.level())
        //     .collect::<Set<_>>();
        // for level in &new_levels {
        //     visited_levels.insert(*level);
        // }
        // for level in &levels_of_interest {
        // for level in &new_levels {
        //     if *level == (0, 0) {
        //         continue;
        //     }
        //     if levels_visited.get(level).is_some() {
        //         continue;
        //     }
        //     let mut level_positions = spots
        //         .iter()
        //         .filter(|p| p.level() == *level)
        //         .map(|p| p.position)
        //         .collect_vec();
        //     level_positions.sort_unstable();
        //     if level_positions.is_empty() {
        //         continue;
        //     }
        //
        //     if level_start.get(level).is_none() {
        //         level_start.insert(*level, step);
        //         level_to_init.insert(
        //             *level,
        //             unique.iter().position(|p| *p == level_positions).unwrap(),
        //         );
        //     }
        //     if let Some(before) = level_to_hashes
        //         .entry(*level)
        //         .or_default()
        //         .get(&level_positions)
        //     {
        //         // println!(
        //         //     "step: {step}, level: {level:?}, before: {}, diff: {}, from_level_start: {}, size: {}, index: {}",
        //         //     before,
        //         //     step - before,
        //         //     before - level_start.get(level).unwrap(),
        //         //     level_positions.len(),
        //         //     level_to_init.get(level).unwrap()
        //         // );
        //         levels_visited.insert(*level);
        //     }
        //     level_to_hashes
        //         .entry(*level)
        //         .or_default()
        //         .insert(level_positions, step);
        // }

        // let mut segment_by_signum: Map<bool, Set<(i64, i64)>> = Map::default();
        // for spot in &spots {
        //     let segment = (spot.level_hort, spot.level_vert);
        //     let key = (spot.level_hort + spot.level_vert).abs() % 2 == 0;
        //     segment_by_signum.entry(key).or_default().insert(segment);
        // }
        // let mut even = segment_by_signum
        //     .get(&true)
        //     .map(|s| s.len())
        //     .unwrap_or_default();
        // let odd = segment_by_signum
        //     .get(&false)
        //     .map(|s| s.len())
        //     .unwrap_or_default();
        // even = even + odd;
        //
        // let mut res: Map<usize, u64> = Map::default();
        // let new_levels = spots
        //     .iter()
        //     .filter(|p| !visited_levels.contains(&p.level()))
        //     .map(|p| p.level())
        //     .collect::<Set<_>>();
        // for level in &new_levels {
        //     if *level != (0, 0) {
        //         let x = get_by_level(&spots, *level);
        //         level_to_init.insert(*level, unique.iter().position(|p| *p == x).unwrap());
        //         // println!(
        //         //     "step: {step}, {level:?}/{}",
        //         //     level_to_init.get(level).unwrap()
        //         // );
        //     }
        // }
        // if even != last_even {
        //     // println!(
        //     //     "E {step}: even {even}, even diff {}, step diff {}",
        //     //     even - last_even,
        //     //     step - last_even_signum_step
        //     // );
        //     last_even = even;
        //     last_even_signum_step = step;
        //
        //     for level in &new_levels {
        //         if *level != (0, 0) {
        //             let x = get_by_level(&spots, *level);
        //             let index = unique.iter().position(|p| **p == x).unwrap();
        //             *res.entry(index).or_default() += 1;
        //         }
        //         visited_levels.insert(*level);
        //     }
        //     // println!("{res:?}");
        // }
        // if odd != last_odd {
        //     // println!(
        //     //     "O {step}: odd {odd}, odd diff {}, step diff {}",
        //     //     odd - last_odd,
        //     //     step - last_odd_signum_step
        //     // );
        //     last_odd = odd;
        //     last_odd_signum_step = step;
        // }
        // for level in new_levels {
        //     visited_levels.insert(level);
        // }

        // assert_eq!(even + odd, calculate_unique_levels(&spots));
        // println!(
        //     "after {step}: even: {even}, odd: {odd}, total: {}",
        //     calculate_unique_levels(&spots)
        // );
    }

    // // for spot in &spots {
    // //     let level = spot.level();
    // //     if !level_initializers.contains_key(&level) {
    // //         let mut items = spots
    // //             .iter()
    // //             .filter(|p| p.level() == level)
    // //             .map(|p| p.position)
    // //             .collect_vec();
    // //         items.sort_unstable();
    // //         level_initializers.insert(level, items);
    // //     }
    // // }
    //
    // // let mut unique = level_initializers
    // //     .values()
    // //     .collect::<Set<_>>()
    // //     .into_iter()
    // //     .collect_vec();
    // // unique.sort_unstable();
    // // println!("{}", unique.len());
    // // println!("{unique:?}");
    //
    // spots = orig_spots;
    //
    // println!("Init configs found");
    //
    // // let mut init_pos_to_step = Map::default();
    // let mut last_even = 1;
    // let mut last_odd = 0;
    // let mut last_even_signum_step = 0;
    // let mut last_odd_signum_step = 0;
    //
    // let steps = 1000;
    // let mut init_pos_to_step: Map<(Level, usize), usize> = Map::default();
    // let mut level_to_init = Map::default();
    // let mut visited_levels: Set<Level> = Set::default();
    // visited_levels.insert((0, 0));
    // for step in 0..steps {
    //     spots = move_spots(&grid, spots);
    //     let step = step + 1;
    //     let new_levels = spots
    //         .iter()
    //         .filter(|p| !visited_levels.contains(&p.level()))
    //         .map(|p| p.level())
    //         .collect::<Set<_>>();
    //     for new_level in new_levels {
    //         let items = get_by_level(&spots, new_level);
    //         let index = unique
    //             .iter()
    //             .position(|p| **p == items)
    //             .expect("Init configuration not found");
    //         level_to_init.insert(new_level, index);
    //         // if let Some(last_step) = init_pos_to_step.get(&index) {
    //         //     println!(
    //         //         "Step {step}: index {index}, last_step {}, diff {}",
    //         //         last_step,
    //         //         step - last_step,
    //         //     );
    //         // }
    //         // level_.insert(index, step);
    //
    //         // println!("{step}: {index}");
    //         // println!("Step {step}, level {new_level:?}, index {index}");
    //         visited_levels.insert(new_level);
    //     }
    //
    //     // let mut segment_by_signum: Map<bool, Set<(i64, i64)>> = Map::default();
    //     // for spot in &spots {
    //     //     let segment = spot.level();
    //     //     let key = (spot.level_hort + spot.level_vert).abs() % 2 == 0;
    //     //     segment_by_signum.entry(key).or_default().insert(segment);
    //     // }
    //     // let mut even = segment_by_signum
    //     //     .get(&true)
    //     //     .map(|s| s.len())
    //     //     .unwrap_or_default();
    //     // let mut odd = segment_by_signum
    //     //     .get(&false)
    //     //     .map(|s| s.len())
    //     //     .unwrap_or_default();
    //     // even = even + odd;
    //     // odd = even + odd;
    //
    //     // if even != last_even {
    //     //     println!(
    //     //         "E {step}: even {even}, even diff {}, step diff {}",
    //     //         even - last_even,
    //     //         step - last_even_signum_step
    //     //     );
    //     //     last_even = even;
    //     //     last_even_signum_step = step;
    //     //     let new_levels = spots
    //     //         .iter()
    //     //         .filter(|p| !visited_levels.contains(&p.level()))
    //     //         .map(|p| p.level())
    //     //         .collect::<Set<_>>();
    //     //     let mut res = Set::default();
    //     //     for level in new_levels {
    //     //         let x = get_by_level(&spots, level);
    //     //         let index = unique.iter().position(|p| **p == x).unwrap();
    //     //         res.insert(index);
    //     //     }
    //     //     println!("{res:?}");
    //     // }
    //     // if odd != last_odd {
    //     //     println!(
    //     //         "O {step}: odd {odd}, odd diff {}, step diff {}",
    //     //         odd - last_odd,
    //     //         step - last_odd_signum_step
    //     //     );
    //     //     last_odd = odd;
    //     //     last_odd_signum_step = step;
    //     //     let new_levels = spots
    //     //         .iter()
    //     //         .filter(|p| !visited_levels.contains(&p.level()))
    //     //         .map(|p| p.level())
    //     //         .collect::<Set<_>>();
    //     //     let mut res = Set::default();
    //     //     for level in new_levels {
    //     //         let x = get_by_level(&spots, level);
    //     //         let index = unique.iter().position(|p| **p == x).unwrap();
    //     //         res.insert(index);
    //     //     }
    //     //     let res = res.into_iter().sorted_unstable().collect_vec();
    //     //     println!("{res:?}");
    //     // }
    //     // if odd != last_odd {
    //     //     println!(
    //     //         "O {step}: odd {odd}, odd diff {}, step diff {}",
    //     //         odd - last_odd,
    //     //         step - last_odd_signum_step
    //     //     );
    //     //     last_odd = odd;
    //     //     last_odd_signum_step = step;
    //     // }
    //     for spot in &spots {
    //         visited_levels.insert(spot.level());
    //     }
    // }

    println!("{}", spots.len());

    Ok(())
}

fn get_by_level(spots: &Set<Position>, level: Level) -> Vec<Position2D> {
    let mut items = spots
        .iter()
        .filter(|p| p.level() == level)
        .map(|p| p.position)
        .collect_vec();
    items.sort_unstable();
    items
}

fn calculate_unique_levels(spots: &Set<Position>) -> usize {
    spots.iter().map(|p| p.level()).collect::<Set<_>>().len()
}

fn move_spots(grid: &Grid, spots: Set<Position>) -> Set<Position> {
    let mut next_spots = Set::default();
    for spot in &spots {
        for neighbor in neighbours(grid, *spot) {
            next_spots.insert(neighbor);
        }
    }
    next_spots
}

fn neighbours(grid: &Grid, spot: Position) -> Vec<Position> {
    const DIRS: [Position2D; 4] = [
        Position2D::new(0, 1),
        Position2D::new(1, 0),
        Position2D::new(0, -1),
        Position2D::new(-1, 0),
    ];
    let mut positions = vec![];
    for dir in DIRS {
        let mut new_pos = spot.position + dir;
        let mut level_vert = spot.level_vert;
        let mut level_hort = spot.level_hort;
        if new_pos.row < 0 {
            level_vert -= 1;
            new_pos.row = (grid.height() - 1) as isize;
        } else if new_pos.row == grid.height() as isize {
            level_vert += 1;
            new_pos.row = 0;
        } else if new_pos.col < 0 {
            level_hort -= 1;
            new_pos.col = (grid.width() - 1) as isize;
        } else if new_pos.col == grid.width() as isize {
            level_hort += 1;
            new_pos.col = 0;
        }

        if grid.get_force(new_pos) == b'.' {
            positions.push(Position {
                position: new_pos,
                level_vert,
                level_hort,
            });
        }
    }
    positions
}
// 612947170623657 too high
// 612941110899440 too low
