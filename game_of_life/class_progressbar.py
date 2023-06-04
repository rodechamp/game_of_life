"""Progressbar class, to keep track how far the code is in calculation for
long calculations
"""

class ProgressBar():
    def __init__(self, 
            total, 
            prefix = 'Progress:', 
            suffix = '', 
            decimals = 1, 
            length = 30, 
            fill = '█', 
            printEnd = "\r"
            ) -> None:
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.printEnd = printEnd
        
        return None
    

    def print(self, iteration) -> None:
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (iteration / float(self.total)))
        
        filledLength = int(self.length * iteration // self.total)
        bar = self.fill * filledLength + '-' * (self.length - filledLength)

        print(f'\r{self.prefix} |{bar}| {percent}% {self.suffix}', end = self.printEnd)

        if iteration == self.total:
            print()

        return None

