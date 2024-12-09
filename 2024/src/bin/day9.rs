use std::collections::BTreeMap;

#[derive(Debug, Clone)]
struct Range {
    id: u64,
    length: usize,
}

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let line = file.lines().next().unwrap().trim();

    let mut positions: BTreeMap<usize, Range> = BTreeMap::new();
    let mut free_spots: BTreeMap<usize, usize> = BTreeMap::new();

    let mut id = 0;
    let mut inode = 0;
    for (index, num) in line.chars().enumerate() {
        let value = num.to_digit(10).unwrap() as usize;
        if value == 0 {
            continue;
        }
        if index % 2 == 0 {
            positions.insert(inode, Range { id, length: value });
            id += 1;
            inode += value;
        } else {
            free_spots.insert(inode, value);
            inode += value;
        }
    }
    // println!("{positions:?}");
    // println!("{free_spots:?}");

    for (inode, next_num) in positions.clone().into_iter().rev() {
        let mut to_insert = None;
        let mut to_delete = None;
        for (&inode_free, free_len) in free_spots.iter_mut() {
            if inode_free < inode && *free_len >= next_num.length {
                positions.insert(inode_free, next_num.clone());
                positions.remove(&inode);

                let remaining = *free_len - next_num.length;
                to_delete = Some(inode_free);
                if remaining > 0 {
                    to_insert = Some((inode_free + next_num.length, remaining));
                }
                break;
            }
        }
        if let Some(index) = to_delete {
            free_spots.remove(&index);
        }
        if let Some((index, value)) = to_insert {
            free_spots.insert(index, value);
        }
    }

    println!("{positions:?}");
    println!("{free_spots:?}");

    let mut checksum = 0u64;
    for (index, range) in positions {
        for byte in 0..range.length {
            let final_index = (index + byte) as u64;
            checksum += final_index * range.id;
        }
    }
    println!("{checksum}");

    Ok(())
}

fn part1(mut positions: BTreeMap<usize, Range>, mut free_spots: BTreeMap<usize, usize>) {
    let mut index = 0u64;
    let mut checksum = 0u64;

    while !positions.is_empty() && !free_spots.is_empty() {
        let (&inode, next_num) = positions.iter_mut().next().unwrap();
        let (&inode_free, free_len) = free_spots.iter_mut().next().unwrap();

        if inode < inode_free {
            checksum += index * next_num.id;
            index += 1;
            next_num.length -= 1;
            if next_num.length == 0 {
                positions.remove(&inode);
            }
        } else {
            let (&inode, next_num) = positions.iter_mut().next_back().unwrap();

            checksum += index * next_num.id;
            index += 1;
            next_num.length -= 1;
            if next_num.length == 0 {
                positions.remove(&inode);
            }

            *free_len -= 1;
            if *free_len == 0 {
                free_spots.remove(&inode_free);
            }
        }
    }

    while !positions.is_empty() {
        let (&inode, next_num) = positions.iter_mut().next().unwrap();
        checksum += index * next_num.id;
        index += 1;
        next_num.length -= 1;
        if next_num.length == 0 {
            positions.remove(&inode);
        }
    }
    println!("{checksum}");
}
