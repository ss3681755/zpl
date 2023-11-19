# References
1. [Nasm tutorial](https://cs.lmu.edu/~ray/notes/nasmtutorial/)
2. [Calling Conventions](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#calling-conventions)

# Build
1. Download nasm.
```sh
$ make setup
```
2. Generate the **nasm** assembly code.
```sh
$ make tests/add.zpl asm
```
3. Create a binary executable.
```sh
$ make tests/add.zpl compile
```
4. To compile and run.
```sh
$ make tests/add.zpl run
```
5. To verify the program output against a file. The generated output can be found in `test.out`.
```sh
$ make PROGRAM=tests/add.zpl OUTPUT=tests/add.out verify
```
6. To run all the tests.
```sh
$ make test
```
7. To clean up the generated assembly, object files and test output.
```sh
$ make clean
```
