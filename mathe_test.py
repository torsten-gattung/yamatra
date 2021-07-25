from fractions import Fraction
import random
import datetime


class Test():
    """
    Generic Test Class
    """
    def __init__(self, max_time):
        self.test_type = ''
        self.punkte = 0
        self.max_time = datetime.timedelta(seconds=max_time)

    def punktabzug(self):
        if self.punkte > 4:
            self.punkte = 3
        else:
            self.punkte -= 1
            if self.punkte < 0:
                self.punkte = 0
    
    def ok(self, z):
        try:
            z = int(z)
            return z == self.result
        except ValueError:
            return False;

    def get_points(self, duration):
        if duration > self.max_time+self.max_time:
            return 0
        if duration > self.max_time:
            return self.punkte - 1
        else:
            return self.punkte
        

class Multiplikation(Test):
    def __init__(self, max_time=10):
        super().__init__(max_time)
        self.test_type = 'Multiplikation'
        
        self.x = random.randint(2,20)
        self.y = random.randint(2,20)

        if self.x > 10 and self.x != 20: 
            self.punkte = 2
        else:
            self.punkte = 1
        if self.y > 10 and self.y != 20:
            self.punkte += 2
        else:
            self.punkte += 1
        self.question = f"Wieviel ist {self.x} mal {self.y}?"
        self.text = f"{self.x} ⋅ {self.y}: "
        self.result = self.x * self.y
    
class Division(Test):
    def __init__(self, max_time=20):
        super().__init__(max_time)
        self.test_type = 'Division'
        self.x = random.randint(2,20)
        self.y = random.randint(2,20)

        if self.x > 10 and self.x != 20: 
            self.punkte = 3
        else:
            self.punkte = 2
        
        if self.y > 10 and self.y != 20:
            self.punkte += 2
        else:
            self.punkte += 1

        self.question = f"Wieviel ist {self.x * self.y} geteilt durch {self.y}?"
        self.text = f"{self.x*self.y} : {self.y}: "
        self.result = self.x

class Bruchrechnung(Test):
    def __init__(self, max_time=20):
        super().__init__(max_time)
        self.nenner_names = ["halbe", "drittel", "viertel", "fünftel", "sechstel", "siebtel", "achtel", "neuntel", "zehntel", "elftel", "zwölftel"]
        self.test_type = 'Bruchrechnung'

        self.zaehler1 = random.randint(1,10)
        self.nenner1 = random.randint(2,10)

        self.zaehler2 = random.randint(1,10)
        self.nenner2 = random.randint(2,10)
        self.operation = random.randint(1,3)
        
        if self.nenner1 != self.nenner2:
            self.punkte = 4
        else:
            self.punkte = 3
        
        if self.operation == 3: #Mult
            self.punkte += 1
            a = self._nenner(self.nenner1)
            b = self._nenner(self.nenner2)
            self.question = f"Wieviel ist {self.zaehler1} {a} mal {self.zaehler2} {b}?"
            s = f"            {self.zaehler1:2}      {self.zaehler2:2}\n"
            s+= f"Wieviel ist ---  *  ---?\n"
            s+= f"            {self.nenner1:2}      {self.nenner2:2}\n"
            self.text = s
            self.result = Fraction(self.zaehler1, self.nenner1) * Fraction(self.zaehler2,self.nenner2)
        
        elif self.operation == 2: #Sub
            #self.punkte += 1
            a = self._nenner(self.nenner1)
            b = self._nenner(self.nenner2)
            self.question = f"Wieviel ist {self.zaehler1} {a} minus {self.zaehler2} {b}?"
            s = f"            {self.zaehler1:2}      {self.zaehler2:2}\n"
            s+= f"Wieviel ist ---  —  ---?\n"
            s+= f"            {self.nenner1:2}      {self.nenner2:2}\n"
            self.text = s
            self.result = Fraction(self.zaehler1, self.nenner1) - Fraction(self.zaehler2,self.nenner2)
        else: #Add
            a = self._nenner(self.nenner1)
            b = self._nenner(self.nenner2)
            self.question = f"Wieviel ist {self.zaehler1} {a} + {self.zaehler2} {b}?"
            s = f"            {self.zaehler1:2}      {self.zaehler2:2}\n"
            s+= f"Wieviel ist ——— +  ———?\n"
            s+= f"            {self.nenner1:2}      {self.nenner2:2}\n"
            self.text = s
            self.result = Fraction(self.zaehler1, self.nenner1) + Fraction(self.zaehler2,self.nenner2)

    
    def _nenner(self, n: int)->str:
        if n < 12:
            return self.nenner_names[n-2]
        else:
            return str(n)

    def ok(self, z):
        return Fraction(z) == self.result

