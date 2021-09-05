# Tools
`dd`  
`hdparm`  
`iotop`  

# FIO
Tool for benchmarking IO. Can spawn multiple threads performing different kind of work.

Options worth mentioning:  
`direct=<bool>` - uses non-buffered IO (`O_DIRECT`)

## Testing scenarios

### Random read-write  
`fio --randrepeat=1 --ioengine=libaio --direct=1 --gtod_reduce=1 --name=test --filename=random_read_write.fio --bs=4k --iodepth=64 --size=4G --readwrite=randrw --rwmixread=75`

# References
 1. https://dotlayer.com/how-to-use-fio-to-measure-disk-performance-in-linux/
 2. https://wiki.mikejung.biz/Benchmarking#Fio_Test_Options_and_Examples
