import sys
import re

def s(line):
    return re.sub(r' {2,}', ' ', line)

def lift(lines):

    out = []    
    i = 0
    while i < len(lines):

        if i + 150 >= len(lines):
            out.append(lines[i])
            i += 1
            continue

        if all([
            "mov rax, 0" in s(lines[i]),
            "mov rbx, rax" in s(lines[i + 1]),
            "mov rcx, rax" in s(lines[i + 2]),
            "mov rdx, rax" in s(lines[i + 3]),
            "mov r8, " in s(lines[i + 4]),
            "mov r9, " in s(lines[i + 5]),
            "mov r10, " in s(lines[i + 6]),
        ]):
            src1 = lines[i + 4].split("offset ")[1]
            src2 = lines[i + 5].split("offset ")[1]
            dst = lines[i + 6].split("offset ")[1]

            if "add_carry_table" in s(lines[i + 9]) and "add_table" in s(lines[i + 12]):
                if all([
                    "*8]" in s(lines[i + 7 + 18*0]),
                    "*8+1]" in s(lines[i + 7 + 18*1]),
                    "*8+2]" in s(lines[i + 7 + 18*2]),
                    "*8+3]" in s(lines[i + 7 + 18*3]),
                    "*8+4]" in s(lines[i + 7 + 18*4]),
                    "*8+5]" in s(lines[i + 7 + 18*5]),
                    "*8+6]" in s(lines[i + 7 + 18*6]),
                    "*8+7]" in s(lines[i + 7 + 18*7]),
                    "*8+7], al" in s(lines[i + 150]),
                ]):
                    lifted = f"mov     [{dst}], [{src1}] + [{src2}]  ; qword add"
                    lifted = lines[i].split(" ")[0] + " " * 17 + lifted
                    out.append(lifted)
                    i += 151
                    continue

        if all([
            "mov rax, 0" in s(lines[i]),
            "mov rbx, rax" in s(lines[i + 1]),
            "mov r8, " in s(lines[i + 2]),
            "mov r9, " in s(lines[i + 3]),
            "mov r10, " in s(lines[i + 4]),
        ]):
            src1 = lines[i + 2].split("offset ")[1]
            src2 = lines[i + 3].split("offset ")[1]
            dst = lines[i + 4].split("offset ")[1]

            if "and_table" in s(lines[i + 7]):
                if all([
                    "*8]" in s(lines[i + 5 + 6*0]),
                    "*8+1]" in s(lines[i + 5 + 6*1]),
                    "*8+2]" in s(lines[i + 5 + 6*2]),
                    "*8+3]" in s(lines[i + 5 + 6*3]),
                    "*8+4]" in s(lines[i + 5 + 6*4]),
                    "*8+5]" in s(lines[i + 5 + 6*5]),
                    "*8+6]" in s(lines[i + 5 + 6*6]),
                    "*8+7]" in s(lines[i + 5 + 6*7]),
                ]):
                    lifted = f"mov     [{dst}], [{src1}] & [{src2}]  ; qword and"
                    lifted = lines[i].split(" ")[0] + " " * 17 + lifted
                    out.append(lifted)
                    i += 53
                    continue

            if "xor_table" in s(lines[i + 7]):
                if all([
                    "*8]" in s(lines[i + 5 + 6*0]),
                    "*8+1]" in s(lines[i + 5 + 6*1]),
                    "*8+2]" in s(lines[i + 5 + 6*2]),
                    "*8+3]" in s(lines[i + 5 + 6*3]),
                    "*8+4]" in s(lines[i + 5 + 6*4]),
                    "*8+5]" in s(lines[i + 5 + 6*5]),
                    "*8+6]" in s(lines[i + 5 + 6*6]),
                    "*8+7]" in s(lines[i + 5 + 6*7]),
                ]):
                    lifted = f"mov     [{dst}], [{src1}] ^ [{src2}]  ; qword xor"
                    lifted = lines[i].split(" ")[0] + " " * 17 + lifted
                    out.append(lifted)
                    i += 53
                    continue

            if "or_table" in s(lines[i + 7]) and not "xor" in s(lines[i + 7]):
                if all([
                    "*8]" in s(lines[i + 5 + 6*0]),
                    "*8+1]" in s(lines[i + 5 + 6*1]),
                    "*8+2]" in s(lines[i + 5 + 6*2]),
                    "*8+3]" in s(lines[i + 5 + 6*3]),
                    "*8+4]" in s(lines[i + 5 + 6*4]),
                    "*8+5]" in s(lines[i + 5 + 6*5]),
                    "*8+6]" in s(lines[i + 5 + 6*6]),
                    "*8+7]" in s(lines[i + 5 + 6*7]),
                ]):
                    lifted = f"mov     [{dst}], [{src1}] | [{src2}]  ; qword xor"
                    lifted = lines[i].split(" ")[0] + " " * 17 + lifted
                    out.append(lifted)
                    i += 53
                    continue

            if "cmp_eq_table" in s(lines[i + 8]):
                if all([
                    "r15]" in s(lines[i + 6 + 6*0]),
                    "r15+1]" in s(lines[i + 6 + 6*1]),
                    "r15+2]" in s(lines[i + 6 + 6*2]),
                    "r15+3]" in s(lines[i + 6 + 6*3]),
                    "r15+4]" in s(lines[i + 6 + 6*4]),
                    "r15+5]" in s(lines[i + 6 + 6*5]),
                    "r15+6]" in s(lines[i + 6 + 6*6]),
                    "r15+7]" in s(lines[i + 6 + 6*7]),
                ]):
                    lifted = f"mov     [{dst}], [{src1}] == [{src2}]  ; qword cmp eq"
                    lifted = lines[i].split(" ")[0] + " " * 17 + lifted
                    out.append(lifted)
                    i += 55
                    continue

        if all([
            "mov rax, 0" in s(lines[i]),
            "mov rbx, rax" in s(lines[i + 1]),
            "mov rdx, rax" in s(lines[i + 2]),
            "mov r8, " in s(lines[i + 3]),
            "mov r9, " in s(lines[i + 4]),
        ]):
            src1 = lines[i + 3].split("offset ")[1]
            src2 = lines[i + 4].split("offset ")[1]

            if "cmp_eq_table" in s(lines[i + 8]):
                if all([
                    "]" in s(lines[i + 6 + 6*0]),
                    "+1]" in s(lines[i + 6 + 6*1]),
                    "+2]" in s(lines[i + 6 + 6*2]),
                    "+3]" in s(lines[i + 6 + 6*3]),
                    "+4]" in s(lines[i + 6 + 6*4]),
                    "+5]" in s(lines[i + 6 + 6*5]),
                    "+6]" in s(lines[i + 6 + 6*6]),
                    "+7]" in s(lines[i + 6 + 6*7]),
                ]):
                    lifted = f"mov     dl, [{src1}] == [{src2}]  ; qword cmp eq (no r15)"
                    lifted = lines[i].split(" ")[0] + " " * 17 + lifted
                    out.append(lifted)
                    i += 55
                    continue

        if all([
            "mov rax, 0" in s(lines[i]),
            "mov r8, " in s(lines[i + 1]),
            "mov r10, " in s(lines[i + 2]),
        ]):
            src = lines[i + 1].split("offset ")[1]
            dst = lines[i + 2].split("offset ")[1]

            if "opposite_table" in s(lines[i + 4]):
                if all([
                    "*8]" in s(lines[i + 3 + 4*0]),
                    "*8+1]" in s(lines[i + 3 + 4*1]),
                    "*8+2]" in s(lines[i + 3 + 4*2]),
                    "*8+3]" in s(lines[i + 3 + 4*3]),
                    "*8+4]" in s(lines[i + 3 + 4*4]),
                    "*8+5]" in s(lines[i + 3 + 4*5]),
                    "*8+6]" in s(lines[i + 3 + 4*6]),
                    "*8+7]" in s(lines[i + 3 + 4*7]),
                ]):
                    lifted = f"mov     [{dst}], [{src}] ^ 0xFF  ; qword opposite"
                    lifted = lines[i].split(" ")[0] + " " * 17 + lifted
                    out.append(lifted)
                    i += 35
                    continue

        if all([
            ("mov rax, " in s(lines[i]) or "mov eax, " in s(lines[i])),
            "[" not in s(lines[i]),
            "mov r8, offset " in s(lines[i + 1]),
            "mov [r8+r15*8], rax" in s(lines[i + 2]),
        ]):
            src = s(lines[i]).split("ax, ")[1]
            dst = s(lines[i + 1]).split("offset ")[1]
            lifted = f"mov     [{dst}], {src}"
            lifted = lines[i].split(" ")[0] + " " * 17 + lifted
            out.append(lifted)
            i += 3
            continue

        if all([
            "mov rax, " in s(lines[i]),
            "[" not in s(lines[i]),
            "mov r8, offset " in s(lines[i + 1]),
            "mov al, [r8+r15]" in s(lines[i + 2]),
        ]):
            src = s(lines[i + 1]).split("offset ")[1]
            lifted = f"mov     al, byte ptr [{src}]"
            lifted = lines[i].split(" ")[0] + " " * 17 + lifted
            out.append(lifted)
            i += 3
            continue

        if all([
            "mov r8, offset " in s(lines[i]),
            "mov rax, 0" in s(lines[i + 1]),
            "mov [r8+8], rax" in s(lines[i + 2]),
            "mov rax, [r8+r15*8]" in s(lines[i + 3]),
            "mov r8, offset " in s(lines[i + 4]),
            "mov [r8+r15*8], rax" in s(lines[i + 5]),
        ]):
            src = s(lines[i]).split("offset ")[1]
            dst = s(lines[i + 4]).split("offset ")[1]
            lifted = f"mov     [{dst}], [{src}]"
            lifted = lines[i].split(" ")[0] + " " * 17 + lifted
            out.append(lifted)
            i += 6
            continue

        if all([
            "mov r8, offset " in s(lines[i]),
            "mov al, [r8+r15]" in s(lines[i + 1]),
            "mov r8, offset " in s(lines[i + 2]),
            "mov r8, [r8+r15*8]" in s(lines[i + 3]),
            "mov [r8+r15], al" in s(lines[i + 4]),
        ]):
            src = s(lines[i]).split("offset ")[1]
            dst = s(lines[i + 2]).split("offset ")[1]
            lifted = f"mov     byte [[{dst}]], [{src}]"
            lifted = lines[i].split(" ")[0] + " " * 17 + lifted
            out.append(lifted)
            i += 5
            continue

        if all([
            "mov r8, offset " in s(lines[i]),
            "mov r8, [r8+r15*8]" in s(lines[i + 1]),
            "mov al, [r8+r15]" in s(lines[i + 2]),
            "mov r8, offset " in s(lines[i + 3]),
            "mov [r8+r15], al" in s(lines[i + 4]),
        ]):
            src = s(lines[i]).split("offset ")[1]
            dst = s(lines[i + 3]).split("offset ")[1]
            lifted = f"mov     [{dst}], byte [[{src}]]"
            lifted = lines[i].split(" ")[0] + " " * 17 + lifted
            out.append(lifted)
            i += 5
            continue

        out.append(lines[i])
        i += 1
    
    return out


f = open(sys.argv[1], "r").read().split("\n")
f = lift(f)
print("\n".join(f))
