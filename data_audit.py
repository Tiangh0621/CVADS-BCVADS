import init
import utils.parameters as parameter
import json
import utils.func_Base as func_Base
import utils.cryptoBase as cryptoBase
import data_append
import random
CHAL_NUM = parameter.CHAL_NUM
FILE = parameter.file_url
DATA_SIZA = parameter.DATA_SIZA

class User(data_append.User):
    def __init__(self, sk) -> None:
        super().__init__(sk)

class Audit():
    def __init__(self, cnt, name, u, sigma_jian, fai_n, N, u_list, g,e, h_list) -> None:
        self.cnt = cnt
        self.name = name
        self.u = u
        self.sigma_jian = sigma_jian
        self.fai_n = fai_n
        self.N = N
        self.u_list = u_list
        self.g = g
        self.e = e
        self.h_list = h_list
    def challenge(self):
        r1 = random.randint(0, parameter.LAMBDA2)
        r2 = random.randint(0, parameter.LAMBDA2)
        z = []
        for i in range(0,CHAL_NUM):
            num = random.randint(0, self.cnt-1)
            z.append(num)
        z = [1,5]
        r1 = 10
        r2 = 100
        self.z = z
        self.r2 = r2

        return (z,r1,r2)
    def verify(self, reply):
        (rou, F, y) = reply
        sigma_list = []
        b = []
        count = 0
        for i in self.z:
            us = func_Base.HPrime(json.dumps([self.name, i]))
            u_re = cryptoBase.generate_mutual_prime(us, self.fai_n)
            us_bar = self.u*u_re %self.fai_n
            x = pow(self.sigma_jian, us_bar, self.N)
            Fs_re = cryptoBase.generate_mutual_prime(F[count], self.N)
            x = x*Fs_re %self.N
            sigma = func_Base.Shamir(x,y[count],us,us_bar,self.N,self.fai_n)
            sigma_list.append(sigma)
            b.append(func_Base.fai2(i, self.r2))
            count += 1
        # b = [1,1]
        tag = 1
        count = 0
        for i in self.z:
            tem_tag = pow(sigma_list[count], self.e*self.u_list[i], self.N)
            tem_tag2 = pow(self.g, self.h_list[i], self.N)
            print(tem_tag2)
            tem_tag2 = cryptoBase.generate_mutual_prime(tem_tag2, self.N)
            tem_tag *= tem_tag2%self.N
            tem_tag = pow(tem_tag, b[count], self.N)
            tag *= tem_tag %self.N
            count += 1
        return tag%self.N == pow(self.g, rou, self.N)




    


class Server(data_append.Server):
    def __init__(self, pk) -> None:
        super().__init__(pk)
    def data_audit(self, chal):
        (z,r1,r2) = chal
        F = []
        y = []
        rou = 0
        for i in z:
            si = func_Base.fai1(i, r1)
            bi = func_Base.fai2(i, r2)
            # bi = 1
            fi = 0
            for count in range(0, len(self.data)):
                if count != i:
                    msg = cryptoBase.str_to_int(self.data[count])
                    tem_value = self.h_list[count]+msg
                    for count2 in range(0, len(self.u_list)):
                        if count2 != count and count2 != i:
                            tem_value *= self.u_list[count2]
                    fi += tem_value
            Fi = pow(self.gd, fi, self.N)
            yi = pow(self.gd, (self.h_list[i]+msg), self.N)
            msg = cryptoBase.str_to_int(self.data[i])
            rou += msg*bi
            F.append(Fi)
            y.append(yi)
        return (rou, F, y)




        


def main():
    (sk,pk) = init.init()
    user = User(sk)
    server = Server(pk)
    with open(FILE, "r") as f:
        m = f.read()
    (m_list, sigma_list) = user.append(m)
    server.append(m_list, sigma_list)
    i = 0
    auditor = Audit(user.cnt, user.name, user.u, user.sigma_jian, (user.p-1)*(user.q-1), user.N, user.u_list, user.g, user.e, user.h_list)
    chal = auditor.challenge()
    reply = server.data_audit(chal)
    ans = auditor.verify(reply=reply)
    print(ans)

    


if __name__ == '__main__':
    main()