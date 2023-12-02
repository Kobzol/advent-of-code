use aoc2023::StrExt;

#[derive(Default, Debug)]
struct Move {
    red: u32,
    green: u32,
    blue: u32,
}

#[derive(Debug)]
struct Game {
    id: u32,
    moves: Vec<Move>,
}

fn parse_games(input: &str) -> anyhow::Result<Vec<Game>> {
    let mut games = vec![];
    for mut line in input.lines() {
        line = &line[5..];
        let (id, rest) = line.split_by(b':');
        let id = id.to_u32();
        games.push(Game {
            id,
            moves: rest
                .split(';')
                .map(|mv| {
                    let mut move_ret = Move::default();
                    let samples = mv.split(',');
                    for sample in samples {
                        let sample = sample.trim();
                        let (count, name) = sample.split_by(b' ');
                        let count = count.to_u32();
                        match name {
                            "red" => {
                                move_ret.red = count;
                            }
                            "green" => {
                                move_ret.green = count;
                            }
                            "blue" => {
                                move_ret.blue = count;
                            }
                            _ => panic!(),
                        }
                    }
                    move_ret
                })
                .collect(),
        });
    }
    Ok(games)
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let games = parse_games(&input)?;
    let ret = games
        .iter()
        // .filter(|g| {
        //     g.moves
        //         .iter()
        //         .all(|m| m.red <= 12 && m.green <= 13 && m.blue <= 14)
        // })
        .map(|g| {
            let min_red = g.moves.iter().map(|m| m.red).max().unwrap();
            let min_green = g.moves.iter().map(|m| m.green).max().unwrap();
            let min_blue = g.moves.iter().map(|m| m.blue).max().unwrap();
            min_red * min_green * min_blue
        })
        .sum::<u32>();
    println!("{ret}");

    Ok(())
}
