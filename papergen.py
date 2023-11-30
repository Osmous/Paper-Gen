
from reportlab.pdfgen import canvas
import reportlab.lib.pagesizes as pagesizes
from reportlab.lib.colors import Color
import reportlab.lib.units as units
import argparse

pagesizemap={
    "A0":pagesizes.A0,
    "A1":pagesizes.A1,
    "A2":pagesizes.A2,
    "A3":pagesizes.A3,
    "A4":pagesizes.A4,
    "A5":pagesizes.A5,
    "A6":pagesizes.A6,
    "A7":pagesizes.A7,
    "A8":pagesizes.A8,
    "A9":pagesizes.A9,
    "A10":pagesizes.A10,
    "B0":pagesizes.B0,
    "B1":pagesizes.B1,
    "B2":pagesizes.B2,
    "B3":pagesizes.B3,
    "B4":pagesizes.B4,
    "B5":pagesizes.B5,
    "B6":pagesizes.B6,
    "B7":pagesizes.B7,
    "B8":pagesizes.B8,
    "B9":pagesizes.B9,
    "B10":pagesizes.B10,
    "C0":pagesizes.C0,
    "C1":pagesizes.C1,
    "C2":pagesizes.C2,
    "C3":pagesizes.C3,
    "C4":pagesizes.C4,
    "C5":pagesizes.C5,
    "C6":pagesizes.C6,
    "C7":pagesizes.C7,
    "C8":pagesizes.C8,
    "C9":pagesizes.C9,
    "C10":pagesizes.C10,
    "LETTER":pagesizes.LETTER,
    "LEGAL":pagesizes.LEGAL,
    "ELEVENSEVENTEEN":pagesizes.ELEVENSEVENTEEN,
    "JUNIOR_LEGAL":pagesizes.JUNIOR_LEGAL,
    "HALF_LETTER":pagesizes.HALF_LETTER,
    "GOV_LETTER":pagesizes.GOV_LETTER,
    "GOV_LEGAL":pagesizes.GOV_LEGAL,
    "TABLOID":pagesizes.TABLOID,
    "LEDGER":pagesizes.LEDGER
} 


def get_coords(centercoords,spacing,counter):
    # function to get square coordinate grid. used for everything
    # tri grid based on this grid but is edited in their respective function
    i=1
    x= [centercoords[0]]
    while (i<=counter[0]):
        x.append(centercoords[0]-i*spacing)
        x.append(centercoords[0]+i*spacing)
        x.sort()
        i+=1
    i=1
    y= [centercoords[1]]
    while (i<=counter[1]):
        y.append(centercoords[1]-i*spacing)
        y.append(centercoords[1]+i*spacing)
        y.sort()
        i+=1
    return x,y


def draw_dots(x,y,weight,pdf):
    # draw dot grid based on coordinates
    for x1 in x:
        for y1 in y:
            # +- weight/2 to get bottom left and top right eclipse box corners coordinates, centered arnd original coordinate grid
            pdf.ellipse(x1-weight/2,y1-weight/2, x1+weight/2,y1+weight/2, stroke=1, fill=1)
    return

def draw_hrule(x,y,pdf):
    # draw horizontal lines
    lines=[]
    for i in y:
        lines.append([x[0],i,x[-1],i])
    pdf.lines(lines)
    return

def draw_vrule(x,y,pdf):
    # draw vertical lines
    lines=[]
    for i in x:
        lines.append([i,y[0],i,y[-1]])
    pdf.lines(lines)
    return

def draw_grid(x,y,pdf):
    # draw line grid
    draw_vrule(x,y,pdf)
    draw_hrule(x,y,pdf)
    return

def draw_htridots(x,y,weight,spacing,pdf):
    # draw horizontal aligned alternating dot grid
    # xholder used to store the alterating coordinates 
    xholder=[i+spacing/2 for i in x]
    xholder.pop()
    for i,y1 in enumerate(y):
        if i%2 == 1:
            for x1 in x:
                pdf.ellipse(x1-weight/2,y1-weight/2, x1+weight/2,y1+weight/2, stroke=1, fill=1)
        else:
            for x1 in xholder:
                pdf.ellipse(x1-weight/2,y1-weight/2, x1+weight/2,y1+weight/2, stroke=1, fill=1)
    return

def draw_vtridots(x,y,weight,spacing,pdf):
    # draw vertical aligned alternating dot grid
    # yholder used to store the alterating coordinates 
    yholder=[i+spacing/2 for i in y]
    yholder.pop()
    for i,x1 in enumerate(x):
        if i%2 == 1:
            for y1 in y:
                pdf.ellipse(x1-weight/2,y1-weight/2, x1+weight/2,y1+weight/2, stroke=1, fill=1)
        else:
            for y1 in yholder:
                pdf.ellipse(x1-weight/2,y1-weight/2, x1+weight/2,y1+weight/2, stroke=1, fill=1)
    return


def draw_htriline(x,y,spacing,pdf):
    # draw horizontal aligned alternating line grid
    # same as htridot but lines lol
    xholder=[i+spacing/2 for i in x]
    xholder.pop()
    lines=[]
    i=0
    while i<len(y)-1:
        if i %2==1:
            # handle less coordinates to more coordinates draw lines.
            for c,x1 in enumerate(xholder):
                lines.append([x1,y[i],x[c],y[i+1]])
                lines.append([x1,y[i],x[c+1],y[i+1]])
            # draw dividing line
            draw_hrule(xholder,[y[i]],pdf)
            
        else:
            # handle more coordinates to less coordinates draw lines.
            for c,x1 in enumerate(x):
                if c ==0:
                    lines.append([x1,y[i],xholder[c],y[i+1]])
                elif c == len(x)-1:
                    lines.append([x1,y[i],xholder[c-1],y[i+1]])
                else:
                    lines.append([x1,y[i],xholder[c],y[i+1]])
                    lines.append([x1,y[i],xholder[c-1],y[i+1]])
            # draw dividing line
            draw_hrule(x,[y[i]],pdf)
        i+=1
    # handle final line
    if len(y)%2 == 0:
        draw_hrule(xholder,[y[-1]],pdf)
    else:
        draw_hrule(x,[y[-1]],pdf)

    pdf.lines(lines)
    return

def draw_vtriline(x,y,spacing,pdf):
    # draw vertical aligned alternating line grid
    # same as htridot but lines lol
    yholder=[i+spacing/2 for i in y]
    yholder.pop()
    lines=[]
    i=0
    while i<len(x)-1:
        if i %2==1:
            # handle less coordinates to more coordinates draw lines.
            for c,y1 in enumerate(yholder):
                lines.append([x[i],y1,x[i+1],y[c]])
                lines.append([x[i],y1,x[i+1],y[c+1]])
            # draw dividing line
            draw_vrule([x[i]],yholder,pdf)
            
        else:
            # handle more coordinates to less coordinates draw lines.
            for c,y1 in enumerate(y):
                if c ==0:
                    lines.append([x[i],y1,x[i+1],yholder[c]])
                elif c == len(y)-1:
                    lines.append([x[i],y1,x[i+1],yholder[c-1]])
                else:
                    lines.append([x[i],y1,x[i+1],yholder[c]])
                    lines.append([x[i],y1,x[i+1],yholder[c-1]])
            # draw dividing line
            draw_vrule([x[i]],y,pdf)
        i+=1
    # handle final line
    if len(x)%2 == 0:
        draw_vrule([x[-1]],yholder,pdf)
    else:
        draw_vrule([x[-1]],y,pdf)

    pdf.lines(lines)
    return


def main():
    parser = argparse.ArgumentParser(description="pagegen",formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("filename",metavar=("FILENAME"),help="Filename.")
    parser.add_argument("--type", metavar=("TYPE"),  default="dots",
                    help="The type of paper to be drawn.  Supported types:\n\tndots\t\tDots in a square grid pattern\n\thrule\t\tHorizontally ruled\n\tvrule\t\tVertically ruled\n\tgrid\t\tSquare grid\n\thtridots\tDots in a horizontally-aligned triangle grid pattern\n\tvtridots\tDots in a vertically-aligned triangle grid pattern\n\thtriline\tHorizontally-aligned triangles\n\tvtriline\tVertically-aligned triangles\nDefault is \"dots\"")
    parser.add_argument("--pagesize",metavar=("PAGESIZE"),default="A4",
                    help = "Standard page sizes. Here are the supported values: \n\tA0-A10\n\tB0-B10\n\tC0-C10\n\tLETTER\n\tLEGAL\n\tELEVENSEVENTEEN\n\tJUNIOR_LEGAL\n\tHALF_LETTER\n\tGOV_LETTER\n\tGOV_LEGAL\n\tTABLOID\n\tLEDGER")
    parser.add_argument("--spacing",metavar=("SPACING"),default="5mm",help="How far apart should the dots/lines be apart.\nAccepts: mm, cm, in, pt, pica\nDefault is 5mm.")
    parser.add_argument("--margin",metavar=("MARGIN"),default="5mm",help="Page margins.\nAccepts: mm, cm, in, pt, pica\nDefault is 5mm.")
    parser.add_argument("--weight",metavar=("WEIGHT"),default="0.5",type=float,help="The size, in pt, should each dot/line be drawn.\nDefault is 0.5pt")
    parser.add_argument("--colour",metavar=("COLOUR"),default="000000",help="The colour of dot/line in hex RGB value.  Default is \"000000\".\n")
    parser.add_argument("--opacity",metavar=("OPACITY"),default="0.5",type=float,help="Opacity value of the dots/lines to be drawn. Must be between 0 and 1  Default is \"0.5\".\n")
    parser.add_argument("--pagewidth",metavar=("PAGEWIDTH"),help="Specify custom page width. Must specify --pageheight. Overwrites --pagesize\nAccepts: mm, cm, in, pt, pica\n")
    parser.add_argument("--pageheight",metavar=("PAGEHEIGHT"),help="Specify custom page height. Must specify --pageheight. Overwrites --pagesize\nAccepts: mm, cm, in, pt, pica\n")
    args = parser.parse_args()
    print(args)
    #page size handling
    if(args.pagewidth or args.pageheight):
        if not args.pagewidth:
            print("Pagewidth value not present.")
            return
        if not args.pageheight:
            print("Pageheight value not present.")
            return
        try:
            width = units.toLength(args.pagewidth)
            height = units.toLength(args.pageheight)
        except ValueError:
            print("Invalid height or width value.")
            return
        page_size=(width,height)
    else:
        if args.pagesize in pagesizemap.keys():
            page_size=pagesizemap[args.pagesize]
        else:
            print("Invalid pagesize.")
            return
    
    spacing=units.toLength(args.spacing)
    margin=units.toLength(args.margin)

    # rgba handling
    try:
        rgba = list(int(args.colour[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        print("Invalid RGB hex code.")
        return
    if 0<=args.opacity<=1:
        rgba.append(args.opacity)
    else:
        print("Invalid opacity value.")
        return
    colour = Color(rgba[0],rgba[1],rgba[2],rgba[3])


    centercoords = [page_size[0]/2,page_size[1]/2]
    if margin == 0:
        use_limit = [page_size[0]/2 - margin-1,page_size[1]/2 - margin-1]
    else:
        use_limit = [page_size[0]/2 - margin,page_size[1]/2 - margin]
    counter =[use_limit[0]/spacing,use_limit[1]/spacing]

    pdf = canvas.Canvas(args.filename,pagesize=page_size)
    pdf.setFillColor(colour)
    pdf.setStrokeColor(colour)
    pdf.setLineWidth(args.weight)

    x,y=get_coords(centercoords,spacing,counter)
    if args.type.lower() == "dots":
        draw_dots(x,y,args.weight,pdf)
    elif args.type.lower() == "hrule":
        draw_hrule([margin,page_size[0]-margin],y,pdf)
    elif args.type.lower() == "vrule":
        draw_vrule(x,[margin,page_size[1]-margin],pdf)
    elif args.type.lower() == "grid":
        draw_grid(x,y,pdf)
    elif args.type.lower() == "htridots":
        draw_htridots(x,y,args.weight,spacing,pdf)
    elif args.type.lower() == "vtridots":
        draw_vtridots(x,y,args.weight,spacing,pdf)
    elif args.type.lower() == "htriline":
        draw_htriline(x,y,spacing,pdf)
    elif args.type.lower() == "vtriline":
        draw_vtriline(x,y,spacing,pdf)
    else:
        print("Invalid Type")
        return

    pdf.save()

    return

main()