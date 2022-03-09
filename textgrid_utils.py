from typing import Tuple


def write_box(file, id: int, start: float, end: float, text: str) -> None:
    file.write("\t\tintervals[" + str(id) + "]:\n")
    file.write("\t\t\txmin = " + str(start) + "\n")
    file.write("\t\t\txmax = " + str(end) + "\n")
    file.write('\t\t\ttext = "' + text + '"\n')

def write_textgrid(filename, first_tier, second_tier, x_min, xmax):
    fout = open(filename, "w", encoding="utf8")
    header = (
        'File type = "ooTextFile"\nObject class = "TextGrid"\n\nxmin = '
        + str(x_min)
        + "\nxmax = "
        + str(xmax)
        + "\ntiers? <exists> \nsize = 2\n"
    )
    fout.write(header)

    # First tier
    firstTierHeader = (
        'item []: \n\titem [1]:\n\t\tclass = "IntervalTier"\n\t\tname = "Words" \n\t\txmin = 0 \n\t\txmax = '
        + str(xmax)
        + "\n"
    )
    fout.write(firstTierHeader)
    fout.write("\t\tintervals: size = " + str(len(first_tier)) + "\n")
    
    prev = x_min
    for i, info in enumerate(first_tier):
        write_box(fout, i + 1, prev, info[0], info[1])
        prev = info[0]
    
    # Second tier
    secondTierHeader = (
        '\titem [2]:\n\t\tclass = "IntervalTier"\n\t\tname = "Phones" \n\t\txmin = '
        + str(x_min)
        + "\n\t\txmax = "
        + str(xmax)
        + "\n"
    )
    fout.write("\n" + secondTierHeader)
    fout.write("\t\tintervals: size = " + str(len(second_tier)) + "\n")
    prev = x_min
    for i, info in enumerate(second_tier):
        write_box(fout, i + 1, prev, info[0], info[1])
        prev = info[0]

    fout.close()
