import math
import cmath


# to be updated
def reformat_fft_output(data):
    output = []
    for item in data:
        temp = ''
        sign = item[0]
        output_val = []
        for char in item:
            if (char.isdigit() or char == '.'):
                temp += char
            else:
                if (temp != ''):
                    output_val.append(sign + temp)
                    temp = ''
                if (char == '+'):
                    sign = '+'
                elif (char == '-'):
                    sign = '-'
                temp = ''
        output.append(complex((float)(output_val[0]), (float)(output_val[1])))
    return output


def get_ifft(data):
    if len(data) == 2:
        input1 = (data[0] + data[1]) / 2
        input2 = data[0] - input1
        return [round(input1.real), round(input2.real)]

    elif len(data) == 1:
        data[0] = round(data[0].real)
        return data

    else:
        inputs = [data[i:i + int(len(data)/4)] for i in range(0, len(data), (int(len(data)/4)))]

        X0 = inputs[0]
        X1 = inputs[1]
        X2 = inputs[2]
        X3 = inputs[3]

        sum_odd = []
        diff_odd = []
        fft_e1 = []
        fft_e2 = []

        for i in range(int(len(X0))):
            e_val = (X0[i] + X2[i]) / 2
            fft_e1.append(e_val)
            sum_odd.append(X0[i] - e_val)
            e_val2 = (X1[i] + X3[i]) / 2
            fft_e2.append(e_val2)
            diff_odd.append((X3[i] - e_val2)/1j)

        fft_e = fft_e1 + fft_e2

        twiddle_factors = []

        for k in range(len(data)):
            twiddle_factors += [cmath.exp(-2j*math.pi*k/len(data))]

        fft_a = []
        fft_b = []

        for i in range(len(sum_odd)):
            a_val = (sum_odd[i] + diff_odd[i]) / (2*twiddle_factors[i])
            b_val = (sum_odd[i] - (a_val*twiddle_factors[i]))/twiddle_factors[3*i]
            fft_a.append(a_val)
            fft_b.append(b_val)

        e = get_ifft(fft_e)
        a = get_ifft(fft_a)
        b = get_ifft(fft_b)

        orig_signal = []
        e_count = 0
        a_count = 0
        b_count = 0

        for i in range(len(data)):
            if i % 2 == 0:
                orig_signal.append(round(e[e_count].real))
                e_count += 1
            elif i % 4 == 1:
                orig_signal.append(round(a[a_count].real))
                a_count += 1
            elif i % 4 == 3:
                orig_signal.append(round(b[b_count].real))
                b_count += 1

    return orig_signal


if __name__ == '__main__':
    T = input()
    inputs = []
    outputs = []
    print(T)
    for i in range(int(T)):
        inputs.append(input())
        inputs[i] = inputs[i].split()
        outputs.append(get_ifft(reformat_fft_output(inputs[i][2:])))
        output_string = str(inputs[i][0]) + " "
        for j in range(int(inputs[i][0])):
            output_string = output_string + str(outputs[i][j]) + " "
        print(output_string)
