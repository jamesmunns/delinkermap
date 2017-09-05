# delinkermap

Process Rust Mapfiles produced by the linker.

You can see how much space in your binary is taken up by what library

Its not done yet. I might rewrite it in Rust.

## Usage

```bash
./delinkermap.py your_mapfile.map
```

## Example output

All sizes are in bytes. Each node shows the sum of all of its children.

```
# ...
reqwest - 11176
    client - 2180
        Client - 2036
            item:new size:0x7f4 loc:0x000000000011c7b0
        RequestBuilder - 144
            send - 144
                item:_LOC size:0x10 loc:0x00000000000069d8
                item:_LOC size:0x10 loc:0x0000000000006a68
                item:_LOC size:0x10 loc:0x0000000000006a80
                item:_LOC size:0x10 loc:0x0000000000006aa8
                item:_LOC size:0x14 loc:0x000000000040defc
                item:_LOC size:0x14 loc:0x000000000040df88
                item:_LOC size:0x14 loc:0x000000000040dfa4
                item:_LOC size:0x14 loc:0x000000000040dfd0
    response - 8996
        Decoder - 36
            from_hyper_response - 36
                item:_LOC size:0x10 loc:0x0000000000006bd0
                item:_LOC size:0x14 loc:0x000000000040e0b0
        Response - 8924
            item:json size:0x2038 loc:0x00000000000fc1c8
            item:json size:0x2a4 loc:0x0000000000106ac8
        new - 36
            item:_LOC size:0x10 loc:0x0000000000006b10
            item:_LOC size:0x14 loc:0x000000000040e028
ring - 1868
    digest - 1140
        Context - 1140
            item:update size:0x204 loc:0x0000000000225fa0
            item:finish size:0x270 loc:0x00000000002261a4
    hkdf - 48
        expand - 48
            item:_FILE_LINE_COL size:0x8 loc:0x000000000000c1d8
            item:_FILE_LINE_COL size:0x8 loc:0x000000000000c1e0
            item:_FILE_LINE_COL size:0x10 loc:0x0000000000414374
            item:_FILE_LINE_COL size:0x10 loc:0x0000000000414384
    rand - 680
        sysrand_or_urandom - 680
            item:fill size:0x2a8 loc:0x000000000022646c
```

## How do I get a mapfile from Rust?

In your crate, make a file called `./.cargo/config` (you might have to make the `.cargo` folder). Put this text in that file:

```
[build]
rustflags = ["-Clink-args=-Wl,-Map=/absolute/path/to/your/mapfile.map"]
```

Compile your program. Run that map file through this program.

## License

MIT License