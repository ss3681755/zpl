# References
1. [Nasm Docs](https://www.nasm.us/doc/nasmdoci.html)
2. [Nasm tutorial](https://cs.lmu.edu/~ray/notes/nasmtutorial/)
3. [Calling Conventions](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#calling-conventions)
4. [NASM Instructions](https://www.perplexity.ai/search/319657e2-1956-4f7e-b77f-2c68e2c2df73?s=u)

# Build
1. Download nasm.
```sh
$ make setup
```
2. Compile `zpl` code to create an executable and **nasm** assembly code.
```sh
$ make -B tests/add.zpl
```
3. To run all the tests.
```sh
$ make test
```
4. To clean up the generated assembly, object files and test output.
```sh
$ make clean
```
