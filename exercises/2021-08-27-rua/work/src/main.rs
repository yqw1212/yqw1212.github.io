use chacha20::{ChaCha20, Key, Nonce};
use chacha20::cipher::{NewCipher, StreamCipher, StreamCipherSeek};

fn main() {
    let mut data = [249u8, 115, 69, 5, 196, 159, 163, 213, 135, 95, 4, 149, 29, 223, 136, 114, 110, 1, 230, 35, 103, 186, 95, 213, 45, 187, 218, 114, 19, 231, 25, 230, 177, 16, 32, 218, 246, 216, 196, 186, 145, 179];
    let key = Key::from_slice(b"printf_llvm_version_printf_cargo");
    let nonce = Nonce::from_slice(b"_version_1.1");

    let mut cipher = ChaCha20::new(&key, &nonce);
    cipher.apply_keystream(&mut data);
    let mut flag = Vec::new();
    for i in data.iter() {
        flag.push(i ^ 0x80);
    }
    println!("{}",String::from_utf8(flag).unwrap());
}