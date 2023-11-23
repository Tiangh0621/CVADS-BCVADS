from utils import func_Base, cryptoBase, parameters
SEED = 123
NAME = "user"
def init():
    p = cryptoBase.hash_to_prime(SEED,parameters.LAMBDA/2)[0]
    q = cryptoBase.hash_to_prime(SEED+SEED,parameters.LAMBDA/2)[0]
    N = p*q
    fai_N = (p-1)*(q-1)
    g = cryptoBase.generate_squre_root(N)
    e = cryptoBase.hash_to_prime(SEED,parameters.LAMBDA+parameters.LAMBDA1+parameters.LAMBDA2+2)[0]
    d = cryptoBase.generate_mutual_prime(e,fai_N)
    cnt = 0
    gd = pow(g, d, N)
    sigma_jian = 1
    u = 1
    # sk = (p,q,d,g,cnt,u)
    sk = {"p":p,"q":q,"d":d,"g":g,"cnt":cnt,"u":u, "NAME":NAME,"sigma_jian":sigma_jian,"e":e}
    pk = {"N":N,"g":g,"e":e,"gd":gd,"NAME":NAME,"sigma_jian":sigma_jian}
    # pk = (N,g,e,gd,NAME,sigma_jian)
    return (sk,pk)



def main():
    (sk,pk) = init()
    print(sk)
    print(pk)
if __name__ == '__main__':
    main()