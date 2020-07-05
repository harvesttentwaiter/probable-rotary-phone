use std::fs::OpenOptions;
use std::io::prelude::*;
use std::time::SystemTime;

/** 
 * mod loggy; // for the separate file
 * use loggy::loggy; // use loggy() in loggy.rs
 * 
 * loggy(line!(), String::from("hi"));
 * loggy(line!(), format!("tuple{:?}", (3,4)));
 */
pub fn loggy(line :u32, msg :String) {
    // TODO move to diff dir, and diff module

    let mut file = OpenOptions::new()
        .write(true)
        .append(true)
        .create(true)
        .open("z.log")
        .unwrap();
    let unix_epoch :u64;
    match SystemTime::now().duration_since(SystemTime::UNIX_EPOCH) {
        Ok(n) => unix_epoch = n.as_secs(),
        Err(_) => panic!("SystemTime before UNIX EPOCH!"),
    }
    /*
    x /* nested comment */
    // always commented, can end multiline comment */    
    if let Err(e) = writeln!(file, "{} {} {} {}", 
            unix_epoch, 
            std::process::id(), 
            line, 
            msg) {

        eprintln!("Couldn't write to file: {}", e);
    }
}
