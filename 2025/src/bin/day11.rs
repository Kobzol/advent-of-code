use aoc2025::Map;
use pathfinding::prelude::count_paths;

fn main() -> anyhow::Result<()> {
    let data = std::fs::read_to_string("input.txt")?;
    let paths: Map<String, Vec<String>> = data
        .lines()
        .map(|line| {
            let line = line.replace(":", "");
            let mut items = line.split_whitespace();
            let first = items.next().unwrap();
            (
                first.to_string(),
                items.map(|v| v.to_string()).collect::<Vec<_>>(),
            )
        })
        .collect();

    #[derive(PartialEq, Eq, Hash, Copy, Clone, Debug)]
    struct State<'a> {
        state: &'a str,
        saw_dac: bool,
        saw_fft: bool,
    }

    let count = count_paths(
        State {
            state: "svr",
            saw_dac: false,
            saw_fft: false,
        },
        |&s| match paths.get(s.state) {
            Some(neighbours) => neighbours
                .iter()
                .map(|s| s.as_str())
                .map(move |n| {
                    let saw_dac = n == "dac";
                    let saw_fft = n == "fft";
                    State {
                        state: n,
                        saw_dac: s.saw_dac || saw_dac,
                        saw_fft: s.saw_fft || saw_fft,
                    }
                })
                .collect(),
            None => {
                if s.saw_dac && s.saw_fft {
                    vec![State {
                        state: "out",
                        saw_dac: true,
                        saw_fft: true,
                    }]
                } else {
                    vec![]
                }
            }
        },
        |&s| s.state == "out" && s.saw_dac && s.saw_fft,
    );
    println!("{count}");

    Ok(())
}
