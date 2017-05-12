"""
This is python code I wrote to use as reference to translate to our machine's architecture
"""

def eratosthenes(n):
    array_of_primes = [True for i in range(n+1)]
    array_of_primes[0] = False # 0 is not prime
    array_of_primes[1] = False # 1 is not prime

    first_prime = 2

    # Stop searching when first prime found ^ 2 exceeds n
    while first_prime * first_prime <= n:
        # Once we find first prime, cross out all multiples
        if array_of_primes[first_prime] == True:
            multiple_of_prime = first_prime * first_prime
            while multiple_of_prime <= n:
                array_of_primes[multiple_of_prime] = False
                multiple_of_prime = multiple_of_prime + first_prime
            first_prime = first_prime + 1
        # Look for next prime
        else:
            first_prime = first_prime + 1
    return array_of_primes


prime_bools = eratosthenes(255)

for i in range(len(prime_bools)):
    if prime_bools[i] == True:
        print(i)
