import utils.parameters as parameters
import utils.cryptoBase as cryptoBase


def fai1(prime1,prime2):
    hash_str = str(prime1)+str(prime2)
    if type(hash_str) == type(""):
        hash_str = cryptoBase.str_to_int(hash_str)
    return cryptoBase.hash_to_prime(hash_str, parameters.LAMBDA1)[0]
def fai2(prime1,prime2):
    hash_str = str(prime1)+str(prime2)
    if type(hash_str) == type(""):
        hash_str = cryptoBase.str_to_int(hash_str)
    return cryptoBase.hash_to_prime(hash_str, parameters.LAMBDA2)[0]
def h(msg):
    if type(msg) == type(""):
        msg = cryptoBase.str_to_int(msg)
    return cryptoBase.hash_to_prime(msg, parameters.LAMBDA2)[0]
def HPrime(msg):
    if type(msg) == type(""):
        msg = cryptoBase.str_to_int(msg)
    return cryptoBase.hash_to_prime(msg, parameters.LAMBDA)[0]
def Shamir(x,y,a,b,N,Fn):
    [_,alpha,beita] = cryptoBase.xgcd(a,b) 
    # if alpha<0:
    #     alpha += Fn
    # if beita<0:
    #     beita += Fn
    if alpha<0:
        sigma = pow(y, -alpha, N)
        sigma = cryptoBase.generate_mutual_prime(sigma, N)
    else:
        sigma = pow(y, alpha, N)    
    if beita<0:
        ans = pow(x, -beita,N)
        ans = cryptoBase.generate_mutual_prime(ans, N)
        sigma *= ans
    else:
        sigma *= pow(x, beita,N)    
    return sigma%N