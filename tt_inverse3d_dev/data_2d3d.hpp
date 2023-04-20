#ifndef _TOMO_DATA_2D3D
#define _TOMO_DATA_2D3D

#include <iostream>
#include <fstream>
#include <cstdio>
using namespace std;

class data_2d3d {

private:

        int             nx,ny,nz;
        double          plane,dif;
        int             ns,npicks,raycode;
        double          vw,va,tt,dt;
        double          ss,sZ,rr,rZ;
        double          ref,depth;
        char            char_xy;

        int             num,num0,num2;
        int             xmin,xmax;
        int             ymin,ymax;
        int             zmin,zmax;
        int             lx_top,lx_bot;
        int             ly_top,ly_bot;
        int             lz_top,lz_bot;
        int             lxr,lyr;

        char*     	input2D;
        char*     	input3D;
        ifstream file;
        ofstream file3D;

public:

	data_2d3d(int nxx, int nzz, std::string const& input2D, std::string const& input3D);
	~data_2d3d();
	void meshfn_2d3d();
	void datafn_2d3d();
	void reflfn_2d3d();
        void corr_velfn_2d3d();
        void corr_depfn_2d3d();


};//class

#endif
