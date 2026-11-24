"""Original cube, two views, independent CPU triangle/color/depth reference."""
import pathlib, sys, math
FACES=(
    ((-1,-1,-1),(1,-1,-1),(-1,1,-1),(1,1,-1)),
    ((1,-1,1),(-1,-1,1),(1,1,1),(-1,1,1)),
    ((-1,-1,1),(-1,-1,-1),(-1,1,1),(-1,1,-1)),
    ((1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)),
    ((-1,1,-1),(1,1,-1),(-1,1,1),(1,1,1)),
    ((-1,-1,1),(1,-1,1),(-1,-1,-1),(1,-1,-1)),
)
UV=((0,1),(1,1),(0,0),(1,0))
TRIS=((0,1,2),(2,1,3))
PALETTE=((255,0,0),(0,255,0),(0,0,255),(255,255,255))
def project(p,view):
    x,y,z=p
    if view: x,z=z,-x
    # CPU camera projection: all clip coordinates inside the frustum.
    return (.36*x+.18*z,.42*y+.15*z,.50+.12*z-.06*x-.04*y,1+.125*z)
def verts(view):
    return [(*project(p,view),*uv) for face in FACES for p,uv in zip(face,UV)]
def header(path):
    def num(x):
        return format(float(x),".9f")+"f"
    values=[num(x) for view in range(2) for v in verts(view) for x in v]
    pathlib.Path(path).write_text("static const float scene_vertices[]={"+",".join(values)+"};\n")
def raster(view,reverse):
    vs=verts(view)
    triangles=[]
    for face in (range(5,-1,-1) if reverse else range(6)):
        for inds in TRIS:
            v=[vs[face*4+i] for i in inds]
            p=[((a/w+1)*160,(1-b/w)*96,c/w,w,u,t) for a,b,c,w,u,t in v]
            (ax,ay,*_),(bx,by,*_),(cx,cy,*_)=p
            den=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
            if abs(den)<1e-9: raise ValueError("degenerate reference")
            # Barycentric weights divided by gradients give distances to edges.
            grad=(math.hypot(by-cy,cx-bx)/abs(den),
                  math.hypot(cy-ay,ax-cx)/abs(den),
                  math.hypot(ay-by,bx-ax)/abs(den))
            triangles.append((face,p,den,grad))
    result=[]
    for y in range(96):
        for x in range(160):
            px,py=2*x+.5,2*y+.5
            hits=[]; uncertain=False
            for face,p,den,grad in triangles:
                (ax,ay,*_),(bx,by,*_),(cx,cy,*_)=p
                l0=((by-cy)*(px-cx)+(cx-bx)*(py-cy))/den
                l1=((cy-ay)*(px-cx)+(ax-cx)*(py-cy))/den
                l=(l0,l1,1-l0-l1)
                d=[w/g for w,g in zip(l,grad)]
                if min(d)<-0.75: continue
                if min(d)<=0.75:
                    uncertain=True
                    continue
                depth=sum(w*v[2] for w,v in zip(l,p))
                inv=sum(w/v[3] for w,v in zip(l,p))
                u=sum(w*v[4]/v[3] for w,v in zip(l,p))/inv
                t=sum(w*v[5]/v[3] for w,v in zip(l,p))/inv
                color=PALETTE[(int(u>=.5)+2*int(t>=.5)+face%2+view)%4]
                hits.append((depth,color,abs(u-.5)<.004 or abs(t-.5)<.004,face))
            hits.sort(key=lambda h:h[0])
            if uncertain or (hits and hits[0][2]) or (len(hits)>1 and abs(hits[1][0]-hits[0][0])<1e-5):
                result.append(None)
            else:
                result.append(hits[0][1] if hits else (0,0,0))
    return result
if __name__=="__main__":
    header(sys.argv[1])
