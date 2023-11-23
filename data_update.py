import init
import utils.parameters as parameter
import json
import utils.func_Base as func_Base
import utils.cryptoBase as cryptoBase
import data_query
FILE = parameter.file_url
DATA_SIZA = parameter.DATA_SIZA

class User(data_query.User):
    def __init__(self, sk) -> None:
        super().__init__(sk)
    def data_query(self, msg, Fs,i):
        super().data_query(msg, Fs, i)
        msg = cryptoBase.str_to_int(msg)
        us = func_Base.HPrime(json.dumps([self.name, i]))
        u_re = cryptoBase.generate_mutual_prime(us, (self.p-1)*(self.q-1))
        us_bar = self.u*u_re %((self.p-1)*(self.q-1))
        x = pow(self.sigma_jian, us_bar, self.N)
        Fs_re = cryptoBase.generate_mutual_prime(Fs, self.N)
        x = x*Fs_re %self.N

        y = pow(self.g, (self.h_list[i]+msg)*self.d, self.N)

        u = func_Base.HPrime(json.dumps([self.name, i]))

        sigma_s = func_Base.Shamir(x,y,us,us_bar,self.N,(self.p-1)*(self.q-1))

        tag1 = pow(sigma_s, self.e*self.u_list[i], self.N)
        tag2 = pow(self.g, self.h_list[i]+msg, self.N)

        self.s = i
        self.ms = msg
        self.sigma_s = sigma_s
        self.hs = self.h_list[i]
        self.us = us
        return tag1 ==tag2

    def data_update(self, m_new):
        msg_new = cryptoBase.str_to_int(m_new)
        W = json.dumps([self.name, self.s, func_Base.h(msg_new)])
        hs = func_Base.h(W)
        u_re = cryptoBase.generate_mutual_prime(self.us, (self.p-1)*(self.q-1))
        sigma_s = pow(self.g, (hs+msg_new)*u_re*self.d, self.N)
        sigma_re = cryptoBase.generate_mutual_prime(self.sigma_s, self.N)
        self.sigma_jian = self.sigma_jian*sigma_re*sigma_s%self.N
        # print(self.sigma_jian)
        return (self.s, m_new, sigma_s)


    


class Server(data_query.Server):
    def __init__(self, pk) -> None:
        super().__init__(pk)
    def data_update(self, quest):
        (s, m_new, sigma_s) = quest
        msg_new = cryptoBase.str_to_int(m_new)
        W = json.dumps([self.name, s, func_Base.h(msg_new)])
        hs = func_Base.h(W)
        tag1 = pow(sigma_s, self.e*self.u_list[s], self.N)
        tag2 = pow(self.g, hs+msg_new, self.N)
        print(tag1 ==tag2)
        if tag1 == tag2:
            self.data[s] = m_new
            sigma_re = cryptoBase.generate_mutual_prime(self.sigma_list[s], self.N)
            self.sigma_jian = self.sigma_jian*sigma_re*sigma_s%self.N  
            self.sigma_list[s] = sigma_s
        # print(self.sigma_jian)

        return tag1 ==tag2


        


def main():
    (sk,pk) = init.init()
    user = User(sk)
    server = Server(pk)
    with open(FILE, "r") as f:
        m = f.read()
    (m_list, sigma_list) = user.append(m)
    server.append(m_list, sigma_list)
    i = 5
    (data, Fs) = server.data_query(i)
    ans = user.data_query(data, Fs,i)
    quest = user.data_update("aaaaaaaaaaaaaaaaaaaa")
    server.data_update(quest)
    print(ans)
    


if __name__ == '__main__':
    main()