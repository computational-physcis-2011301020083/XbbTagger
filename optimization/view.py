import argparse,math,os
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
parser.add_argument("--outname", dest='outname',  default="", help="outname")
args = parser.parse_args()

path=args.path
with open(path, "rU") as f:
    lines = f.readlines()

info = [x.strip() for x in lines]
for i in info:
  Loss=i.split(",")
  val_loss.append(Loss[4])
print min(val_loss)



