import random
class RandomProxy:
    def __init__(self) -> None:
        self.proxies = [
            "http://108.59.14.208:13081",
            "http://37.48.118.90:13081",
            "http://83.149.70.159:13081",
            "http://108.59.14.203:13081"
        ]

    def get_random_proxy(self):
        rand_num = random.randint(0,len(self.proxies) -1)
        return self.proxies[rand_num]




if __name__ == "__main__":
    rp = RandomProxy()
    
    for i in range(0,20):
        print(rp.get_random_proxy())