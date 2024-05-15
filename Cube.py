import copy


class Edge:
    def __init__(self, number):
        self.number = number


class Cube:
    def __init__(self, top, bottom, front, back, left, right):
        self.neighbors = {"top": top, "bottom": bottom, "front": front, "back": back, "left": left, "right": right}

    def __init__(self, top,front):
        bottom, left, right, back = self.find_other_faces(top, front)
        self.neighbors = {"top": top, "bottom": bottom, "front": front, "back": back, "left": left, "right": right}
    def __str__(self):
        return str(self.neighbors)
    def pathBetweenTopAndEdge(self, givenEdge): #Itt a front irányába nézünk, és ez alapján fordítjuk át
        if givenEdge == "bottom":
            return ["up", "up"]
        if givenEdge == "back":
            return ["up"]

        elif givenEdge == "front":
            return ["down"]

        elif givenEdge == "left":
            return ["right"]

        elif givenEdge == "right":
            return ["left"]



    def switchByDirection(self, direction):
        tempTop = copy.deepcopy(self.neighbors["top"])
        tempBottom = copy.deepcopy(self.neighbors["bottom"])

        if direction == "up":
            self.neighbors["top"] = self.neighbors["back"]
            self.neighbors["bottom"] = self.neighbors["front"]
            self.neighbors["back"] = tempBottom
            self.neighbors["front"] = tempTop

        if direction == "down":
            self.neighbors["top"] = self.neighbors["front"]
            self.neighbors["bottom"] = self.neighbors["back"]
            self.neighbors["back"] = tempTop
            self.neighbors["front"] = tempBottom

        if direction == "left":
            self.neighbors["top"] = self.neighbors["right"]
            self.neighbors["bottom"] = self.neighbors["left"]
            self.neighbors["left"] = tempTop
            self.neighbors["right"] = tempBottom

        if direction == "right":
            self.neighbors["top"] = self.neighbors["left"]
            self.neighbors["bottom"] = self.neighbors["right"]
            self.neighbors["left"] = tempBottom
            self.neighbors["right"] = tempTop

    def find_other_faces(self, top, front):
        opposite_faces = {
            1: 6,
            6: 1,
            2: 5,
            5: 2,
            3: 4,
            4: 3
        }
        right_faces = {
            1: 3,
            3: 6,
            6: 4,
            4: 1
        }
        bottom = opposite_faces[top]
        back = opposite_faces[front]
        left = opposite_faces[right_faces[front]]
        right = right_faces[front]

        return bottom, left, right, back


