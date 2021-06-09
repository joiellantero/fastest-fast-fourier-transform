import math
import cmath

#function for rounding down with specific number of decimal places (from: https://kodify.net/python/math/round-decimals/)
def round_decimals_down(number:float, decimals:int=2):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor

def split_array(signal):
    e=[]
    a=[]
    b=[]

    for i in range(0, len(signal), 2):
        e += [signal[i]]

    for i in range(1, len(signal), 4):
        a += [signal[i]]

    for i in range(3, len(signal), 4):
        b += [signal[i]]
    
    return e, a, b

def get_fft(signal):
    #making sure the size of the signal is a power of 2
    while (math.ceil(math.log2(len(signal))) != math.floor(math.log2(len(signal)))):
        signal.append(0)
    
    #pre-computing twiddling factors
    twiddle_factors = []

    for k in range(len(signal)):
        twiddle_factors += [cmath.exp(-2j*math.pi*k/len(signal))]
        

    if len(signal) == 1:
        return [twiddle_factors[0]*signal[0]] #multiplied to twiddle_factor[0] so that the 
    elif len(signal) == 2:
        return [twiddle_factors[0]*(signal[0]+signal[1]), twiddle_factors[0]*(signal[0]-signal[1])]
    else:
        #do splitting of array
        e, a, b = split_array(signal)

        #doing recursion
        fft_e = get_fft(e)
        fft_a = get_fft(a)
        fft_b = get_fft(b)

        #pre-computing twiddling factors
        twiddle_factors = []

        for k in range(len(signal)):
            twiddle_factors += [cmath.exp(-2j*math.pi*k/len(signal))]
        
        #precomputing the sum and difference of the odd-indexed signal slices a and b
        sum_odd = []
        diff_odd = []

        for i in range(len(fft_a)): #note length of fft_a is always the same as fft_b since the length of the original signal was ensured to be a power of 2
            sum_odd += [twiddle_factors[i]*fft_a[i] + twiddle_factors[3*i]*fft_b[i]]
            diff_odd += [twiddle_factors[i]*fft_a[i] - twiddle_factors[3*i]*fft_b[i]]

        #computing each quarter of the DFT
        X0 = []
        X1 = []
        X2 = []
        X3 = []
        for i in range(int(len(signal)/4)):
            X0 += [fft_e[i]+sum_odd[i]]
            X1 += [fft_e[i+int(len(signal)/4)]-1j*diff_odd[i]]
            X2 += [fft_e[i]-sum_odd[i]]
            X3 += [fft_e[i+int(len(signal)/4)]+1j*diff_odd[i]]
        #note that indices for fft_e at quarters X1 and X3 start at N/4 and ends at N/2-1

        #merging DFT quarters
        return X0+X1+X2+X3


if __name__ == '__main__':
    #input
    input_signal = []
    T = int(input())
    for i in range(T):
        input_signal += [input()]

    #output
    output_signal = []
    for i in range(T):
        input_signal[i] = input_signal[i].split()
        input_signal[i] = [int(item) for item in input_signal[i]] #converting all items in list to int
        signal = []
        for j in range(1, input_signal[i][0]+1):
            signal += [input_signal[i][j]]
        output_signal += [get_fft(signal)]

        #formatting the complex number to real + imag*j with real and imag having six decimal places
        formatted_output = ''
        for k in range(len(output_signal[i])):
            if output_signal[i][k].real < 0: #checking if the real component is negative
                formatted_output += format(output_signal[i][k], '.6f') + " " #formatting found here: https://www.codegrepper.com/code-examples/python/how+to+add+extra+zeros+after+decimal+in+python 
            else: #if real component is positive, '+' sign will be added at the beginning of the number
                formatted_output += '+' + format(output_signal[i][k], '.6f') + " "
        print(input_signal[i][0], len(output_signal[i]), formatted_output)