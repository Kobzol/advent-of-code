use std::cmp::Ordering;
use std::collections::HashMap;
use std::fmt::{Display, Formatter};

use aoc2023::{DisplaySlice, StrExt};

#[derive(Debug, PartialEq, Eq, Hash, Copy, Clone)]
struct Card(char);

impl Card {
    fn value(&self) -> u32 {
        match self.0 {
            'J' => 0,
            '2' => 1,
            '3' => 2,
            '4' => 3,
            '5' => 4,
            '6' => 5,
            '7' => 6,
            '8' => 7,
            '9' => 8,
            'T' => 9,
            'Q' => 10,
            'K' => 11,
            'A' => 12,
            _ => panic!("Unknown card {}", self.0),
        }
    }
}

impl PartialOrd for Card {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        self.value().partial_cmp(&other.value())
    }
}

impl Ord for Card {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap()
    }
}

#[derive(Debug, Eq, PartialEq)]
struct Hand {
    cards: Vec<Card>,
    bid: u64,
}

impl Display for Hand {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{} ({})",
            self.cards.iter().map(|c| c.0).collect::<String>(),
            self.bid,
        )
    }
}

impl Hand {
    fn calc_type(&self) -> u32 {
        let mut counts = self
            .cards
            .iter()
            .fold(HashMap::<Card, u64>::new(), |mut acc, card| {
                *acc.entry(*card).or_default() += 1;
                acc
            });
        // Five of a kind
        if counts.len() == 1 {
            assert_eq!(counts.into_iter().next().unwrap().1, 5);
            return 7;
        }
        if counts.len() == 2 {
            if counts.iter().any(|(_, &count)| count == 4) {
                // Four of a kind
                return 6;
            }
            // Full house
            return 5;
        }
        if counts.len() == 3 {
            if counts.iter().any(|(_, &count)| count == 3) {
                // Three of a kind
                return 4;
            }
            // Two pair
            return 3;
        }
        if counts.len() == 4 {
            // One pair
            return 2;
        }
        // High card
        assert_eq!(counts.len(), 5);
        1
    }

    fn calc_type_joker(&self) -> u32 {
        let mut counts = self
            .cards
            .iter()
            .fold(HashMap::<Card, u64>::new(), |mut acc, card| {
                *acc.entry(*card).or_default() += 1;
                acc
            });
        let jokers = counts.remove(&Card('J')).unwrap_or(0);
        if jokers == 0 {
            return self.calc_type();
        }
        if counts.iter().any(|(_, &count)| count == 4) {
            // Five of a kind, one joker applied
            assert_eq!(jokers, 1);
            return 7;
        }
        if counts.iter().any(|(_, &count)| count == 3) {
            match jokers {
                1 => {
                    // Four of a kind, one joker applied
                    assert_eq!(counts.len(), 2);
                    assert_eq!(jokers, 1);
                    return 6;
                }
                2 => {
                    // Five of a kind, two jokers applied
                    assert_eq!(counts.len(), 1);
                    return 7;
                }
                _ => panic!(),
            }
        }
        if counts.len() == 2 {
            match jokers {
                1 => {
                    // Full house, one joker applied
                    return 5;
                }
                2 | 3 => {
                    // Four of a kind, two jokers applied
                    return 6;
                }
                _ => panic!(),
            }
        }
        if counts.len() == 3 && counts.iter().any(|(_, &count)| count == 2) {
            // Three of a kind, one joker applied
            assert_eq!(jokers, 1);
            return 4;
        }
        if counts.len() == 3 {
            assert_eq!(jokers, 2);
            // Three of a kind, two jokers applied
            return 4;
        }
        if counts.len() == 4 {
            // One pair, one joker applied
            assert_eq!(jokers, 1);
            return 2;
        }
        if counts.len() <= 1 {
            assert!(jokers == 3 || jokers == 4 || jokers == 5);
            // Five of a kind, 1/2/3 jokers applied
            return 7;
        }
        panic!("{} {}", counts.len(), jokers);
    }
}

impl PartialOrd for Hand {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        match self.calc_type_joker().partial_cmp(&other.calc_type_joker()) {
            Some(Ordering::Equal) => self.cards.partial_cmp(&other.cards),
            Some(ord) => Some(ord),
            None => None,
        }
    }
}

impl Ord for Hand {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap()
    }
}

fn main() -> anyhow::Result<()> {
    let input = std::fs::read_to_string("input.txt")?;
    let mut hands = input
        .lines()
        .map(|line| {
            let (hand, bid) = line.split_by(b' ');
            let cards = hand.chars().map(Card).collect();
            let bid = bid.to_u64();
            Hand { cards, bid }
        })
        .collect::<Vec<_>>();
    hands.sort();
    let ret = hands
        .into_iter()
        .enumerate()
        .map(|(index, card)| (index as u64 + 1) * card.bid)
        .sum::<u64>();
    println!("{ret}");

    Ok(())
}
// 249468791 too high
