.SILENT:
.PHONY: sample
sample: gen run
	make clean

gen:
	python3 main.py

run: out.asm runtime.asm
	nasm -felf64 out.asm && nasm -felf64 runtime.asm && ld out.o runtime.o -o out && ./out

test:
	python3 tester.py
	make clean

clean:
	rm runtime.o out out.asm out.o test.out