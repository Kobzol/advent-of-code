use aoc2024::vector::{Direction2D, Position2D};
use aoc2024::{Map, Set, StrExt};
use fxhash::FxBuildHasher;
use pathfinding::directed::bfs::bfs as bfs_pathfinding;
use std::collections::VecDeque;
use std::fmt::{Debug, Formatter, Write};
use std::hash::Hash;
use std::sync::LazyLock;

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;
    let codes: Vec<String> = file.lines().map(|l| l.to_string()).collect();
    let command_length: Vec<u64> = codes
        .iter()
        .map(|code| find_command_length(code.as_bytes()))
        .collect();
    let res = command_length
        .iter()
        .zip(codes.into_iter())
        .map(|(length, mut code)| {
            code.retain(|c| c.is_ascii_digit());
            let code = code.to_u64();
            println!("{length} x {code}");
            length * code
        })
        .sum::<u64>();
    println!("{res}");

    Ok(())
}

type Move = u8;

const NUMPAD_POSITION_A: Position2D = Position2D::new(3, 2);
const DIR_POSITION_A: Position2D = Position2D::new(0, 2);

static NUMPAD_POS_TO_DIGIT: LazyLock<Map<Position2D, u8>> = LazyLock::new(|| {
    let mut map = Map::default();
    map.insert(Position2D::new(0, 0), b'7');
    map.insert(Position2D::new(0, 1), b'8');
    map.insert(Position2D::new(0, 2), b'9');
    map.insert(Position2D::new(1, 0), b'4');
    map.insert(Position2D::new(1, 1), b'5');
    map.insert(Position2D::new(1, 2), b'6');
    map.insert(Position2D::new(2, 0), b'1');
    map.insert(Position2D::new(2, 1), b'2');
    map.insert(Position2D::new(2, 2), b'3');
    map.insert(Position2D::new(3, 1), b'0');
    map.insert(Position2D::new(3, 2), b'A');
    map
});
static NUMPAD_DIGIT_TO_POS: LazyLock<Map<u8, Position2D>> = LazyLock::new(|| {
    NUMPAD_POS_TO_DIGIT
        .iter()
        .map(|(pos, digit)| (*digit, *pos))
        .collect()
});
static DIR_POS_TO_DIGIT: LazyLock<Map<Position2D, u8>> = LazyLock::new(|| {
    let mut map = Map::default();
    map.insert(Position2D::new(0, 1), b'^');
    map.insert(Position2D::new(0, 2), b'A');
    map.insert(Position2D::new(1, 0), b'<');
    map.insert(Position2D::new(1, 1), b'v');
    map.insert(Position2D::new(1, 2), b'>');
    map
});
static DIR_DIGIT_TO_POS: LazyLock<Map<u8, Position2D>> = LazyLock::new(|| {
    DIR_POS_TO_DIGIT
        .iter()
        .map(|(pos, digit)| (*digit, *pos))
        .collect()
});

#[derive(Copy, Clone, PartialEq, Eq, Hash)]
enum KeypadState {
    MovingTo(u8),
    NeedsPress,
    Finished,
}

impl Debug for KeypadState {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            KeypadState::MovingTo(c) => {
                f.write_str("M(")?;
                f.write_char(*c as char)?;
                f.write_char(')')
            }
            KeypadState::NeedsPress => f.write_char('P'),
            KeypadState::Finished => f.write_char('F'),
        }
    }
}

#[derive(Copy, Clone, PartialEq, Eq, Hash)]
enum KeypadKind {
    Numeric,
    Directional,
}

#[derive(Copy, Clone, PartialEq, Eq, Hash)]
struct Keypad {
    state: KeypadState,
    pos: (u8, u8),
    kind: KeypadKind,
}

impl Debug for Keypad {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        f.write_str(&format!("{:?},{:?}", self.pos, self.state))
    }
}

impl Keypad {
    fn pos_2d(&self) -> Position2D {
        Position2D::new(self.pos.0 as isize, self.pos.1 as isize)
    }

    fn get_digit(&self) -> u8 {
        match self.kind {
            KeypadKind::Numeric => NUMPAD_POS_TO_DIGIT.get(&self.pos_2d()).copied().unwrap(),
            KeypadKind::Directional => DIR_POS_TO_DIGIT.get(&self.pos_2d()).copied().unwrap(),
        }
    }
    fn get_pos(&self, c: u8) -> Position2D {
        match self.kind {
            KeypadKind::Numeric => NUMPAD_DIGIT_TO_POS.get(&c).copied().unwrap(),
            KeypadKind::Directional => DIR_DIGIT_TO_POS.get(&c).copied().unwrap(),
        }
    }

    fn distance_to(&self, target: u8) -> u64 {
        let target_pos = self.get_pos(target);
        target_pos.manhattan(self.pos_2d())
    }

    fn generate_moves_to(&self, target: u8) -> Vec<Move> {
        let target_pos = self.get_pos(target);
        match self.kind {
            KeypadKind::Numeric => {
                generate_moves(self.pos_2d(), target_pos, 4, 3, Position2D::new(3, 0))
            }
            KeypadKind::Directional => {
                generate_moves(self.pos_2d(), target_pos, 2, 3, Position2D::new(0, 0))
            }
        }
    }

    fn generate_moves(&self) -> Vec<Move> {
        match self.state {
            KeypadState::MovingTo(c) => {
                assert_ne!(c, self.get_digit());
                self.generate_moves_to(c)
            }
            KeypadState::NeedsPress => vec![b'A'],
            KeypadState::Finished => {
                unreachable!();
            }
        }
    }

    fn perform_move(&mut self, mv: Move, target: &[u8], remaining: &mut u8) -> MoveResult {
        match self.state {
            KeypadState::MovingTo(c) => {
                assert_ne!(c, self.get_digit());
                let dir = move_to_dir(mv);

                let new_pos = self.pos_2d() + dir;
                self.pos = (new_pos.row as u8, new_pos.col as u8);
                // assert_ne!(self.pos_2d(), Position2D::new(3, 0));
                if self.get_digit() == c {
                    self.state = KeypadState::NeedsPress;
                }
                MoveResult::Moved
            }
            KeypadState::NeedsPress => {
                if let KeypadKind::Numeric = self.kind {
                    *remaining -= 1;
                    if *remaining == 0 {
                        self.state = KeypadState::Finished;
                    } else {
                        let next = target[target.len() - *remaining as usize];
                        assert_ne!(next, self.get_digit());
                        self.state = KeypadState::MovingTo(next);
                    }
                }
                MoveResult::Entered(self.get_digit())
            }
            KeypadState::Finished => {
                unreachable!();
            }
        }
    }

    fn perform_move_simple(&mut self, mv: Move) -> MoveResult {
        match self.state {
            KeypadState::MovingTo(c) => {
                assert_ne!(c, self.get_digit());
                let dir = move_to_dir(mv);

                let new_pos = self.pos_2d() + dir;
                self.pos = (new_pos.row as u8, new_pos.col as u8);
                // assert_ne!(self.pos_2d(), Position2D::new(3, 0));
                if self.get_digit() == c {
                    self.state = KeypadState::NeedsPress;
                }
                MoveResult::Moved
            }
            KeypadState::NeedsPress => {
                self.state = KeypadState::Finished;
                MoveResult::Entered(self.get_digit())
            }
            KeypadState::Finished => {
                unreachable!();
            }
        }
    }

    fn set_target(&mut self, target: u8) {
        if target == self.get_digit() {
            self.state = KeypadState::NeedsPress;
        } else {
            self.state = KeypadState::MovingTo(target);
        }
    }
}

enum MoveResult {
    Moved,
    Entered(u8),
}

fn dir_to_move(dir: Direction2D) -> Move {
    match dir {
        Direction2D::Down => b'v',
        Direction2D::Left => b'<',
        Direction2D::Up => b'^',
        Direction2D::Right => b'>',
    }
}
fn move_to_dir(mv: Move) -> Direction2D {
    match mv {
        b'v' => Direction2D::Down,
        b'<' => Direction2D::Left,
        b'^' => Direction2D::Up,
        b'>' => Direction2D::Right,
        _ => unreachable!(),
    }
}

fn generate_moves(
    start: Position2D,
    end: Position2D,
    rows: isize,
    cols: isize,
    forbidden: Position2D,
) -> Vec<Move> {
    // assert_ne!(start, end);

    let mut moves: Vec<Move> = vec![];

    let mut push = |dir| {
        let new_pos: Position2D = start + dir;
        if new_pos.is_within(rows, cols) && new_pos != forbidden {
            moves.push(dir_to_move(dir));
        }
    };

    if end.col > start.col {
        push(Direction2D::Right);
    }
    if end.row > start.row {
        push(Direction2D::Down);
    }
    if end.row < start.row {
        push(Direction2D::Up);
    }
    if end.col < start.col {
        push(Direction2D::Left);
    }
    moves
}

// const KEYPAD_COUNT: usize = 2;
const KEYPAD_COUNT: usize = 25;

#[derive(Clone, PartialEq, Eq, Hash)]
struct State2 {
    keypads: VecDeque<Keypad>,
}

impl State2 {
    fn remove_layer(&self) -> Self {
        let mut s = self.clone();
        s.keypads.pop_front();
        s
    }
}

fn find_command_length(target: &[u8]) -> u64 {
    assert_ne!(target[0], b'A');

    let mut keypads: VecDeque<Keypad> = vec![Keypad {
        state: KeypadState::Finished,
        pos: (NUMPAD_POSITION_A.row as u8, NUMPAD_POSITION_A.col as u8),
        kind: KeypadKind::Numeric,
    }]
    .into_iter()
    .collect();
    keypads.extend(
        [Keypad {
            state: KeypadState::Finished,
            pos: (DIR_POSITION_A.row as u8, DIR_POSITION_A.col as u8),
            kind: KeypadKind::Directional,
        }; KEYPAD_COUNT],
    );
    let state = State2 { keypads };

    let mut cache = Map::default();
    let mut dist = u64::MAX;
    return find_command_inner(state, target[0], &target[1..], &mut cache, &mut dist).1;
    dist
}

// Find final state and min cost to get from state to target
fn find_command_inner(
    mut state: State2,
    target: u8,
    remaining: &[u8],
    cache: &mut Map<(State2, u8), (State2, u64)>,
    min_distance: &mut u64,
) -> (State2, u64) {
    let key = (state.clone(), target);
    if let Some(res) = cache.get(&key) {
        return res.clone();
    }

    let mut next = (state.clone(), u64::MAX);
    let mut res = if let Some(mut keypad) = state.keypads.front_mut() {
        keypad.set_target(target);
        let moves = keypad.generate_moves();

        let keypad = keypad.clone();
        assert!(!moves.is_empty());
        for &mv in &moves {
            let (mut s, mut c) =
                find_command_inner(state.remove_layer(), mv, remaining, cache, min_distance);
            s.keypads.push_front(keypad.clone());
            let keypad = s.keypads.front_mut().unwrap();
            keypad.perform_move_simple(mv);
            if keypad.state == KeypadState::Finished {
                if keypad.kind == KeypadKind::Numeric {
                    println!("Found target digit {}", target as char);

                    if !remaining.is_empty() {
                        let (s2, c2) = find_command_inner(
                            s,
                            remaining[0],
                            &remaining[1..],
                            cache,
                            min_distance,
                        );
                        s = s2;
                        c += c2;
                    }
                }
            } else {
                let (s2, c2) =
                    find_command_inner(s.clone(), target, remaining, cache, min_distance);
                s = s2;
                c += c2;
            }
            if c < next.1 {
                next = (s, c);
            }
        }
        next
    } else {
        (state, 1)
    };
    cache.insert(key, res.clone());
    res
}

// while keypad.state != KeypadState::Finished {
//     let moves = keypad.generate_moves();
//     let (mv, cost) = if moves.len() == 1 {
//         let cost = find_command_inner(state.clone(), moves[0], remaining, cache);
//         (moves[0], cost)
//     } else {
//         let c0 = find_command_inner(state.clone(), moves[0], remaining, cache);
//         let c1 = find_command_inner(state.clone(), moves[1], remaining, cache);
//         if c0 < c1 {
//             (moves[0], c0)
//         } else {
//             (moves[1], c1)
//         }
//     };
//     distance += cost;
//     keypad.perform_move_simple(mv);
// }

#[derive(Eq, PartialEq, Hash)]
struct CacheKey {
    positions: Vec<(u8, u8)>,
    target: u8,
}

#[derive(Copy, Clone, PartialEq, Eq, Hash)]
struct State {
    keypads: [Keypad; KEYPAD_COUNT + 1],
    remaining: u8,
    last_command: Option<u8>,
}

impl Debug for State {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        f.write_str(&format!(
            "{:?}, r={:?}, c={:?}",
            self.keypads, self.remaining, self.last_command
        ))
    }
}

impl State {
    fn is_finished(&self) -> bool {
        self.remaining == 0
    }

    fn cache_key(&self, index: usize, target: u8) -> CacheKey {
        CacheKey {
            positions: self
                .keypads
                .iter()
                .rev()
                .take(self.keypads.len() - (index + 1))
                .map(|keypad| keypad.pos)
                .collect(),
            target,
        }
    }
}

fn find_command_length_1(target: &[u8]) -> u64 {
    assert_ne!(target[0], b'A');

    // let target = &target[..1];

    type Container = Vec<State>;

    let mut keypads = [Keypad {
        state: KeypadState::Finished,
        pos: (DIR_POSITION_A.row as u8, DIR_POSITION_A.col as u8),
        kind: KeypadKind::Directional,
    }; KEYPAD_COUNT + 1];
    keypads[0] = Keypad {
        state: KeypadState::MovingTo(target[0]),
        pos: (NUMPAD_POSITION_A.row as u8, NUMPAD_POSITION_A.col as u8),
        kind: KeypadKind::Numeric,
    };

    let mut cache = Map::default();
    let path = bfs_pathfinding(
        &State {
            keypads,
            remaining: target.len() as u8,
            last_command: None,
        },
        |&state| {
            let mut states = Container::default();
            if state.last_command.is_none() {
                fn recurse_up(
                    states: &mut Container,
                    mut state: State,
                    index: usize,
                    mv: Move,
                    target: &[u8],
                    cache: &mut Map<CacheKey, u64>,
                ) {
                    if index + 1 == state.keypads.len() {
                        assert!(!matches!(
                            state.keypads[index].perform_move(mv, target, &mut state.remaining),
                            MoveResult::Entered(_)
                        ));
                        state.last_command = Some(mv);
                        states.push(state);
                        return;
                    }

                    let mut moves = state.keypads[index].generate_moves();
                    select_moves(&mut moves, &state, index, cache);
                    // if moves.len() == 2 {
                    //     moves.pop();
                    // }

                    for mv_next in moves {
                        let mut state = state.clone();
                        state.keypads[index + 1].set_target(mv_next);
                        recurse_up(states, state, index + 1, mv_next, target, cache);
                    }
                }

                recurse_up(&mut states, state, 0, b'A', target, &mut cache);
            } else {
                for top_key in state
                    .keypads
                    .last()
                    .unwrap()
                    .generate_moves()
                    .into_iter()
                    .take(1)
                {
                    let mut state = state.clone();
                    state.last_command = Some(top_key);

                    fn recurse_down(
                        mut state: State,
                        index: usize,
                        mv: Move,
                        target: &[u8],
                    ) -> (usize, State) {
                        if index == 0 {
                            state.keypads[0].perform_move(mv, target, &mut state.remaining);
                            (0, state)
                        } else if let MoveResult::Entered(next_move) =
                            state.keypads[index].perform_move(mv, target, &mut state.remaining)
                        {
                            recurse_down(state, index - 1, next_move, target)
                        } else {
                            (index, state)
                        }
                    }
                    let (index, state) =
                        recurse_down(state, state.keypads.len() - 1, top_key, target);

                    fn recurse_up(
                        states: &mut Container,
                        state: State,
                        index: usize,
                        cache: &mut Map<CacheKey, u64>,
                    ) {
                        if index == state.keypads.len() - 1 || state.is_finished() {
                            if state.is_finished() {
                                println!("Finished {state:?}");
                            }
                            states.push(state);
                            return;
                        }

                        let mut moves = state.keypads[index].generate_moves();
                        select_moves(&mut moves, &state, index, cache);
                        // if moves.len() == 2 {
                        //     moves.pop();
                        // }

                        for mv in moves {
                            let mut state = state.clone();
                            if index + 1 < state.keypads.len() {
                                state.keypads[index + 1].set_target(mv);
                            }
                            recurse_up(states, state, index + 1, cache);
                        }
                    }

                    recurse_up(&mut states, state, index, &mut cache);
                }
            }

            // println!("Len: {}", states.len());
            states
        },
        |state| state.is_finished(),
    );
    // path
    let commands = String::from_utf8(
        path.unwrap()
            .into_iter()
            .filter_map(|s| s.last_command)
            .collect(),
    )
    .unwrap();
    assert!(commands.ends_with('A'));
    println!("{commands:?}");
    commands.len() as u64
}

fn find_command_length_2(target: &[u8]) -> u64 {
    assert_ne!(target[0], b'A');

    let target = &target[..1];

    type Container = Vec<State>;

    let mut keypads = [Keypad {
        state: KeypadState::Finished,
        pos: (DIR_POSITION_A.row as u8, DIR_POSITION_A.col as u8),
        kind: KeypadKind::Directional,
    }; KEYPAD_COUNT + 1];
    keypads[0] = Keypad {
        state: KeypadState::MovingTo(target[0]),
        pos: (NUMPAD_POSITION_A.row as u8, NUMPAD_POSITION_A.col as u8),
        kind: KeypadKind::Numeric,
    };

    let mut state = State {
        keypads,
        remaining: target.len() as u8,
        last_command: None,
    };

    let mut cache: Map<CacheKey, u64> = Map::default();
    assign_targets(&mut state, 0, &mut cache);

    let mut moves = 0;
    while state.remaining > 0 {
        let mv = state.keypads.last().unwrap().generate_moves()[0];
        let (index, s) = recurse_down(state, state.keypads.len() - 1, mv, target);
        state = s;
        assign_targets(&mut state, index, &mut cache);
        moves += 1;
    }
    moves
}

fn recurse_down(mut state: State, index: usize, mv: Move, target: &[u8]) -> (usize, State) {
    if index == 0 {
        state.keypads[0].perform_move(mv, target, &mut state.remaining);
        (0, state)
    } else if let MoveResult::Entered(next_move) =
        state.keypads[index].perform_move(mv, target, &mut state.remaining)
    {
        recurse_down(state, index - 1, next_move, target)
    } else {
        (index, state)
    }
}

fn assign_targets(state: &mut State, index: usize, cache: &mut Map<CacheKey, u64>) {
    if index >= state.keypads.len() - 1 {
        return;
    }

    let moves = state.keypads[index].generate_moves();
    if moves.len() == 1 {
        state.keypads[index + 1].set_target(moves[0]);
        assign_targets(state, index + 1, cache);
    } else if moves.len() == 2 {
        let c0 = calculate_cost_single(state, index + 1, moves[0], cache);
        let c1 = calculate_cost_single(state, index + 1, moves[1], cache);
        let mv = if c0 < c1 { moves[0] } else { moves[1] };
        state.keypads[index + 1].set_target(mv);
        assign_targets(state, index + 1, cache);
    } else {
        unreachable!();
    }
}

// Cost of getting keypad[index] to target
fn calculate_cost_single(
    state: &State,
    index: usize,
    target: u8,
    cache: &mut Map<CacheKey, u64>,
) -> u64 {
    if index >= state.keypads.len() - 1 {
        1
    } else {
        let key = state.cache_key(index, target);
        if let Some(c) = cache.get(&key) {
            return *c;
        }

        let keypad = &state.keypads[index];
        let mut moves = keypad.generate_moves_to(target);
        if moves.len() == 2 && index < state.keypads.len() - 1 {
            let dist0 = state.keypads[index + 1].distance_to(moves[0]);
            let dist1 = state.keypads[index + 1].distance_to(moves[1]);
            if dist0 < dist1 {
                moves.pop();
            } else if dist1 < dist0 {
                moves.swap(0, 1);
                moves.pop();
            }
        }
        let cost = moves
            .into_iter()
            .map(|m| calculate_cost_single(state, index + 1, m, cache))
            .min()
            .unwrap_or(0);
        cache.insert(key, cost);
        cost
    }
}

fn select_moves(
    targets: &mut Vec<u8>,
    state: &State,
    index: usize,
    cache: &mut Map<CacheKey, u64>,
) {
    if targets.len() == 2 {
        let c0 = calculate_cost_single(state, index + 1, targets[0], cache);
        let c1 = calculate_cost_single(state, index + 1, targets[1], cache);
        if c0 != c1 {
            if c1 < c0 {
                targets.swap(0, 1);
            }
            targets.pop();
        }
    }
}

fn bfs<FN, IN, FS>(start: &State, mut successors: FN, mut success: FS) -> u64
where
    FN: FnMut(&State) -> IN,
    IN: IntoIterator<Item = State>,
    FS: FnMut(&State) -> bool,
{
    let mut queue = Vec::with_capacity(1024);
    queue.push((start.clone(), 0));
    let mut visited = Set::with_capacity_and_hasher(1024, FxBuildHasher::default());
    visited.insert(start);

    while let Some((node, cost)) = queue.pop() {
        for successor in successors(&node) {
            if success(&successor) {
                return cost + 1;
            }
            if !visited.contains(&successor) {
                queue.push((successor, cost + 1));
                if queue.len() % 100000 == 0 {
                    println!("{}", queue.len());
                }
            }
        }
    }
    0
}

// 165340 too high
