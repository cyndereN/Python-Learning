def moveTower(height, frompole, withpole, topole):
    if height>=1:
        moveTower(height-1,frompole,topole,withpole)
        moveDisk(height,frompole,topole)
        moveTower(height-1,withpole,frompole,topole)

def moveDisk(disk, frompole, topole):
    print (f"Moving disk[{disk}] from {frompole} to {topole}")

moveTower(3,"#1","#2","#3")
