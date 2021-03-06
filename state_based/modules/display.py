from mayavi import mlab
import numpy as np
import time

from matplotlib import pyplot as plt
import matplotlib.animation as anim

class Display:

    def __init__(self, geom, pd, opt=None, num=10000, tol = 0.001):
        v0 = np.zeros((geom.NX, geom.NY, geom.NZ))
        v0[0] = 1
        self.v0 = v0
        self.pd = pd
        self.geom = geom
        self.num = num
        self.opt = opt
        self.tol = tol

    def launch_pyplot(self, num=100):
        geom = self.geom
        pd = self.pd
        NN = geom.NN
        xs = pd.bcs.x
        ys = pd.bcs.y
        zs = pd.bcs.z
        M = 4
        filt = geom.chi
        def update_graph(n):
            pd.solve(num)
            print(num)
            u,v,w = pd.get_displacement()
            graph._offsets3d = (xs[filt]+M*u[filt], ys[filt]+M*v[filt], zs[filt]+M*w[filt])

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        graph = ax.scatter(xs[filt], ys[filt], zs[filt])
        # manager = plt.get_current_fig_manager()
        # manager.full_screen_toggle()
        ax.set_box_aspect((np.ptp(xs), np.ptp(ys), np.ptp(zs)))
        ani = anim.FuncAnimation(fig, update_graph)
        plt.show()

    @mlab.show
    @mlab.animate(delay=10)
    def anim(self, vox):
        while True:
            self.pd.solve(self.num, tol = self.tol)
            # print("Updating")
            self.opt.step(self.pd)
            # u,v,w = self.pd.get_displacement()
            # vals = np.sqrt(u**2 + v**2 + w**2)
            vals = self.pd.get_fill()
            # vals = vals/np.max(vals)
            vox.mlab_source.scalars = np.reshape(vals,(self.geom.NZ,self.geom.NY,self.geom.NX)).T/np.max(vals)
            yield
    
    def launch(self):
        fig = mlab.figure(size=(600,600))
        vox = mlab.pipeline.volume(mlab.pipeline.scalar_field(self.v0), vmin=0, vmax=1)
        self.anim(vox)