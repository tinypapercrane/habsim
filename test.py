from habsim import *

def main():
    loc = Location(1, 1)
    print(loc.getLat())

    rec = Record(1613552199, Location(90, 90), 100, 50, 25, 10)
    print(rec.time)
    x = Trajectory([rec])
    
    plot = ioutil.WebPlot()
    plot.origin(37, -122)
    plot.circle(30, -100, 1000, "hi")
    plot.save("plot.html")

    # rec2 = Record(2, Location(2, 2), 200, 100, 50, 25)
    # x.append(rec2)
    # print(x.data)
    # print(x.data[1].time)
    # print(x.startpoint().time)
    # print(x.duration())
    # print(x.length())
    # print(x.endtime())
    # print("asdf")

if __name__ == "__main__":
    main()