from collections import defaultdict

class Data_point():
    """
    Simple class to represent a point of test data
    pkt is the network packet to send to the Method
    malicious is the actual value of whether the packet is malicious
    prediction is the Method's determination of whether the packet is malicious
    """
    def __init__(self, pkt, malicious, prediction=None):
        self.pkt = pkt
        self.malicious = malicious
        self.prediction = prediction

    def is_malicious(self):
        return self.malicious

    def is_benign(self):
        return not self.malicious

    def is_false_positive(self):
        return not self.malicious and self.prediction

    def is_false_negative(self):
        return self.is_classified() and \
            (self.malicious and not self.prediction)

    def is_prediction_correct(self):
        return self.malicious == self.prediction

    def is_classified(self):
        return self.prediction is not None

class Test_data():
    def __init__(self, data_points):
        self.dps = data_points

        # build index to make dp_for_pkt faster
        self.index = defaultdict(list)
        for i, dp in enumerate(self.dps):
            self.index[dp.pkt.time].append(i)

    def false_positive_dps(self):
        return list(filter(lambda dp: dp.is_false_positive(), self.dps))

    def false_negative_dps(self):
        return list(filter(lambda dp: dp.is_false_negative(), self.dps))

    def correct_dps(self):
        return list(filter(lambda dp: dp.is_prediction_correct(), self.dps))

    def malicious_dps(self):
        return list(filter(lambda dp: dp.is_malicious(), self.dps))

    def benign_dps(self):
        return list(filter(lambda dp: dp.is_benign(), self.dps))

    def completed_dps(self):
        return list(filter(lambda dp: dp.is_classified(), self.dps))

    def dp_for_pkt(self, pkt):
        possibilities = self.index[pkt.time]
        match = list(filter(lambda i: self.dps[i].prediction == None, possibilities))
        # assumes pkts with same timestamps (if they exist) have the same label
        return self.dps[match[0]] if match else None
