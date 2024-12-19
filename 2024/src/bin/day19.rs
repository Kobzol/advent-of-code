use bstr::{BStr, BString, ByteSlice};
use hashbrown::HashMap;
use indicatif::ParallelProgressIterator;
use rayon::iter::IntoParallelRefIterator;
use rayon::iter::ParallelIterator;
use indicatif::ProgressIterator;

fn main() -> anyhow::Result<()> {
    let file = std::fs::read_to_string("input.txt")?;

    let mut lines = file.lines();
    let patterns: Vec<BString> = lines.next().unwrap().replace(" ", "").split(',').map(|s| s.to_string().into()).collect();
    let towels: Vec<BString> = lines.skip(1).map(|s| s.to_string().into()).collect();

    let mut cache: HashMap<&[u8], u64> = HashMap::new();
    let possible = towels
        // .par_iter()
        .iter()
        .map(|towel| count_possibilities(towel.as_bstr(), &patterns, &mut cache))
        .progress()
        .sum::<u64>();
    println!("{possible}");

    Ok(())
}

fn count_possibilities<'a>(towel: &'a BStr, patterns: &[BString], cache: &mut HashMap<&'a [u8], u64>) -> u64 {
    if let Some(count) = cache.get(towel.as_bytes()) {
        return *count;
    }
    if towel.is_empty() {
        return 1;
    }

    let mut count = 0;
    for pattern in patterns {
        if let Some(rest) = towel.strip_prefix(pattern.as_slice()) {
            count += count_possibilities(BStr::new(rest), patterns, cache);
        }
    }
    cache.insert(towel.as_bytes(), count);

    count
}
