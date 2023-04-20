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
	int		num_x,num_y,num_z;
        double          xmin,xmax;
        double          ymin,ymax;
	double		bati_min,bati_max;
        double          zmin,zmax;
        double             lx_top,lx_bot;
        double             ly_top,ly_bot;
        double             lz_top,lz_bot;
        double             lxr,lyr_min,lyr_max;
	int 		option;

        char*     	input2D;
        char*     	input3D;
        ifstream file;
        ofstream file3D;

public:

	data_2d3d(int nxx, int nzz, std::string const& input2D, std::string const& input3D);
	~data_2d3d();
	void meshfn_2d3d(int option);//para modelos Vp, ani
	void datafn_2d3d();//datos TTT
	void reflfn_2d3d();//reflector
        void corr_fn_2d3d();//correlations
        void corr_depfn_2d3d();//para reflector

};//class

#endif
