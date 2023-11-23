import init
import utils.parameters as parameter
import json
import utils.func_Base as func_Base
import utils.cryptoBase as cryptoBase
FILE = parameter.file_url
DATA_SIZA = parameter.DATA_SIZA

class User():
    def __init__(self, sk) -> None:
        self.p = sk["p"]
        self.q = sk["q"]
        self.d = sk["d"]
        self.g = sk["g"]
        self.e = sk["e"]
        self.cnt = sk["cnt"]
        self.u = sk["u"]
        self.name = sk["NAME"]
        self.N = self.p*self.q
        self.sigma_jian = sk["sigma_jian"]

    def append(self, msg):
        self.W_list = []
        self.h_list = []
        self.u_list = []
        self.sigma_list = []
        m_list =  [msg[i:i+DATA_SIZA] for i in range (0, len(msg), DATA_SIZA) ]  
        self.m_list = m_list
        for i in range(0,len(m_list)):
            msg = cryptoBase.str_to_int(m_list[i])
            W = json.dumps([self.name, i, func_Base.h(msg)])
            hi = func_Base.h(W)
            u = func_Base.HPrime(json.dumps([self.name, i]))
            u_re = cryptoBase.generate_mutual_prime(u, (self.p-1)*(self.q-1))
            # u_re = 1
            # self.d = 1
            sigma = pow(self.g, (hi+msg)*u_re*self.d, self.N)
            re = cryptoBase.generate_mutual_prime((hi+msg)*self.d, self.N)
            self.u *= u
            self.cnt += 1
            self.sigma_jian *= sigma
            self.W_list.append(W)
            self.h_list.append(hi)
            self.u_list.append(u)
            self.sigma_list.append(sigma)

        return (m_list,self.sigma_list)
    


class Server():
    def __init__(self, pk) -> None:
        self.N = pk["N"]
        self.g = pk["g"]
        self.e = pk["e"]
        self.name = pk["NAME"]
        self.sigma_jian = pk["sigma_jian"]
        self.gd = pk["gd"]
        self.h_list = []
        self.u_list = []
    def append(self, m_list, sigma_list):
        self.sigma_list = sigma_list
        self.data = m_list
        for i in range(0, len(sigma_list)):
            msg = cryptoBase.str_to_int(m_list[i])
            W = json.dumps([self.name, i, func_Base.h(msg)])
            hi = func_Base.h(W)
            ui = func_Base.HPrime(json.dumps([self.name, i]))
            self.h_list.append(hi)
            self.u_list.append(ui)
            tag1 = pow(sigma_list[i], self.e*ui, self.N)
            tag2 = pow(self.g, hi+msg, self.N)
            if tag1 != tag2:
                print("error")
                return False
            else:
                self.sigma_jian *=  sigma_list[i]
        return True
        


def main():
    (sk,pk) = init.init()
    user = User(sk)
    server = Server(pk)
    with open(FILE, "r") as f:
        m = f.read()
    (m_list, sigma_list) = user.append(m)
    server.append(m_list, sigma_list)

if __name__ == '__main__':
    main()