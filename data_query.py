import init
import utils.parameters as parameter
import json
import utils.func_Base as func_Base
import utils.cryptoBase as cryptoBase
import data_append
FILE = parameter.file_url
DATA_SIZA = parameter.DATA_SIZA

class User(data_append.User):
    def __init__(self, sk) -> None:
        super().__init__(sk)
    def data_query(self, msg, Fs,i):
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
        return tag1 ==tag2


    


class Server(data_append.Server):
    def __init__(self, pk) -> None:
        super().__init__(pk)
    def data_query(self, i):
        value = 0
        for count in range(0, len(self.data)):
            if count != i:
                msg = cryptoBase.str_to_int(self.data[count])
                tem_value = self.h_list[count]+msg
                for count2 in range(0, len(self.u_list)):
                    if count2 != count and count2 != i:
                        tem_value *= self.u_list[count2]
                value += tem_value
        value = pow(self.gd, value, self.N)
        return (self.data[i], value)

        


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
    print(ans)
    


if __name__ == '__main__':
    main()