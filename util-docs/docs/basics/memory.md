# RAM

## Linux Memory Types
 1. physical memory - resource containing code and data.
 2. swap file - optional. Keeps (dirty) modified memory for later use if too many demands are made on physical memory.
 3. virtual memory - "unlimited" (...)

No matter the memory type - all are managed as **pages** (typically 4096 bytes)

## Memory monitoring tools

 1. `free (-m to show in MB)`

  | Header | Description |
  |--------|-------------|
  | total | indicates memory/physical RAM available for your machine. By default these numbers are in KB's |
  | used | indicates memory/RAM used by system. This includes buffers and cached data size as well |
  | free | indicates total **unused** RAM available for new process to run |
  | shared |  indicates shared memory. This column is obsolete and may be removed in future releases of free |
  | buffers | indicates total RAM buffered by different applications in Linux |
  | cached | indicates total RAM used for Caching of data for future purpose |
  | -/+ buffers/cache | shows _used_ column minus (_buffers_+_cached_) and _free_ column plus (_buffers_+_cached_). Why is that? Because when memory used is getting up to limit, the buffers + cache will be freed and used by demanding applications. This show most accurate memory usage. | 
  New version of `free`:
   - buff/cache: sum of buffers and cached
   - available: not exactly _free_ column plus (_buffers_+_cached_)  

 2. `top`
  
  | Header | Description |
  |--------|-------------|
  | virt | |
  | res | |
  | shr | |
  | %mem | |
